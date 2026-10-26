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

def load(folder):
    books = json.load(open(os.path.join(folder, "books.json")))["books"]
    chapters, glossary = [], []
    for f in sorted(glob.glob(os.path.join(folder, "*.json"))):
        if f.endswith("books.json"):
            continue
        d = json.load(open(f))
        chapters += d.get("chapters", [])
        glossary += d.get("glossary", [])
    return books, chapters, glossary

def tidy(chapters):
    for c in chapters:
        c.setdefault("sections", [])
        if c.get("book") == "studies":
            for d in c.get("diagrams", []):
                if d.get("type") == "lexicon":
                    d.setdefault("after", 0)  # the word list follows the opening section
        for d in c.get("diagrams", []):
            if d.get("type") == "compare":
                n = min(len(d["left"]["items"]), len(d["right"]["items"]))
                d["left"]["items"], d["right"]["items"] = d["left"]["items"][:n], d["right"]["items"][:n]

books, chapters, glossary = load(os.path.join(ROOT, "content"))
BOOK_ORDER = {"words": 0, "gospel": 1, "studies": 2}
chapters.sort(key=lambda c: (BOOK_ORDER.get(c["book"], 9), part_rank(c.get("part")), c.get("order", 0)))
ids = [c["id"] for c in chapters]
assert len(ids) == len(set(ids)), "duplicate chapter ids"
tidy(chapters)
data = {"en": {"books": books, "chapters": chapters, "glossary": glossary}}

# Tamil: same chapters in the same order; any chapter not yet translated falls back to English
ta_dir = os.path.join(ROOT, "content/ta")
if os.path.exists(os.path.join(ta_dir, "books.json")):
    tb, tc, tg = load(ta_dir)
    by_id = {c["id"]: c for c in tc}
    ta_chapters, missing = [], []
    for c in chapters:
        t = by_id.get(c["id"])
        if t is None:
            missing.append(c["id"])
            t = c
        else:
            t = dict(t)
        t["partKey"] = c.get("part")  # English part name groups chapters in both languages
        ta_chapters.append(t)
    tidy(ta_chapters)
    data["ta"] = {"books": tb, "chapters": ta_chapters, "glossary": tg or glossary}
    print(f"Tamil: {len(chapters) - len(missing)}/{len(chapters)} chapters translated" + (f"; English fallback for {', '.join(missing)}" if missing else ""))

js = "window.APP_DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + ";"
app = open(os.path.join(ROOT, "src/app.html"), encoding="utf-8").read().replace("/*__DATA__*/", js)

# guard: the authors are never named in the app
for banned in ["Eitan", "Bar,", "ஈட்டான்", "ஈத்தான்", "எய்டன்", "ஈதான்"]:
    assert banned not in js, f"banned name found: {banned}"

# guard: the app's own script must parse (catches a stray quote in interface text)
import re, shutil, subprocess, tempfile
if shutil.which("node"):
    src = open(os.path.join(ROOT, "src/app.html"), encoding="utf-8").read()
    code = re.findall(r"<script>(.*?)</script>", src, re.S)[-1]
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(code)
    r = subprocess.run(["node", "--check", f.name], capture_output=True, text=True)
    os.unlink(f.name)
    assert r.returncode == 0, "app script does not parse:\n" + r.stderr

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
