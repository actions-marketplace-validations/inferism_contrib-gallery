"""Your year as a product barcode: one bar per day, thicker when you were busier."""
from common import W, level, peak_of

H = 300
X0, X1, Y0, BAR_H = 28, W - 28, 100, 130


def render(days):
    peak = peak_of(days)
    n = len(days)
    step = (X1 - X0) / n
    out = []
    for i, d in enumerate(days):
        c = d["count"]
        lv = level(c, peak)
        w = step * (0.3 + lv * 0.17) if c else max(0.5, step * 0.12)
        out.append(f'<rect x="{X0 + i * step:.2f}" y="{Y0}" width="{w:.2f}" height="{BAR_H}" fill="#fff" fill-opacity="{1 if c else 0.28}"/>')
    total = sum(d["count"] for d in days)
    out.append(f'<text x="{W / 2}" y="{Y0 + BAR_H + 30}" text-anchor="middle" class="hi" font-size="18" letter-spacing="8">{total:08d}</text>')
    return {
        "w": W, "h": H, "body": "".join(out), "defs": "", "foot": Y0 + BAR_H + 40, "top": 90,
        "caption": f"one bar per day · thick bars are active days",
        "title": "barcode", "cmd": "scan --last 365d",
        "aria": f"Barcode of {n} days with {total:,} contributions, thicker bars for busier days",
    }
