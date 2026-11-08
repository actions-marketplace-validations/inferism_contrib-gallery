"""One ring per month. The dots on a ring are that month's days."""
import math

from common import W, level, peak_of

H = 600
CX, CY = 500, 320


def render(days):
    peak = peak_of(days)
    by_month = {}
    for d in days:
        by_month.setdefault(d["date"][:7], []).append(d)
    keys = sorted(by_month)[-12:]
    out = []
    for m, k in enumerate(keys):
        r = 34 + m * 18
        out.append(f'<circle cx="{CX}" cy="{CY}" r="{r}" fill="none" stroke="#2a2a2d" stroke-width="1"/>')
        n = len(by_month[k])
        for i, d in enumerate(by_month[k]):
            a = i / n * math.tau - math.pi / 2
            c = d["count"]
            lv = level(c, peak)
            out.append(
                f'<circle cx="{CX + r * math.cos(a):.1f}" cy="{CY + r * math.sin(a):.1f}" r="{1.5 + lv * 0.75 if c else 0.9:.1f}" '
                f'fill="#fff" fill-opacity="{0.45 + lv * 0.13 if c else 0.2:.2f}"/>'
            )
    total = sum(d["count"] for d in days)
    return {
        "w": W, "h": H, "body": "".join(out), "defs": "", "foot": CY + 34 + 11 * 18 + 10, "top": 70,
        "caption": f"{total:,} contributions · one ring per month, the newest month on the outside",
        "title": "orbit-rings", "cmd": "orbit --last 12mo  # one ring per month",
        "aria": f"Orbit rings, one ring per month, with a dot for each of the {len(days)} days",
    }
