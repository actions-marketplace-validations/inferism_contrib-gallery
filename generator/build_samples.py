#!/usr/bin/env python3
"""Rebuild the gallery samples: samples/<theme>/<style>.svg for every style and theme.

The samples are the default look (just the chart) on the gallery's dark page color.
  python generator/build_samples.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import common  # noqa: E402
from styles import STYLES  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "samples")
GALLERY_BG = "#08080a"


def main():
    days = common.sample_days()
    sizes = {}
    for theme, accent in common.THEMES.items():
        folder = os.path.join(ROOT, theme)
        os.makedirs(folder, exist_ok=True)
        for name, render in STYLES.items():
            chart = render(days)
            svg = common.frame(chart, accent, "dark", "none", "none", False, GALLERY_BG)
            with open(os.path.join(folder, f"{name}.svg"), "w", encoding="utf8", newline="\n") as f:
                f.write(svg)
            sizes[name] = [chart["w"], int(svg.split('height="', 1)[1].split('"', 1)[0])]
    with open(os.path.join(ROOT, "sizes.json"), "w", encoding="utf8", newline="\n") as f:
        json.dump(sizes, f, indent=1, sort_keys=True)
        f.write("\n")
    print(f"built {len(STYLES) * len(common.THEMES)} samples")


if __name__ == "__main__":
    main()
