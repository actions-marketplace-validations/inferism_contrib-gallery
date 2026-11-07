"""A terrain mesh: weeks run left to right, weekdays go into the distance, height is how busy."""
import math

from common import W, grid_pos, peak_of

H = 510
SUB = 3  # extra rows between weekdays, for a smooth surface


def render(days):
    peak = peak_of(days)
    pos = grid_pos(days)
    nw = max(w for w, _ in pos) + 1
    val = [[0.0] * 7 for _ in range(nw)]
    for d, (w, dow) in zip(days, pos):
        val[w][dow] = d["count"]
    sm = [  # light smoothing along the weeks
        [(val[max(0, w - 1)][r] + 2 * val[w][r] + val[min(nw - 1, w + 1)][r]) / 4 for r in range(7)]
        for w in range(nw)
    ]

    dxw, dyw, dxr, dyr, ox, oy = 14.2, 1.2, -24.0, 22.0, 200.0, 262.0

    def height(w, r):
        a = int(r)
        b = min(6, a + 1)
        f = r - a
        v = sm[w][a] * (1 - f) + sm[w][b] * f
        return math.sqrt(v / peak) * 118

    def point(w, r):
        return ox + w * dxw + r * dxr, oy + w * dyw + r * dyr - height(w, r)

    out = []
    prev = None
    rows = [i / SUB for i in range(6 * SUB + 1)]
    for ri, r in enumerate(rows):
        pts = [point(w, r) for w in range(nw)]
        line = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
        out.append(f'<path d="{line}L{pts[-1][0]:.1f} {H}L{pts[0][0]:.1f} {H}Z" fill="#050507"/>')
        if prev:  # ribs between this row and the one behind it
            ribs = "".join(
                f"M{prev[w][0]:.1f} {prev[w][1]:.1f}L{pts[w][0]:.1f} {pts[w][1]:.1f}" for w in range(0, nw, 3)
            )
            out.append(f'<path d="{ribs}" fill="none" stroke="#fff" stroke-width="0.7" stroke-opacity="0.22"/>')
        out.append(
            f'<path d="{line}" fill="none" stroke="#fff" stroke-width="1.1" '
            f'stroke-opacity="{0.3 + 0.6 * ri / len(rows):.2f}" stroke-linejoin="round"/>'
        )
        prev = pts
    total = sum(d["count"] for d in days)
    out.append(f'<text x="28" y="{H - 22}" class="dim" font-size="15">{total:,} contributions · peak {peak}/day · higher ground is a busier day</text>')
    return {
        "w": W, "h": H, "body": "".join(out), "defs": "",
        "title": "terrain", "cmd": "render-terrain --last 365d  # height is how busy",
        "aria": f"Terrain mesh of {total:,} contributions over the last year, peak {peak} in a day",
    }
