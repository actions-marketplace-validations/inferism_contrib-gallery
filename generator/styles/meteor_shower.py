"""A meteor shower: every active day is a streak across the sky, longer and brighter when busier."""
import math
import random

from common import W, grid_pos, level, peak_of, starfield

H = 520
ANGLE = 0.5


def render(days):
    peak = peak_of(days)
    pos = grid_pos(days)
    rnd = random.Random(21)
    ca, sa = math.cos(ANGLE), math.sin(ANGLE)
    out = []
    for day, (w, _) in zip(days, pos):
        c = day["count"]
        if not c:
            continue
        x, y = 30 + w / 52 * (W - 170), 100 + rnd.random() * (H - 240)
        length = 16 + c / peak * 70
        lv = level(c, peak)
        x2, y2 = x + length * ca, y + length * sa
        out.append(
            f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#fff" stroke-opacity="0.12"/>'
            f'<line class="meteor" pathLength="100" x1="{x:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#fff" '
            f'stroke-width="{1 + lv * 0.4:.1f}" stroke-linecap="round" stroke-opacity="{0.5 + lv * 0.12:.2f}" style="animation-delay:{rnd.random() * 5:.2f}s"/>'
        )
    css = (
        ".meteor { stroke-dasharray: 14 120; stroke-dashoffset: 14; animation: shoot 5s linear infinite; } "
        "@keyframes shoot { from { stroke-dashoffset: 14; } to { stroke-dashoffset: -120; } }"
    )
    total = sum(d["count"] for d in days)
    return {
        "w": W, "h": H, "body": "".join(out), "defs": "", "css": css, "deco": starfield(W, H, 5, 150), "foot": H - 90, "top": 90,
        "caption": f"{total:,} contributions · a streak for every active day",
        "title": "meteor-shower", "cmd": "watch --last 365d  # a meteor for every active day",
        "aria": "A meteor shower with a streak for each active day of the last year, longer for busier days",
    }
