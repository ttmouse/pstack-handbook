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
    print(f"tables    {n_tables} (wrapped for mobile scroll)")
    print(f"pre       {len(re.findall(r'<pre>', doc))}")
    print(f"missing   {missing}")
    print(f"external  {external}")
    print(f"unbalanced {unbalanced}")
    if missing or external or unbalanced:
        sys.exit(1)


if __name__ == "__main__":
    main()
