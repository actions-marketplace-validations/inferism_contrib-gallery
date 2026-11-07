"""Shared helpers for the contribution chart generators.

Every style module exposes render(days) and returns a dict:
  w, h, body, defs, title, cmd, aria
frame() wraps that in the shared terminal look and returns the final SVG text.
"""
import json
import math
import random
import re
import subprocess
from datetime import date, datetime, timedelta, timezone

W = 1000
FONT = 'ui-monospace, "SF Mono", Menlo, Consolas, "Courier New", monospace'
BG, PANEL, LINE = "#0b0b0c", "#111113", "#2a2a2d"
TEXT, DIM, BRIGHT = "#d4d4d8", "#9a9aa1", "#ffffff"

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}"""


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def fetch_days(username):
    """Last 12 months of contribution counts, oldest first. Needs the gh CLI and GH_TOKEN."""
    out = subprocess.run(
        ["gh", "api", "graphql", "-f", f"login={username}", "-f", f"query={QUERY}"],
        check=True, capture_output=True, text=True,
    ).stdout
    cal = json.loads(out)["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    today = datetime.now(timezone.utc).date().isoformat()
    days = [
        {"date": d["date"], "count": d["contributionCount"]}
        for w in cal["weeks"] for d in w["contributionDays"] if d["date"] <= today
    ]
    return sorted(days, key=lambda d: d["date"])


def sample_days():
    """Made-up but stable data, used for the gallery previews."""
    rnd = random.Random(11)
    end = date(2026, 11, 7)
    start = end - timedelta(days=364)
    start -= timedelta(days=(start.weekday() + 1) % 7)
    days, d, i, total = [], start, 0, (end - start).days + 1
    while d <= end:
        left = total - i
        if left < 30:
            c = rnd.randint(2, 32) if rnd.random() < 0.9 else 0
        elif left < 110:
            c = rnd.randint(1, 14) if rnd.random() < 0.42 else 0
        else:
            c = rnd.randint(1, 5) if rnd.random() < 0.05 else 0
        days.append({"date": d.isoformat(), "count": c})
        d += timedelta(days=1)
        i += 1
    return days


def peak_of(days):
    return max((d["count"] for d in days), default=0) or 1


def level(count, peak):
    return 0 if count == 0 else min(4, max(1, math.ceil(4 * count / peak)))


def grid_pos(days):
    """(week, weekday) for every day, with weeks counted from the first Sunday."""
    first = date.fromisoformat(days[0]["date"])
    sunday = first.toordinal() - ((first.weekday() + 1) % 7)
    out = []
    for d in days:
        o = date.fromisoformat(d["date"]).toordinal() - sunday
        out.append((o // 7, o % 7))
    return out


def month_totals(days, last=12):
    by = {}
    for d in days:
        k = d["date"][:7]
        by[k] = by.get(k, 0) + d["count"]
    keys = sorted(by)[-last:]
    return [(k, by[k]) for k in keys]


MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def corner(x, y, dx, dy):
    return f'<path d="M{x} {y + dy}V{y}H{x + dx}" fill="none" stroke="#fff" stroke-width="2"/>'


def starfield(w, h, seed, count, top_clear=84, left_clear=520):
    """Dark sky with a light scatter of stars. Keeps the title area clear."""
    rnd = random.Random(seed)
    out = [f'<rect x="0" y="0" width="{w}" height="{h}" fill="#050507"/>']
    for i in range(count):
        x, y = rnd.uniform(12, w - 12), rnd.uniform(10, h - 10)
        if y < top_clear and x < left_clear:
            continue
        r = rnd.choice([0.5, 0.6, 0.7, 0.9, 1.1])
        tw = f' class="tw" style="animation-delay:-{rnd.uniform(0, 4):.1f}s"' if i % 9 == 0 else ""
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#fff" fill-opacity="{rnd.uniform(0.2, 0.65):.2f}"{tw}/>')
    return "".join(out)


THEMES = {
    "mono": "#ffffff",
    "ice": "#7dd3fc",
    "ember": "#fb923c",
    "matrix": "#4ade80",
    "sakura": "#f9a8d4",
    "violet": "#c4b5fd",
}

# the neutral colors the styles draw with, and how strongly each one picks up the accent
NEUTRALS = {
    "#d4d4d8": 0.30,  # body text
    "#9a9aa1": 0.25,  # dim text
    "#2a2a2d": 0.18,  # lines
    "#1b1b1e": 0.10,  # empty bar ticks
    "#111113": 0.06,  # panel
    "#0b0b0c": 0.05,  # background
    "#08080a": 0.05,  # ridgeline fill
    "#050507": 0.05,  # sky
}


def _rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _mix(base, tint, t):
    a, b = _rgb(base), _rgb(tint)
    return "#" + "".join(f"{round(a[i] * (1 - t) + b[i] * t):02x}" for i in range(3))


# accent colors that read well on a light page, for each theme color
LIGHT_ACCENTS = {
    "#ffffff": "#111827",
    "#7dd3fc": "#0369a1",
    "#fb923c": "#c2410c",
    "#4ade80": "#15803d",
    "#f9a8d4": "#be185d",
    "#c4b5fd": "#6d28d9",
}

# how the neutral colors change for each look: (mode, frame) -> {source: replacement}
PALETTES = {
    ("dark", "terminal"): {},
    ("dark", "none"): {  # blends into GitHub's dark page
        "#2a2a2d": "#30363d", "#1b1b1e": "#21262d", "#111113": "#161b22",
        "#0b0b0c": "#0d1117", "#08080a": "#0d1117", "#050507": "#0d1117",
    },
    ("light", "terminal"): {
        "#d4d4d8": "#3f3f46", "#9a9aa1": "#6b6b74", "#2a2a2d": "#d4d4d8", "#1b1b1e": "#e4e4e7",
        "#111113": "#f4f4f5", "#0b0b0c": "#fbfbfc", "#08080a": "#fbfbfc", "#050507": "#eef0f3",
    },
    ("light", "none"): {  # blends into GitHub's light page
        "#d4d4d8": "#3f3f46", "#9a9aa1": "#6b6b74", "#2a2a2d": "#d0d7de", "#1b1b1e": "#e7ebef",
        "#111113": "#f6f8fa", "#0b0b0c": "#ffffff", "#08080a": "#ffffff", "#050507": "#ffffff",
    },
}
TEXT_NEUTRALS = ("#d4d4d8", "#9a9aa1")


def apply_theme(svg, accent, mode="dark", boxed=True):
    """Recolor a finished SVG: white becomes the accent, the greys follow the look."""
    white = accent.lower() in ("#fff", "#ffffff")
    if mode == "dark" and boxed and white:
        return svg
    palette = PALETTES[(mode, "terminal" if boxed else "none")]
    ink = LIGHT_ACCENTS.get(accent.lower(), accent) if mode == "light" else accent
    pairs = {"#ffffff": ink, "#fff": ink}
    for src, tint in NEUTRALS.items():
        base = palette.get(src, src)
        tinted = ((mode == "dark" and boxed) or src in TEXT_NEUTRALS) and not (mode == "dark" and white)
        pairs[src] = _mix(base, ink, tint) if tinted else base
    return re.sub(
        r"#(?:ffffff|fff|d4d4d8|9a9aa1|2a2a2d|1b1b1e|111113|0b0b0c|08080a|050507)(?![0-9a-fA-F])",
        lambda m: pairs[m.group(0).lower()],
        svg,
    )


def frame(chart, accent="#ffffff", mode="dark", boxed=True, header=True):
    """The shared frame around a style's output, recolored for the theme and look.

    boxed=False drops the border, corner brackets and dots. header=False drops the title lines.
    """
    return apply_theme(_frame(chart, boxed, header), accent, mode, boxed)


def _frame(chart, boxed=True, header=True):
    """Wrap a style's output in the shared frame and return the SVG text."""
    w, h = chart["w"], chart["h"]
    shift = 0
    if not header:  # close the gap the title lines would have filled
        shift = max(0, chart.get("top", 84) - 24)
        h -= shift
    title = (
        f'<text x="28" y="46" class="hi" font-size="28" font-weight="700"><tspan class="dim">~/</tspan>{esc(chart["title"])}</text>'
        f'<text x="28" y="72" class="dim" font-size="14">$ {esc(chart["cmd"])}</text>'
    ) if header else ""
    body = f'<g transform="translate(0 {-shift})">{chart["body"]}</g>' if shift else chart["body"]
    x, y, bw, bh, r = (1, 1, w - 2, h - 2, 14) if boxed else (0, 0, w, h, 0)
    dots = f'<rect x="1" y="1" width="{bw}" height="{bh}" rx="14" fill="url(#dots)"/>\n' if boxed else ""
    edge = (
        f'<rect x="1" y="1" width="{bw}" height="{bh}" rx="14" fill="none" stroke="{LINE}" stroke-width="2"/>\n'
        + corner(1, 1, 18, 18) + corner(w - 1, 1, -18, 18) + corner(1, h - 1, 18, -18) + corner(w - 1, h - 1, -18, -18)
        + "\n"
    ) if boxed else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
        f'aria-label="{esc(chart["aria"])}">\n'
        f'<defs><clipPath id="panel"><rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="{r}"/></clipPath>'
        '<pattern id="dots" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="#fff" fill-opacity="0.05"/></pattern>'
        f'{chart.get("defs", "")}</defs>\n'
        f"<style>text {{ font-family: {FONT}; }} .dim {{ fill: {DIM}; }} .txt {{ fill: {TEXT}; }} .hi {{ fill: {BRIGHT}; }} "
        ".blink { animation: blink 1.1s steps(1) infinite; } @keyframes blink { 50% { opacity: 0; } } "
        ".tw { animation: tw 4s ease-in-out infinite; } @keyframes tw { 50% { opacity: 0.25; } }</style>\n"
        f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="{r}" fill="{BG}"/>\n'
        f'{dots}<g clip-path="url(#panel)">{body}</g>\n{title}\n{edge}</svg>\n'
    )
