#!/usr/bin/env python3
"""Merge content/*.json into the app and write the single-file builds.

  index.html      full standalone page (works offline, installable on GitHub Pages)
  dist/artifact.html  same app without the document skeleton (for hosted preview)
"""
import glob, json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
PART_ORDER = ["Start Here", "Part I", "Part II", "Part III", "Part IV", "Part V", "Part VI"]

def part_rank(p):
    for i, k in enumerate(PART_ORDER):
        if p and (p == k or p.startswith(k + ":")):
            return i
    return 99

books = json.load(open(os.path.join(ROOT, "content/books.json")))["books"]
chapters, glossary = [], []
for f in sorted(glob.glob(os.path.join(ROOT, "content/*.json"))):
    if f.endswith("books.json"):
        continue
    d = json.load(open(f))
    chapters += d.get("chapters", [])
    glossary += d.get("glossary", [])

chapters.sort(key=lambda c: (0 if c["book"] == "words" else 1, part_rank(c.get("part")), c.get("order", 0)))
ids = [c["id"] for c in chapters]
assert len(ids) == len(set(ids)), "duplicate chapter ids"
for c in chapters:
    c.setdefault("sections", [])
    for d in c.get("diagrams", []):
        if d.get("type") == "compare":
            n = min(len(d["left"]["items"]), len(d["right"]["items"]))
            d["left"]["items"], d["right"]["items"] = d["left"]["items"][:n], d["right"]["items"][:n]

data = {"books": books, "chapters": chapters, "glossary": glossary}
js = "window.APP_DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + ";"
app = open(os.path.join(ROOT, "src/app.html"), encoding="utf-8").read().replace("/*__DATA__*/", js)

# guard: the authors are never named in the app
for banned in ["Eitan", "Bar,"]:
    assert banned not in js, f"banned name found: {banned}"

os.makedirs(os.path.join(ROOT, "dist"), exist_ok=True)
open(os.path.join(ROOT, "dist/artifact.html"), "w", encoding="utf-8").write(app)

head_extra = (
    '<link rel="manifest" href="manifest.webmanifest">\n'
    '<meta name="theme-color" content="#1f4e8c">\n'
    '<link rel="icon" href="icon.svg" type="image/svg+xml">\n'
    '<link rel="apple-touch-icon" href="icon-512.png">\n'
    '<meta name="apple-mobile-web-app-capable" content="yes">\n'
    '<meta name="mobile-web-app-capable" content="yes">\n'
)
title_end = app.index("</style>") + len("</style>")
page = ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
        + head_extra + app[:title_end] + "\n<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}[hidden]{display:none!important}img{max-width:100%}</style>\n</head>\n<body>\n"
        + app[title_end:] + "\n</body>\n</html>\n")
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(page)
words = sum(len(" ".join(p for s in c["sections"] for p in s["p"]).split()) for c in chapters)
print(f"{len(chapters)} chapters, {len(glossary)} glossary terms, ~{words} words of explanation, index.html {len(page)//1024} KB")
