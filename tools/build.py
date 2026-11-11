#!/usr/bin/env python3
"""Assemble index.html from the source shards, inlining the SVG figures.

    python3 tools/diagrams.py   # regenerate src/figs/*.svg
    python3 tools/build.py      # rebuild index.html and validate

A shard can contain <!--FIG:name-->, which is replaced by src/figs/name.svg.
The build fails on a missing figure, a dead in-page link, an external resource,
or an unbalanced block tag.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
FIGS = os.path.join(SRC, "figs")


def read(name):
    with open(os.path.join(SRC, name), encoding="utf-8") as fh:
        return fh.read()


def inline_figures(html):
    used = []

    def repl(m):
        name = m.group(1)
        path = os.path.join(FIGS, name + ".svg")
        if not os.path.exists(path):
            sys.exit(f"missing figure: {path}")
        used.append(name)
        with open(path, encoding="utf-8") as fh:
            return fh.read()

    out = re.sub(r"<!--FIG:([a-z0-9-]+)-->", repl, html)
    return out, used


def square_figures(html):
    """The drawings take the page's square language: drop rounded corners inside inlined SVGs."""
    def repl(m):
        return re.sub(r'\s+rx="[0-9.]+"', "", m.group(0))
    return re.sub(r"<svg\b.*?</svg>", repl, html, flags=re.S)


def split_numbers(html):
    """<h2 id="x">3 二十三本 playbook</h2> -> numeral in its own span, hung in the margin."""
    def repl(m):
        attrs, text = m.group(1), m.group(2).strip()
        mm = re.match(r"^([0-9]+(?:\.[0-9]+)?|[A-Z])\s+(.+)$", text)
        if not mm:
            # "附录 A 命令速查": the word hangs in the margin, the letter stays with the title
            mm = re.match(r"^(附录)\s+([A-Z])\s+(.+)$", text)
            if mm:
                return (f'<h2{attrs}><span class="num">{mm.group(1)}</span>'
                        f'<span class="ttl">{mm.group(2)} {mm.group(3)}</span></h2>')
            return m.group(0)
        return (f'<h2{attrs}><span class="num">{mm.group(1)}</span>'
                f'<span class="ttl">{mm.group(2)}</span></h2>')
    return re.sub(r"<h2([^>]*)>(.*?)</h2>", repl, html, flags=re.S)


# Where an entry's English name stops: at the first character outside ASCII.
NON_ASCII = r"(?=[^\x00-\x7f])"

# Playbook numbers are pinned here, by the English half of the entry title, and
# never counted off the page. A reader who cites "第 3 章 06" must keep landing on
# Trace forensics after the chapter is edited or a new playbook is inserted, so
# inserting one means giving it a number here — not shifting the twenty below it.
# Nothing here reaches the playbook files themselves: routing is by description,
# and numbering the handbook cannot change what poteto-mode selects.
PLAYBOOK_NUMBERS = {
    "Investigation": 1,
    "Bug fix": 2,
    "Perf issue": 3,
    "Hillclimb": 4,
    "Runtime forensics": 5,
    "Trace forensics": 6,
    "Feature": 7,
    "Refactoring": 8,
    "Prototype": 9,
    "Visual parity": 10,
    "Authoring a skill": 11,
    "Eval": 12,
    "Babysit": 13,
    "Shipping": 14,
    "Opening a PR": 15,
    "Autonomous run": 16,
    "Orchestrate": 17,
    "Autopilot-full": 18,
    "Autopilot-stack": 19,
    "Session pickup": 20,
    "Pause safely": 21,
    "Multi-phase plan": 22,
    "Worktree and simulator cleanup": 23,
}


