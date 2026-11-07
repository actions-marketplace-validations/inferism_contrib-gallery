"""A cross-section of the ground. Every week digs a shaft, deeper when busier, with a gem at the bottom."""
import math
import random

from common import W, grid_pos, peak_of

H = 470
ROWS = 15


def _rect(x, y, w, h):
    return f"M{x:.1f} {y:.1f}h{w:.1f}v{h:.1f}h{-w:.1f}z"


def render(days):
    pos = grid_pos(days)
    nw = max(w for w, _ in pos) + 1
    tot = [0] * nw
    for d, (w, _) in zip(days, pos):
        tot[w] += d["count"]
    top_week = max(tot) or 1
    rnd = random.Random(4)
    bs = (W - 56) / nw
    surf = 150

    grass, dirt_a, dirt_b, ore, gems = [], [], [], [], []
    for w in range(nw):
        x = 28 + w * bs
        depth = round(math.sqrt(tot[w] / top_week) * (ROWS - 2)) if tot[w] else 0
        for r in range(ROWS):
            y = surf + r * bs
            if r < depth:
                continue  # dug out
            if r == depth and depth:
                gems.append(_rect(x + 1.5, y + 1.5, bs - 3, bs - 3))  # the find at the bottom of the shaft
            elif r == 0:
                grass.append(_rect(x + 0.5, y + 0.5, bs - 1, bs - 1))
            elif rnd.random() < 0.05:
                ore.append(_rect(x + 0.5, y + 0.5, bs - 1, bs - 1))
            else:
                (dirt_a if (w + r) % 2 else dirt_b).append(_rect(x + 0.5, y + 0.5, bs - 1, bs - 1))

    def layer(paths, opacity):
        return f'<path d="{"".join(paths)}" fill="#fff" fill-opacity="{opacity}"/>' if paths else ""

    out = [
        layer(dirt_b, 0.09), layer(dirt_a, 0.15), layer(ore, 0.45), layer(grass, 0.8), layer(gems, 1.0),
        f'<line x1="28" y1="{surf + ROWS * bs + 4:.1f}" x2="{W - 28}" y2="{surf + ROWS * bs + 4:.1f}" stroke="#2a2a2d" stroke-width="2"/>',
    ]
    dug = sum(1 for t in tot if t)
    total = sum(d["count"] for d in days)
    return {
        "w": W, "h": H, "body": "".join(out), "defs": "", "foot": round(surf + ROWS * bs + 6), "top": 140,
        "caption": f"{dug} shafts dug · {total:,} contributions · deeper shafts are busier weeks",
        "title": "dig-site", "cmd": "dig --last 365d  # a shaft for every active week",
        "aria": f"Cross-section of the ground with {dug} shafts, one for each active week, deeper when busier",
    }
