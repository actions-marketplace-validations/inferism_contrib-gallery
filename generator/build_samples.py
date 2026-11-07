#!/usr/bin/env python3
"""Rebuild the gallery samples: samples/<theme>/<style>.svg for every style and theme.

  python generator/build_samples.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import common  # noqa: E402
from styles import STYLES  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "samples")


def main():
    days = common.sample_days()
    for theme, accent in common.THEMES.items():
        folder = os.path.join(ROOT, theme)
        os.makedirs(folder, exist_ok=True)
        for name, render in STYLES.items():
            with open(os.path.join(folder, f"{name}.svg"), "w", encoding="utf8", newline="\n") as f:
                f.write(common.frame(render(days), accent))
    print(f"built {len(STYLES) * len(common.THEMES)} samples")


if __name__ == "__main__":
    main()
