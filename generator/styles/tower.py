"""A tower with one floor per month. Wider floors and more lit windows are busier months."""
import math

from common import MONTHS, W

H = 560
FLOOR, WINDOWS = 34, 18


def render(days):
    by_month = {}
    for d in days:
        by_month.setdefault(d["date"][:7], []).append(d["count"])
    keys = sorted(by_month)[-12:]
    totals = [sum(by_month[k]) for k in keys]
    top_total = max(totals) or 1
    base = 500
    out = [f'<line x1="260" y1="{base}" x2="740" y2="{base}" stroke="#2a2a2d" stroke-width="2"/>']
    for m, k in enumerate(keys):
        y = base - (m + 1) * (FLOOR + 6)
        w = 150 + math.sqrt(totals[m] / top_total) * 250
        x = 500 - w / 2
        counts = by_month[k]
        active = sum(1 for c in counts if c)
        lit = round(active / len(counts) * WINDOWS)
        out.append(
            f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{FLOOR}" fill="#111113" stroke="#9a9aa1" stroke-width="1.2"/>'
        )
        pitch = (w - 24) / WINDOWS
        for j in range(WINDOWS):
            out.append(
                f'<rect x="{x + 12 + j * pitch:.1f}" y="{y + 10}" width="{max(2.0, pitch - 3):.1f}" height="{FLOOR - 20}" '
                f'fill="{"#fff" if j < lit else "#1b1b1e"}"/>'
            )
        out.append(f'<text x="{x - 14:.1f}" y="{y + 22}" text-anchor="end" class="dim" font-size="13">{MONTHS[int(k[5:7]) - 1]}</text>')
    total = sum(totals)
    return {
        "w": W, "h": H, "body": "".join(out), "defs": "", "foot": base + 6, "top": base - 12 * (FLOOR + 6) - 6,
        "caption": f"{total:,} contributions · one floor per month, the newest month at the top",
        "title": "tower", "cmd": "build --last 12mo  # one floor per month",
        "aria": f"Tower with a floor for each of the last {len(keys)} months, wider and brighter when busier",
    }
