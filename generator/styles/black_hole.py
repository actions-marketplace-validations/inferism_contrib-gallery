"""A black hole: your days orbit it on an accretion disk, the newest days closest to the edge."""
import math

from common import W, level, peak_of, starfield

H = 580
TILT = 0.24
CX, CY, HOLE = 500, 310, 100
GOLDEN = 2.399963


def render(days):
    n, peak = len(days), peak_of(days)
    back, front = [], []
    for i, d in enumerate(days):
        t = i / max(1, n - 1)
        rad = HOLE + 24 + (1 - t) * 275
        ang = i * GOLDEN
        x, y = CX + rad * math.cos(ang), CY + rad * TILT * math.sin(ang)
        c = d["count"]
        lv = level(c, peak)
        dot = (
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{1.2 + lv * 0.7 if c else 0.8:.1f}" '
            f'fill="#fff" fill-opacity="{0.45 + lv * 0.13 if c else 0.16:.2f}"/>'
        )
        (front if math.sin(ang) > 0 else back).append(dot)

    rings = "".join(
        f'<ellipse cx="{CX}" cy="{CY}" rx="{r}" ry="{r * TILT:.1f}" fill="none" stroke="#2a2a2d" stroke-width="0.8"/>'
        for r in range(HOLE + 30, HOLE + 310, 24)
    )
    hole = (
        f'<circle cx="{CX}" cy="{CY}" r="{HOLE + 14}" fill="#fff" fill-opacity="0.08"/>'
        f'<circle cx="{CX}" cy="{CY}" r="{HOLE}" fill="#050507"/>'
        f'<circle cx="{CX}" cy="{CY}" r="{HOLE}" fill="none" stroke="#fff" stroke-width="2" stroke-opacity="0.85"/>'
        f'<path d="M{CX - HOLE - 46} {CY}A{HOLE + 46} {HOLE + 46} 0 0 1 {CX + HOLE + 46} {CY}" fill="none" stroke="#fff" stroke-width="1.4" stroke-opacity="0.4"/>'
        f'<path d="M{CX - HOLE - 46} {CY}A{HOLE + 46} {HOLE + 46} 0 0 0 {CX + HOLE + 46} {CY}" fill="none" stroke="#fff" stroke-width="1.4" stroke-opacity="0.25"/>'
    )
    total = sum(d["count"] for d in days)
    return {
        "w": W, "h": H, "body": rings + "".join(back) + hole + "".join(front), "defs": "",
        "deco": starfield(W, H, 21, 160), "foot": CY + HOLE + 60, "top": 150,
        "caption": f"{total:,} contributions · one point per day · the newest days orbit closest to the hole",
        "title": "black-hole", "cmd": "orbit --last 365d  # one point per day",
        "aria": f"Black hole with an accretion disk of {total:,} contributions, one point per day",
    }
