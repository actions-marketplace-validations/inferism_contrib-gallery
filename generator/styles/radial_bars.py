"""Every day is a spoke around a circle, longer when you were busier. It starts at the top and runs clockwise."""
import math

from common import W, peak_of

H = 640
CX, CY, R0, LONG = 500, 340, 78, 190


def render(days):
    peak = peak_of(days)
    n = len(days)
    out = []
    for i, d in enumerate(days):
        a = i / n * math.tau - math.pi / 2
        c = d["count"]
        length = 4 + (c / peak) ** 0.8 * LONG if c else 4
        x1, y1 = CX + R0 * math.cos(a), CY + R0 * math.sin(a)
        x2, y2 = CX + (R0 + length) * math.cos(a), CY + (R0 + length) * math.sin(a)
        out.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{"#fff" if c else "#2a2a2d"}" '
            f'stroke-width="2.2" stroke-opacity="{0.5 + 0.5 * c / peak if c else 1:.2f}"/>'
        )
    out.append(f'<circle cx="{CX}" cy="{CY}" r="{R0 - 8}" fill="none" stroke="#2a2a2d" stroke-width="1.5"/>')
    out.append(f'<text x="{CX}" y="{CY + 8}" text-anchor="middle" class="hi" font-size="26" font-weight="700">{n}d</text>')
    total = sum(d["count"] for d in days)
    return {
        "w": W, "h": H, "body": "".join(out), "defs": "", "foot": CY + R0 + LONG + 12, "top": CY - R0 - LONG - 12,
        "caption": f"{total:,} contributions · one spoke per day, starting at the top",
        "title": "radial-bars", "cmd": "spin --last 365d  # a spoke for every day",
        "aria": f"Radial bar chart of {n} days, with longer spokes for busier days",
    }
