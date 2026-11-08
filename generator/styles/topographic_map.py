"""A topographic map: contour lines rise around the weeks you were busiest."""
import math

from common import W, grid_pos

H = 500
CELL, SIGMA = 8, 34
X0, X1, Y0, Y1 = 28, W - 28, 100, 440
LEVELS = [0.05, 0.13, 0.25, 0.4, 0.6, 0.82]
# marching squares: for each corner pattern, which pairs of cell edges the contour joins (0 top, 1 right, 2 bottom, 3 left)
SEGMENTS = {
    1: [(3, 2)], 2: [(2, 1)], 3: [(3, 1)], 4: [(0, 1)], 5: [(0, 3), (1, 2)], 6: [(0, 2)], 7: [(0, 3)],
    8: [(0, 3)], 9: [(0, 2)], 10: [(0, 1), (2, 3)], 11: [(0, 1)], 12: [(3, 1)], 13: [(2, 1)], 14: [(3, 2)],
}


def render(days):
    pos = grid_pos(days)
    weeks = max(w for w, _ in pos) + 1
    pts = [
        (X0 + w / max(1, weeks - 1) * (X1 - X0), Y0 + 20 + dow / 6 * (Y1 - Y0 - 40), d["count"])
        for d, (w, dow) in zip(days, pos) if d["count"]
    ]
    gw, gh = int((X1 - X0) / CELL), int((Y1 - Y0) / CELL)
    field = [[0.0] * (gw + 1) for _ in range(gh + 1)]
    peak = 0.0
    reach = (SIGMA * 3) ** 2
    for j in range(gh + 1):
        for i in range(gw + 1):
            x, y = X0 + i * CELL, Y0 + j * CELL
            v = 0.0
            for px, py, c in pts:
                dd = (x - px) ** 2 + (y - py) ** 2
                if dd < reach:
                    v += c * math.exp(-dd / (2 * SIGMA * SIGMA))
            field[j][i] = v
            peak = max(peak, v)
    out = []
    for li, level in enumerate(LEVELS):
        th = level * peak
        path = []
        for j in range(gh):
            for i in range(gw):
                tl, tr, br, bl = field[j][i], field[j][i + 1], field[j + 1][i + 1], field[j + 1][i]
                idx = (8 if tl > th else 0) | (4 if tr > th else 0) | (2 if br > th else 0) | (1 if bl > th else 0)
                if idx not in SEGMENTS:
                    continue
                x, y = X0 + i * CELL, Y0 + j * CELL
                edge = [
                    (x + CELL * (th - tl) / (tr - tl), y), (x + CELL, y + CELL * (th - tr) / (br - tr)),
                    (x + CELL * (th - bl) / (br - bl), y + CELL), (x, y + CELL * (th - tl) / (bl - tl)),
                ]
                for a, b in SEGMENTS[idx]:
                    path.append(f"M{edge[a][0]:.1f} {edge[a][1]:.1f}L{edge[b][0]:.1f} {edge[b][1]:.1f}")
        out.append(
            f'<path d="{"".join(path)}" fill="none" stroke="#fff" stroke-width="{1.4 if li > 3 else 0.9}" '
            f'stroke-opacity="{0.25 + li * 0.13:.2f}" stroke-linecap="round"/>'
        )
    total = sum(d["count"] for d in days)
    return {
        "w": W, "h": H, "body": "".join(out), "defs": "", "foot": Y1 + 12, "top": Y0 - 6,
        "caption": f"{total:,} contributions · closer lines mean busier ground",
        "title": "topographic-map", "cmd": "survey --last 365d  # contour lines of activity",
        "aria": f"Topographic map with contour lines around the busiest weeks, {total:,} contributions in all",
    }
