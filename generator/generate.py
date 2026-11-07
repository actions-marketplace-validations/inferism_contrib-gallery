#!/usr/bin/env python3
"""Generate one contribution chart as an SVG.

  python generate.py --style spiral-galaxy --username you --out contrib-charts
  python generate.py --style spiral-galaxy --theme ice --frame terminal --header terminal --username you
  python generate.py --style spiral-galaxy --sample --out charts     (made-up data)
  python generate.py --list

The default is the chart alone: no frame, no header, no extras, and it follows the viewer's
light or dark setting. Real data needs the gh CLI and a GH_TOKEN (the GitHub Action sets both).
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import common  # noqa: E402
from styles import STYLES  # noqa: E402

ALIASES = {"show": "terminal", "hide": "none"}  # the first release used show and hide for --header


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--style", help="style name, see --list")
    ap.add_argument("--username", default=os.environ.get("CONTRIB_USERNAME", ""))
    ap.add_argument("--theme", default="mono", help=f"color theme: {', '.join(common.THEMES)}")
    ap.add_argument("--accent", default="", help="custom accent color like #ff66aa (overrides --theme)")
    ap.add_argument("--mode", default="auto", choices=common.MODES,
                    help="auto (default) follows the viewer's light or dark setting")
    ap.add_argument("--frame", default="none", choices=common.FRAMES, help="none (default), simple, brackets or terminal")
    ap.add_argument("--header", default="none", help="none (default), title or terminal")
    ap.add_argument("--details", default="hide", choices=["hide", "show"],
                    help="show adds decorations like stars and a stats line under the chart")
    ap.add_argument("--background", default="", help="page color behind the chart, like #0a0a0a")
    ap.add_argument("--out", default="contrib-charts", help="folder for the SVG")
    ap.add_argument("--sample", action="store_true", help="use made-up data instead of GitHub")
    ap.add_argument("--list", action="store_true", help="list the available styles and themes")
    a = ap.parse_args()

    if a.list:
        print("styles: " + ", ".join(sorted(STYLES)))
        print("themes: " + ", ".join(common.THEMES))
        return 0
    if not a.style or not re.fullmatch(r"[a-z0-9-]+", a.style) or a.style not in STYLES:
        print(f"Unknown style {a.style!r}. Available: {', '.join(sorted(STYLES))}", file=sys.stderr)
        return 2

    header = ALIASES.get(a.header, a.header)
    if header not in common.HEADERS:
        print(f"--header must be one of: {', '.join(common.HEADERS)}", file=sys.stderr)
        return 2
    if a.background and not re.fullmatch(r"#[0-9a-fA-F]{6}", a.background):
        print("--background must look like #0a0a0a", file=sys.stderr)
        return 2

    if a.accent:
        if not re.fullmatch(r"#[0-9a-fA-F]{6}", a.accent):
            print("--accent must look like #ff66aa", file=sys.stderr)
            return 2
        accent = a.accent
    elif a.theme in common.THEMES:
        accent = common.THEMES[a.theme]
    else:
        print(f"Unknown theme {a.theme!r}. Available: {', '.join(common.THEMES)}", file=sys.stderr)
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

    svg = common.frame(STYLES[a.style](days), accent, a.mode, a.frame, header, a.details == "show", a.background)
    os.makedirs(a.out, exist_ok=True)
    path = os.path.join(a.out, f"{a.style}.svg")
    with open(path, "w", encoding="utf8", newline="\n") as f:
        f.write(svg)
    print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
