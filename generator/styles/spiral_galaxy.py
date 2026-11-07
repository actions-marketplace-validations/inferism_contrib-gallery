"""Every day is a star on a spiral arm. Brighter, bigger stars are busier days."""
import math
import random

from common import W, level, peak_of, starfield

H = 520


def render(days):
    n, peak = len(days), peak_of(days)
    rnd = random.Random(8)
    cx, cy = W / 2, 292
    out = [f'<ellipse cx="{cx}" cy="{cy}" rx="105" ry="62" fill="url(#gcore)"/>']
    for _ in range(300):  # faint dust around the arm
        a, d = rnd.uniform(0, math.tau), math.sqrt(rnd.random()) * 175
        out.append(
            f'<circle cx="{cx + math.cos(a) * d * 1.95:.1f}" cy="{cy + math.sin(a) * d * 1.12:.1f}" r="0.6" '
            f'fill="#fff" fill-opacity="{rnd.uniform(0.08, 0.3):.2f}"/>'
        )
    for i, d in enumerate(days):
        t = i / max(1, n - 1)
        ang = t * math.tau * 3 + 0.6
        rad = 14 + t * 150 + (rnd.random() - 0.5) * 7
        x, y = cx + math.cos(ang) * rad * 1.95, cy + math.sin(ang) * rad * 1.12
        c = d["count"]
        if c:
            lv = level(c, peak)
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{1.3 + lv * 0.85:.1f}" fill="#fff" fill-opacity="{0.45 + lv * 0.13:.2f}"/>')
        else:
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="0.8" fill="#fff" fill-opacity="0.16"/>')
    total = sum(d["count"] for d in days)
    return {
        "w": W, "h": H, "body": "".join(out), "deco": starfield(W, H, 7, 190), "foot": 486, "top": 100,
        "caption": f"{total:,} contributions · peak {peak}/day · one star per day",
        "defs": '<radialGradient id="gcore"><stop offset="0" stop-color="#fff" stop-opacity="0.4"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>',
        "title": "spiral-galaxy", "cmd": "render-galaxy --last 365d  # one star per day",
        "aria": f"Spiral galaxy of {total:,} contributions over the last year, peak {peak} in a day",
    }
