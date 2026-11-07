"""One jagged line per month, stacked on black. Peaks are busy days."""
import random

from common import MONTHS, W, peak_of

H = 580


def render(days):
    peak = peak_of(days)
    rnd = random.Random(14)
    per = len(days) // 12
    out = []
    for m in range(12):
        chunk = days[m * per:(m + 1) * per]
        base = 150 + m * 32
        pts = []
        for k, d in enumerate(chunk):
            x = 76 + k / max(1, len(chunk) - 1) * (W - 104)
            c = d["count"]
            pts.append((x, base - (c / peak * 62 + rnd.random() * 3 if c else rnd.random() * 1.4)))
        line = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
        label = MONTHS[int(chunk[0]["date"][5:7]) - 1]
        out.append(
            f'<path d="{line} L{W - 28} {base + 40} L76 {base + 40} Z" fill="#08080a"/>'
            f'<path d="{line}" fill="none" stroke="#fff" stroke-width="1.2" stroke-opacity="{0.45 + m / 12 * 0.5:.2f}"/>'
            f'<text x="28" y="{base + 4}" class="dim" font-size="13">{label}</text>'
        )
    total = sum(d["count"] for d in days)
    return {
        "w": W, "h": H, "body": "".join(out), "defs": "", "foot": 548, "top": 80,
        "caption": f"{total:,} contributions · peak {peak}/day · one line per month",
        "title": "ridgeline", "cmd": "render-ridges --last 365d  # one line per month",
        "aria": f"Ridgeline chart of {total:,} contributions, one line per month",
    }
