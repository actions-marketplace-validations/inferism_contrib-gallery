"""A 3D city floating in space: one building per day, taller and brighter when you were busier."""
import math

from common import W, grid_pos, level, peak_of, starfield

H = 610
TOP = [0.10, 0.22, 0.45, 0.75, 1.0]  # how bright the roof of each level is


def render(days):
    peak = peak_of(days)
    pos = grid_pos(days)
    dx, dy, ox, oy, m = 15.0, 6.2, 155.0, 190.0, 0.07

    def p(a, b, z):
        return f"{ox + (a - b) * dx:.1f},{oy + (a + b) * dy - z:.1f}"

    cells = []
    for d, (gx, gy) in zip(days, pos):
        c = d["count"]
        lv = level(c, peak)
        cells.append((gx + gy, gx, gy, lv, 3.0 if not c else 10 + 110 * math.sqrt(c / peak)))
    cells.sort()

    out = [
        starfield(W, H, 7, 190),
        '<g transform="translate(880 168) rotate(-18)">'
        '<ellipse rx="62" ry="12" fill="none" stroke="#fff" stroke-opacity="0.35" stroke-width="2"/>'
        '<circle r="30" fill="#111113"/><circle r="30" fill="url(#planet)"/>'
        '<path d="M-62 0A62 12 0 0 0 62 0" fill="none" stroke="#fff" stroke-opacity="0.55" stroke-width="2"/></g>',
    ]
    for _, gx, gy, lv, h in cells:
        a0, a1, b0, b1 = gx + m, gx + 1 - m, gy + m, gy + 1 - m
        roof = f"M{p(a0, b0, h)}L{p(a1, b0, h)}L{p(a1, b1, h)}L{p(a0, b1, h)}Z"
        if lv == 0:  # an empty day is a flat tile
            out.append(f'<path d="{roof}" fill="#050507"/><path d="{roof}" fill="#fff" fill-opacity="0.07"/>')
            continue
        left = f"M{p(a0, b1, 0)}L{p(a1, b1, 0)}L{p(a1, b1, h)}L{p(a0, b1, h)}Z"
        right = f"M{p(a1, b1, 0)}L{p(a1, b0, 0)}L{p(a1, b0, h)}L{p(a1, b1, h)}Z"
        t = TOP[lv]
        for shape, k in ((left, 0.62), (right, 0.38), (roof, 1.0)):
            out.append(f'<path d="{shape}" fill="#050507"/><path d="{shape}" fill="#fff" fill-opacity="{t * k:.2f}"/>')
    total = sum(d["count"] for d in days)
    out.append(f'<text x="28" y="{H - 22}" class="dim" font-size="15">{total:,} contributions · peak {peak}/day · one building per day</text>')
    return {
        "w": W, "h": H, "body": "".join(out),
        "defs": '<radialGradient id="planet" cx="0.3" cy="0.3" r="0.8"><stop offset="0" stop-color="#fff" stop-opacity="0.5"/><stop offset="1" stop-color="#fff" stop-opacity="0.02"/></radialGradient>',
        "title": "skyline", "cmd": "render-skyline --last 365d  # one building per day",
        "aria": f"3D skyline of {total:,} contributions over the last year, peak {peak} in a day",
    }
