"""One wave per month, stacked in the sea. Taller swells are busier days."""
import math

from common import MONTHS, W, peak_of

H = 580
POINTS = 80


def _smooth(vals, passes=3):
    for _ in range(passes):
        vals = [(vals[max(0, i - 1)] + 2 * vals[i] + vals[min(len(vals) - 1, i + 1)]) / 4 for i in range(len(vals))]
    return vals


def render(days):
    peak = peak_of(days)
    by_month = {}
    for d in days:
        by_month.setdefault(d["date"][:7], []).append(d["count"])
    keys = sorted(by_month)[-12:]
    x0, x1 = 28, W - 28
    out = [
        '<circle cx="840" cy="150" r="44" fill="#fff" fill-opacity="0.12"/>'
        '<circle cx="840" cy="150" r="30" fill="#fff" fill-opacity="0.9"/>'
    ]
    for m, k in enumerate(keys):
        counts = by_month[k]
        base = 190 + m * 29
        res = []
        for i in range(POINTS):  # stretch the month across the full width
            j = i / (POINTS - 1) * (len(counts) - 1)
            a = int(j)
            b = min(len(counts) - 1, a + 1)
            res.append(counts[a] * (1 - (j - a)) + counts[b] * (j - a))
        res = _smooth(res)
        pts = [
            (x0 + i / (POINTS - 1) * (x1 - x0), base - math.sqrt(v / peak) * 62 + math.sin(i / 5 + m) * 3)
            for i, v in enumerate(res)
        ]
        d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
        for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
            d += f"Q{xa:.1f} {ya:.1f} {(xa + xb) / 2:.1f} {(ya + yb) / 2:.1f}"
        d += f"L{x1} {pts[-1][1]:.1f}"
        shape = f"{d}L{x1} {H}L{x0} {H}Z"
        out.append(
            f'<path d="{shape}" fill="#050507"/>'
            f'<path d="{shape}" fill="#fff" fill-opacity="{0.04 + m * 0.012:.3f}"/>'
            f'<path d="{d}" fill="none" stroke="#fff" stroke-width="1.4" stroke-opacity="{0.3 + m * 0.055:.2f}"/>'
            f'<text x="34" y="{base + 18}" class="dim" font-size="13">{MONTHS[int(k[5:7]) - 1]}</text>'
        )
    total = sum(d["count"] for d in days)
    out.append(f'<text x="28" y="{H - 22}" class="dim" font-size="15">{total:,} contributions · one wave per month · front waves are the newest</text>')
    return {
        "w": W, "h": H, "body": "".join(out), "defs": "",
        "title": "ocean", "cmd": "swell --last 365d  # one wave per month",
        "aria": f"Ocean waves, one wave per month, for {total:,} contributions in the last year",
    }
