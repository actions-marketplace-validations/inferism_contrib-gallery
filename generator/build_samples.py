#!/usr/bin/env python3
"""Rebuild everything the gallery and README need from the styles:

  samples/<theme>/<style>.svg   every style in every theme, as the plain default on the gallery's page color
  samples/styles.json           the list the gallery page loads
  README.md                     the styles table between the styles:start and styles:end markers

  python generator/build_samples.py
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import common  # noqa: E402
from styles import STYLES  # noqa: E402
from styles.catalog import CATALOG  # noqa: E402

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
ROOT = os.path.join(BASE, "samples")
GALLERY_BG = "#08080a"


def write(path, text):
    with open(path, "w", encoding="utf8", newline="\n") as f:
        f.write(text)


def main():
    ids = [c[0] for c in CATALOG]
    missing = set(STYLES) ^ set(ids)
    if missing:
        sys.exit(f"STYLES and CATALOG disagree about: {', '.join(sorted(missing))}")

    days = common.sample_days()
    height = {}
    for theme, accent in common.THEMES.items():
        folder = os.path.join(ROOT, theme)
        os.makedirs(folder, exist_ok=True)
        for name, render in STYLES.items():
            svg = common.frame(render(days), accent, "dark", "none", "none", False, GALLERY_BG)
            write(os.path.join(folder, f"{name}.svg"), svg)
            height[name] = int(svg.split('height="', 1)[1].split('"', 1)[0])

    write(
        os.path.join(ROOT, "styles.json"),
        json.dumps([{"id": i, "title": t, "cat": c, "note": n, "h": height[i]} for i, t, c, n in CATALOG], indent=1) + "\n",
    )

    readme = os.path.join(BASE, "README.md")
    text = open(readme, encoding="utf8").read()
    rows = "\n".join(f"| {t[0].upper() + t[1:]} | `{i}` | {n} |" for i, t, _, n in CATALOG)
    table = f"<!-- styles:start -->\n| Style | Name to use | What it shows |\n|---|---|---|\n{rows}\n<!-- styles:end -->"
    new = re.sub(r"<!-- styles:start -->.*?<!-- styles:end -->", lambda _: table, text, flags=re.S)
    if new == text and "<!-- styles:start -->" not in text:
        sys.exit("README.md has no styles:start and styles:end markers")
    write(readme, new)
    print(f"built {len(STYLES) * len(common.THEMES)} samples for {len(CATALOG)} styles")


if __name__ == "__main__":
    main()
