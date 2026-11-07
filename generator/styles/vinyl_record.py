"""A record: one ring of grooves per month, and every active day is a blip along its ring."""
import math

from common import W, level, peak_of

H = 580


def _arc(cx, cy, r, a0, a1):
    x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
    x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
    return f"M{x0:.1f} {y0:.1f}A{r} {r} 0 0 1 {x1:.1f} {y1:.1f}"


def render(days):
    peak = peak_of(days)
    cx, cy = 500, 318
    by_month = {}
    for d in days:
        by_month.setdefault(d["date"][:7], []).append(d)
    keys = sorted(by_month)[-12:]
    total = sum(d["count"] for d in days)

    out = [
        f'<circle cx="{cx}" cy="{cy}" r="238" fill="#111113" stroke="#2a2a2d" stroke-width="2"/>',
        f'<circle cx="{cx}" cy="{cy}" r="226" fill="none" stroke="#2a2a2d" stroke-width="1"/>',
    ]
    for m, k in enumerate(keys):
        r = 112 + m * 10.4
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#2a2a2d" stroke-width="0.8"/>')
        n = len(by_month[k])
        for i, d in enumerate(by_month[k]):
            if not d["count"]:
                continue
            lv = level(d["count"], peak)
            a0 = i / n * math.tau - math.pi / 2
            out.append(
                f'<path d="{_arc(cx, cy, r, a0, a0 + math.tau / n * 0.72)}" fill="none" stroke="#fff" '
                f'stroke-width="{2.2 + lv * 0.5:.1f}" stroke-linecap="round" stroke-opacity="{0.35 + lv * 0.16:.2f}"/>'
            )
    out.append(f'<circle cx="{cx}" cy="{cy}" r="72" fill="#111113" stroke="#2a2a2d" stroke-width="2"/>')
    out.append(f'<text x="{cx}" y="{cy + 4}" text-anchor="middle" class="hi" font-size="30" font-weight="700">{total:,}</text>')
    out.append(f'<text x="{cx}" y="{cy + 26}" text-anchor="middle" class="dim" font-size="13">contributions</text>')
    # tonearm
    out.append(
        '<circle cx="884" cy="150" r="18" fill="#111113" stroke="#2a2a2d" stroke-width="2"/>'
        '<path d="M910 140L884 150L694 214" fill="none" stroke="#d4d4d8" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
        '<rect x="672" y="206" width="28" height="12" rx="2" transform="rotate(-18.5 686 212)" fill="#fff"/>'
    )
    out.append(f'<text x="28" y="{H - 22}" class="dim" font-size="15">one ring per month · peak {peak}/day</text>')
    return {
        "w": W, "h": H, "body": "".join(out), "defs": "",
        "title": "vinyl-record", "cmd": "play --last 365d  # one groove per month",
        "aria": f"Vinyl record with a ring of grooves for each month and {total:,} contributions in the last year",
    }