def number_playbooks(html):
    """Pin the playbook entries in chapter 3 to their number, so one can be cited as "第 3 章 06".

    The number lives in the published page only: it is assigned here from
    PLAYBOOK_NUMBERS and nowhere in the playbook files themselves. Both directions
    are checked — an entry with no number and a number with no entry both fail the
    build, so the two can never drift apart in silence.
    """
    start = html.find('<h2 id="playbooks">')
    if start < 0:
        return html, 0
    end = html.find("<h2 ", start + 1)
    if end < 0:
        end = len(html)
    head, body, tail = html[:start], html[start:end], html[end:]
    numbers, unnumbered = [], []

    def repl(m):
        title = m.group(1).strip()
        # The English half ends at the first non-ASCII character: "Bug fix 修缺陷" -> "Bug fix".
        # Matching the whole key against it keeps "Eval runs" from quietly passing as "Eval".
        english = re.split(NON_ASCII, title, maxsplit=1)[0].strip()
        if english not in PLAYBOOK_NUMBERS:
            unnumbered.append(title)
            return m.group(0)
        # The title is published exactly as written; only the English half is used,
        # to look the number up. Splitting it for display would drop the space
        # between "Trace forensics" and "轨迹取证" when the line is copied.
        n = PLAYBOOK_NUMBERS[english]
        numbers.append(english)
        return (f'<h4 class="pb" id="pb-{n:02d}">'
                f'<span class="pbnum">{n:02d}</span>'
                f'<span class="pbtitle">{title}</span></h4>')

    body = re.sub(r"<h4>(.*?)</h4>", repl, body, flags=re.S)
    doc = head + body + tail

    missing = sorted(set(PLAYBOOK_NUMBERS) - set(numbers))
    repeated = sorted({k for k in numbers if numbers.count(k) > 1})
    if unnumbered or missing or repeated:
        sys.exit("playbook numbering out of step with PLAYBOOK_NUMBERS\n"
                 f"  entries with no number: {unnumbered}\n"
                 f"  numbers with no entry: {missing}\n"
                 f"  entries matched twice: {repeated}")
    return doc, len(numbers)


def label_cells(html):
    """Copy each column's header text onto its cells as data-label, so a phone can stack the table."""
    def repl(m):
        table = m.group(0)
        rows = re.findall(r"<tr[^>]*>.*?</tr>", table, flags=re.S)
        if not rows:
            return table
        labels = [re.sub(r"<[^>]+>", "", h).strip()
                  for h in re.findall(r"<th[^>]*>(.*?)</th>", rows[0], flags=re.S)]
        if not labels:
            return table
        out = table
        for row in rows[1:]:
            counter = [0]

            def cell(cm):
                idx = counter[0]
                counter[0] += 1
                if idx >= len(labels) or not labels[idx]:
                    return cm.group(0)
                return cm.group(0).replace("<td", f'<td data-label="{labels[idx]}"', 1)

            out = out.replace(row, re.sub(r"<td[^>]*>", cell, row), 1)
        return out
    return re.sub(r"<table[^>]*>.*?</table>", repl, html, flags=re.S)


def main():
    part1, part2, part3 = read("_part1.html"), read("_part2.html"), read("_part3.html")
    doc = part1.split("</main>")[0] + part2 + "\n" + part3
    doc, used = inline_figures(doc)
    doc = square_figures(doc)
    doc = split_numbers(doc)
    doc, n_playbooks = number_playbooks(doc)
    doc = label_cells(doc)
    doc, n_tables = re.subn(r"(<table[^>]*>.*?</table>)", r'<div class="tw">\1</div>',
                            doc, flags=re.S)

    ids = set(re.findall(r'id="([^"]+)"', doc))
    links = set(re.findall(r'href="#([^"]+)"', doc))
    missing = sorted(links - ids)
    external = sorted(set(re.findall(r'(?:src|href)="(https?://[^"]+)"', doc)))
    unbalanced = [
        (t, len(re.findall(r"<%s[ >]" % t, doc)), len(re.findall(r"</%s>" % t, doc)))
        for t in ("div", "table", "ol", "ul", "pre", "figure", "svg", "figcaption")
        if len(re.findall(r"<%s[ >]" % t, doc)) != len(re.findall(r"</%s>" % t, doc))
    ]

    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(doc)

    print(f"bytes     {len(doc.encode())}")
    print(f"figures   {len(used)}: {', '.join(used)}")
    print(f"h2        {len(re.findall(r'<h2 ', doc))}")
    print(f"playbooks {n_playbooks} (numbered 01+)")
    print(f"tables    {n_tables} (wrapped for mobile scroll)")
    print(f"pre       {len(re.findall(r'<pre>', doc))}")
    print(f"missing   {missing}")
    print(f"external  {external}")
    print(f"unbalanced {unbalanced}")
    if missing or external or unbalanced:
        sys.exit(1)


if __name__ == "__main__":
    main()
