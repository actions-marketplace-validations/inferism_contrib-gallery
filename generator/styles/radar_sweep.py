"""A radar: a scan line sweeps around and lights up the days it passes. Weeks go around, weekdays go outward."""
import math

from common import W, grid_pos, level, peak_of

H = 580
CX, CY = 500, 310
PERIOD = 9.0


def render(days):
    peak = peak_of(days)
    pos = grid_pos(days)
    weeks = max(w for w, _ in pos) + 1
    out = []
    for d in range(7):
        out.append(f'<circle cx="{CX}" cy="{CY}" r="{60 + d * 30}" fill="none" stroke="#2a2a2d" stroke-width="1"/>')
    out.append(
        f'<line x1="{CX - 250}" y1="{CY}" x2="{CX + 250}" y2="{CY}" stroke="#2a2a2d" stroke-width="1"/>'
        f'<line x1="{CX}" y1="{CY - 250}" x2="{CX}" y2="{CY + 250}" stroke="#2a2a2d" stroke-width="1"/>'
    )
    for day, (w, dow) in zip(days, pos):
        c = day["count"]
        if not c:
            continue
        a = w / weeks * math.tau
        r = 60 + dow * 30
        lv = level(c, peak)
        out.append(
            f'<circle class="ping" cx="{CX + r * math.cos(a):.1f}" cy="{CY + r * math.sin(a):.1f}" r="{2 + lv * 0.9:.1f}" fill="#fff" '
            f'style="animation-delay:{a / math.tau * PERIOD:.2f}s"/>'
        )
    out.append(
        f'<g class="sweep"><path d="M{CX} {CY}L{CX + 250} {CY}A250 250 0 0 0 {CX + 250 * math.cos(-0.5):.1f} {CY + 250 * math.sin(-0.5):.1f}Z" fill="#fff" fill-opacity="0.08"/>'
        f'<line x1="{CX}" y1="{CY}" x2="{CX + 250}" y2="{CY}" stroke="#fff" stroke-width="2"/></g>'
    )
    css = (
        f".sweep {{ transform-origin: {CX}px {CY}px; animation: spin {PERIOD}s linear infinite; }} "
        "@keyframes spin { to { transform: rotate(360deg); } } "
        f".ping {{ opacity: 0.18; animation: ping {PERIOD}s linear infinite; }} "
        "@keyframes ping { 0% { opacity: 1; } 100% { opacity: 0.18; } }"
    )
    total = sum(d["count"] for d in days)
    return {
        "w": W, "h": H, "body": "".join(out), "defs": "", "css": css, "foot": CY + 258, "top": CY - 258,
        "caption": f"{total:,} contributions · the scan line lights up each active day",
        "title": "radar-sweep", "cmd": "scan --last 365d  # weeks go around, weekdays go outward",
        "aria": "A radar sweep that lights up each active day of the last year as the scan line passes",
    }
