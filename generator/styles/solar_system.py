"""A solar system: one planet for each month, orbiting a sun. Bigger planets are busier months."""
import math

from common import MONTHS, W

H = 600
CX, CY = 500, 320


def render(days):
    by_month = {}
    for d in days:
        by_month[d["date"][:7]] = by_month.get(d["date"][:7], 0) + d["count"]
    keys = sorted(by_month)[-12:]
    top_total = max(by_month[k] for k in keys) or 1
    out = [
        f'<circle cx="{CX}" cy="{CY}" r="24" fill="#fff" fill-opacity="0.12"/>'
        f'<circle cx="{CX}" cy="{CY}" r="13" fill="#fff"/>'
    ]
    css = ["@keyframes orbit { to { transform: rotate(360deg); } }"]
    for m, k in enumerate(keys):
        r = 52 + m * 19
        size = 3 + math.sqrt(by_month[k] / top_total) * 8
        out.append(f'<circle cx="{CX}" cy="{CY}" r="{r}" fill="none" stroke="#2a2a2d" stroke-width="1"/>')
        period = 14 + m * 6
        start = -(m * 37 % period)
        out.append(
            f'<g class="pl" style="animation-duration:{period}s;animation-delay:{start}s">'
            f'<circle cx="{CX + r}" cy="{CY}" r="{size:.1f}" fill="#fff" fill-opacity="{0.45 + 0.55 * by_month[k] / top_total:.2f}"/></g>'
        )
    css.append(f".pl {{ transform-origin: {CX}px {CY}px; animation: orbit 20s linear infinite; }}")
    total = sum(by_month.values())
    return {
        "w": W, "h": H, "body": "".join(out), "defs": "", "css": " ".join(css), "foot": CY + 52 + 11 * 19 + 14, "top": CY - 52 - 11 * 19 - 14,
        "caption": f"{total:,} contributions · one planet per month, the newest on the outside",
        "title": "solar-system", "cmd": "orbit --last 12mo  # a planet for every month",
        "aria": f"Solar system with one planet for each of the last {len(keys)} months, bigger planets for busier months",
    }
