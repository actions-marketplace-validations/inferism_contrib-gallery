#!/usr/bin/env python3
"""Generate one contribution chart as an SVG.

  python generate.py --style spiral-galaxy --username you --out contrib-charts
  python generate.py --style spiral-galaxy --sample --out samples     (made-up data)
  python generate.py --list

Real data needs the gh CLI and a GH_TOKEN (the GitHub Action sets both).
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import common  # noqa: E402
from styles import STYLES  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--style", help="style name, see --list")
    ap.add_argument("--username", default=os.environ.get("CONTRIB_USERNAME", ""))
    ap.add_argument("--out", default="contrib-charts", help="folder for the SVG")
    ap.add_argument("--sample", action="store_true", help="use made-up data instead of GitHub")
    ap.add_argument("--list", action="store_true", help="list the available styles")
    a = ap.parse_args()

    if a.list:
        print("\n".join(sorted(STYLES)))
        return 0
    if not a.style or not re.fullmatch(r"[a-z0-9-]+", a.style) or a.style not in STYLES:
        print(f"Unknown style {a.style!r}. Available: {', '.join(sorted(STYLES))}", file=sys.stderr)
        return 2

    if a.sample:
        days = common.sample_days()
    else:
        if not a.username:
            print("Missing --username (or CONTRIB_USERNAME).", file=sys.stderr)
            return 2
        days = common.fetch_days(a.username)
    if not days:
        print("No contribution data returned.", file=sys.stderr)
        return 1

    svg = common.frame(STYLES[a.style](days))
    os.makedirs(a.out, exist_ok=True)
    path = os.path.join(a.out, f"{a.style}.svg")
    with open(path, "w", encoding="utf8", newline="\n") as f:
        f.write(svg)
    print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
