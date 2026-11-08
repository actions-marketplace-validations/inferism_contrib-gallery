"""A heartbeat monitor: a spike for every active day, with a bright pulse that keeps scanning along it."""
from common import W, peak_of

H = 300
X0, X1, BASE, SCALE = 28, W - 28, 215, 140


def render(days):
    peak = peak_of(days)
    n = len(days)
    d = f"M{X0} {BASE}"
    for i, day in enumerate(days):
        x = X0 + i / max(1, n - 1) * (X1 - X0)
        c = day["count"]
        y = BASE - (10 + (c / peak) ** 0.8 * SCALE) if c else BASE
        d += f"L{x:.1f} {y:.1f}L{x + 0.9:.1f} {BASE}"
    d += f"L{X1} {BASE}"
    body = (
        f'<line x1="{X0}" y1="{BASE}" x2="{X1}" y2="{BASE}" stroke="#2a2a2d" stroke-width="2"/>'
        f'<path d="{d}" fill="none" stroke="#fff" stroke-opacity="0.7" stroke-width="1.3"/>'
        f'<path class="scan" pathLength="100" d="{d}" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"/>'
    )
    css = (
        ".scan { stroke-dasharray: 6 94; animation: scan 3.4s linear infinite; } "
        "@keyframes scan { from { stroke-dashoffset: 6; } to { stroke-dashoffset: -94; } }"
    )
    total = sum(x["count"] for x in days)
    return {
        "w": W, "h": H, "body": body, "defs": "", "css": css, "foot": BASE + 14, "top": 70,
        "caption": f"{total:,} contributions · one spike per active day",
        "title": "pulse-line", "cmd": "monitor --last 365d  # a heartbeat for every active day",
        "aria": f"Heartbeat monitor with a spike for each active day of the last year, {total:,} contributions in all",
    }
