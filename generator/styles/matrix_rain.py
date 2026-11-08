"""Falling code: one column per week, rainier and brighter in the weeks you were busy."""
import random

from common import W, grid_pos

H = 500
CHARS = "01<>/{}[]$#=+*"
RAIN = 16


def render(days):
    pos = grid_pos(days)
    nw = max(w for w, _ in pos) + 1
    tot = [0] * nw
    for d, (w, _) in zip(days, pos):
        tot[w] += d["count"]
    top_week = max(tot) or 1
    rnd = random.Random(14)
    pitch = (W - 56) / nw
    out = []
    for w in range(nw):
        x = 28 + w * pitch + pitch / 2
        heat = tot[w] / top_week
        dur, delay = 4.5 + rnd.random() * 5, -rnd.random() * 9
        glyphs = []
        for k in range(RAIN):
            fade = (k + 1) / RAIN
            op = (0.12 + 0.88 * fade) * (0.3 + 0.7 * heat)
            glyphs.append(
                f'<text x="{x:.1f}" y="{k * 17}" text-anchor="middle" class="hi" font-size="15" fill-opacity="{op:.2f}">'
                f'{rnd.choice(CHARS).replace("<", "&lt;").replace(">", "&gt;")}</text>'
            )
        out.append(f'<g class="rain" style="animation-duration:{dur:.2f}s;animation-delay:{delay:.2f}s">{"".join(glyphs)}</g>')
    css = (
        ".rain { animation: rain 7s linear infinite; } "
        f"@keyframes rain {{ from {{ transform: translateY(-{RAIN * 17}px); }} to {{ transform: translateY({H - 20}px); }} }}"
    )
    total = sum(tot)
    return {
        "w": W, "h": H, "body": "".join(out), "defs": "", "css": css, "foot": H - 20, "top": 90,
        "caption": f"{total:,} contributions · brighter columns are busier weeks",
        "title": "matrix-rain", "cmd": "decode --last 52w  # a column for every week",
        "aria": f"Falling code with a column for each of the {nw} weeks, brighter for busier weeks",
    }
