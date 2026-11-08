"""The whole year as one smooth line, with the busiest week and today marked."""
from common import MONTHS, W, grid_pos

H = 300
BASE, SCALE = 240, 150


def _smooth(vals, passes=2):
    for _ in range(passes):
        vals = [(vals[max(0, i - 1)] + 2 * vals[i] + vals[min(len(vals) - 1, i + 1)]) / 4 for i in range(len(vals))]
    return vals


def render(days):
    pos = grid_pos(days)
    nw = max(w for w, _ in pos) + 1
    tot = [0] * nw
    for d, (w, _) in zip(days, pos):
        tot[w] += d["count"]
    sm = _smooth([float(t) for t in tot], 2)
    top = max(sm) or 1
    x0, x1 = 28, W - 28
    pts = [(x0 + i / max(1, nw - 1) * (x1 - x0), BASE - v / top * SCALE) for i, v in enumerate(sm)]
    line = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        line += f"Q{xa:.1f} {ya:.1f} {(xa + xb) / 2:.1f} {(ya + yb) / 2:.1f}"
    line += f"L{pts[-1][0]:.1f} {pts[-1][1]:.1f}"
    out = [
        f'<path d="{line}L{x1} {BASE}L{x0} {BASE}Z" fill="#fff" fill-opacity="0.09"/>',
        f'<line x1="{x0}" y1="{BASE}" x2="{x1}" y2="{BASE}" stroke="#2a2a2d" stroke-width="2"/>',
        f'<path d="{line}" fill="none" stroke="#fff" stroke-width="2.4" stroke-linejoin="round"/>',
    ]
    n = len(days)
    for i, d in enumerate(days):  # a tick and a label where each month starts
        if d["date"][8:10] == "01":
            x = x0 + i / max(1, n - 1) * (x1 - x0)
            out.append(
                f'<line x1="{x:.1f}" y1="{BASE}" x2="{x:.1f}" y2="{BASE + 8}" stroke="#9a9aa1" stroke-width="1.5"/>'
                f'<text x="{x + 4:.1f}" y="{BASE + 24}" class="dim" font-size="13">{MONTHS[int(d["date"][5:7]) - 1]}</text>'
            )
    k = sm.index(max(sm))
    px, py = pts[k]
    out.append(
        f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5" fill="#fff"/>'
        f'<text x="{px + 12:.1f}" y="{py + 5:.1f}" class="hi" font-size="14">busiest week</text>'
        f'<circle cx="{pts[-1][0]:.1f}" cy="{pts[-1][1]:.1f}" r="9" fill="#fff" fill-opacity="0.25"/>'
        f'<circle cx="{pts[-1][0]:.1f}" cy="{pts[-1][1]:.1f}" r="4.5" fill="#fff"/>'
    )
    total = sum(d["count"] for d in days)
    return {
        "w": W, "h": H, "body": "".join(out), "defs": "", "foot": BASE + 32, "top": 70,
        "caption": f"{total:,} contributions · weekly totals, smoothed · the dot on the right is this week",
        "title": "year-sparkline", "cmd": "plot --weekly --last 365d",
        "aria": f"Line chart of weekly contributions over the last year, {total:,} in total",
    }
