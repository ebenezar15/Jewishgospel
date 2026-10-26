#!/usr/bin/env python3
"""Check that a Tamil content file mirrors its English source in structure.

usage: python3 tools/check_ta.py content/words-a.json content/ta/words-a.json
"""
import json, re, sys

KEEP = {"id", "book", "order", "num", "hebrew", "greek", "root", "translit", "type", "after", "pos", "a", "ch", "lang", "word", "related"}
TAMIL = re.compile(r"[஀-௿]")
errors = []

def walk(en, ta, path):
    if type(en) != type(ta) and not (en is None or ta is None):
        errors.append(f"{path}: type {type(en).__name__} vs {type(ta).__name__}")
        return
    if isinstance(en, dict):
        if set(en) != set(ta):
            errors.append(f"{path}: keys differ {sorted(set(en) ^ set(ta))}")
        for k in en:
            if k in ta:
                walk(en[k], ta[k], f"{path}.{k}")
    elif isinstance(en, list):
        if len(en) != len(ta):
            errors.append(f"{path}: {len(en)} items vs {len(ta)}")
        for i, (a, b) in enumerate(zip(en, ta)):
            walk(a, b, f"{path}[{i}]")
    elif isinstance(en, str):
        key = path.rsplit(".", 1)[-1].split("[")[0]
        # chapter-level "root" is Hebrew letters; a tree diagram's "root" is a text label
        keep = key in KEEP and not (key == "root" and ".diagrams[" in path)
        if keep:
            if en != ta:
                errors.append(f"{path}: must stay unchanged ({en!r} -> {ta!r})")
        elif re.search(r"[A-Za-z]{3}", en) and not TAMIL.search(ta):
            errors.append(f"{path}: not translated: {ta[:60]!r}")
    elif en != ta:
        errors.append(f"{path}: value must stay {en!r}, got {ta!r}")

en = json.load(open(sys.argv[1]))
ta = json.load(open(sys.argv[2]))
walk(en, ta, "$")
for e in errors[:60]:
    print(e)
print(f"{len(errors)} problem(s)" if errors else "OK: structure matches and text is Tamil")
sys.exit(1 if errors else 0)
