"""A sandbox world: every day is a column of blocks, and busier days are taller towers."""
import math

from common import W, grid_pos, level, peak_of

H = 600
CUBE = 9  # height of one block in px
TOP = [0.14, 0.28, 0.48, 0.72, 1.0]  # how bright the top of a column is at each level


def render(days):
    peak = peak_of(days)
    pos = grid_pos(days)
    dx, dy, ox, oy, m = 14.0, 7.0, 190.0, 150.0, 0.04

    def p(a, b, z):
        return f"{ox + (a - b) * dx:.1f},{oy + (a + b) * dy - z:.1f}"

    cells = []
    for d, (gx, gy) in zip(days, pos):
        c = d["count"]
        blocks = 1 + (round(math.sqrt(c / peak) * 7) if c else 0)  # the ground is always one block
        cells.append((gx + gy, gx, gy, level(c, peak), blocks))
    cells.sort()

    out = []
    for _, gx, gy, lv, n in cells:
        a0, a1, b0, b1 = gx + m, gx + 1 - m, gy + m, gy + 1 - m
        h = n * CUBE
        left = f"M{p(a0, b1, 0)}L{p(a1, b1, 0)}L{p(a1, b1, h)}L{p(a0, b1, h)}Z"
        right = f"M{p(a1, b1, 0)}L{p(a1, b0, 0)}L{p(a1, b0, h)}L{p(a1, b1, h)}Z"
        roof = f"M{p(a0, b0, h)}L{p(a1, b0, h)}L{p(a1, b1, h)}L{p(a0, b1, h)}Z"
        t = TOP[lv]
        for shape, k in ((left, 0.55), (right, 0.35), (roof, 1.0)):
            out.append(f'<path d="{shape}" fill="#050507"/><path d="{shape}" fill="#fff" fill-opacity="{max(0.06, t * k):.2f}"/>')
        if n > 1:  # the seams between the blocks of a tower
            seams = "".join(
                f"M{p(a0, b1, z * CUBE)}L{p(a1, b1, z * CUBE)}L{p(a1, b0, z * CUBE)}" for z in range(1, n)
            )
            out.append(f'<path d="{seams}" fill="none" stroke="#050507" stroke-width="0.8" stroke-opacity="0.65"/>')

    total = sum(d["count"] for d in days)
    sun = (
        '<rect x="842" y="96" width="38" height="38" fill="#fff" fill-opacity="0.9"/>'
        '<rect x="700" y="120" width="70" height="16" fill="#fff" fill-opacity="0.1"/>'
        '<rect x="722" y="104" width="40" height="16" fill="#fff" fill-opacity="0.1"/>'
        '<rect x="260" y="92" width="76" height="16" fill="#fff" fill-opacity="0.1"/>'
        '<rect x="282" y="76" width="40" height="16" fill="#fff" fill-opacity="0.1"/>'
    )
    return {
        "w": W, "h": H, "body": "".join(out), "defs": "", "deco": sun, "foot": 574, "top": 130,
        "caption": f"{total:,} contributions · one column per day · taller towers are busier days",
        "title": "block-world", "cmd": "build --last 365d  # one column per day",
        "aria": f"Block world of {total:,} contributions: one column of blocks per day, taller when busier",
    }
