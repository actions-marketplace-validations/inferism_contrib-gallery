"""Northern lights: curtains of light that swell in the weeks you were busy."""
import math

from common import W, grid_pos, starfield

H = 540
RIBBONS = 5


def _smooth(vals, passes=2):
    for _ in range(passes):
        vals = [(vals[max(0, i - 1)] + 2 * vals[i] + vals[min(len(vals) - 1, i + 1)]) / 4 for i in range(len(vals))]
    return vals


def render(days):
    pos = grid_pos(days)
    nw = max(w for w, _ in pos) + 1
    tot = [0.0] * nw
    for d, (w, _) in zip(days, pos):
        tot[w] += d["count"]
    top_week = max(tot) or 1
    sm = _smooth([t / top_week for t in tot])
    x0, x1 = 28, W - 28
    out = []
    for k in range(RIBBONS):
        base = 330 - k * 30
        amp = 190 - k * 20
        pts = []
        for i, v in enumerate(sm):
            x = x0 + i / max(1, nw - 1) * (x1 - x0)
            y = base - 24 - math.sqrt(v) * amp + math.sin(i * 0.33 + k * 1.1) * 14
            pts.append((x, y))
        top = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
        for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
            top += f"Q{xa:.1f} {ya:.1f} {(xa + xb) / 2:.1f} {(ya + yb) / 2:.1f}"
        top += f"L{x1} {pts[-1][1]:.1f}"
        out.append(f'<path d="{top}L{x1} 470L{x0} 470Z" fill="url(#aurora)" fill-opacity="{0.34 - k * 0.055:.2f}"/>')
        rays = "".join(f"M{x:.1f} {y:.1f}V{y + 90 + (i % 4) * 26}" for i, (x, y) in enumerate(pts))
        out.append(f'<path d="{rays}" fill="none" stroke="#fff" stroke-width="1.2" stroke-opacity="{0.32 - k * 0.05:.2f}"/>')
    out.append(f'<path d="{top}" fill="none" stroke="#fff" stroke-width="1.4" stroke-opacity="0.5"/>')
    total = sum(d["count"] for d in days)
    return {
        "w": W, "h": H, "body": "".join(out), "deco": starfield(W, H, 12, 170), "foot": 440, "top": 90,
        "defs": '<linearGradient id="aurora" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0.9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>',
        "caption": f"{total:,} contributions · taller curtains are busier weeks",
        "title": "aurora", "cmd": "shimmer --last 365d  # curtains of light, taller when busier",
        "aria": f"Aurora of {total:,} contributions: curtains of light that rise in the busiest weeks",
    }
