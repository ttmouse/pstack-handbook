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


def main():
    part1, part2, part3 = read("_part1.html"), read("_part2.html"), read("_part3.html")
    doc = part1.split("</main>")[0] + part2 + "\n" + part3
    doc, used = inline_figures(doc)
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
