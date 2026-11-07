"""Every active day is an invader. Busier days are bigger, brighter invaders."""
import random

from common import W, grid_pos, level, peak_of, starfield

H = 430

A = ["00100100", "00011000", "00111100", "01011010", "11111111", "10111101", "10100101", "00011000"]
B = ["00111100", "01111110", "11111111", "11011011", "11111111", "00100100", "01011010", "10100101"]


def _sprite(rows):
    return "".join(f"M{x} {y}h1v1h-1z" for y, row in enumerate(rows) for x, c in enumerate(row) if c == "1")


def render(days):
    peak = peak_of(days)
    pos = grid_pos(days)
    weeks = max(w for w, _ in pos) + 1
    rnd = random.Random(2)
    x0, x1, top, row = 28, W - 28, 112, 26
    cw = (x1 - x0) / weeks
    defs = (
        f'<symbol id="inva" viewBox="0 0 8 8"><path d="{_sprite(A)}"/></symbol>'
        f'<symbol id="invb" viewBox="0 0 8 8"><path d="{_sprite(B)}"/></symbol>'
    )
    out = [starfield(W, H, 9, 90, top_clear=100, left_clear=620)]
    hits = []
    for d, (w, dow) in zip(days, pos):
        c = d["count"]
        x, y = x0 + w * cw + cw / 2, top + dow * row
        if not c:
            out.append(f'<rect x="{x - 1:.1f}" y="{y + 8}" width="2" height="2" fill="#fff" fill-opacity="0.16"/>')
            continue
        lv = level(c, peak)
        size = 11 + lv * 1.3
        sym = "invb" if lv >= 3 else "inva"
        out.append(
            f'<use href="#{sym}" x="{x - size / 2:.1f}" y="{y + 9 - size / 2:.1f}" width="{size:.1f}" height="{size:.1f}" '
            f'fill="#fff" fill-opacity="{0.45 + lv * 0.13:.2f}"/>'
        )
        hits.append((x, y + 9))
    ship_x = x0 + (weeks - 6) * cw
    for tx, ty in rnd.sample(hits, min(3, len(hits))):  # a few shots on the way up
        out.append(f'<line x1="{ship_x:.1f}" y1="352" x2="{tx:.1f}" y2="{ty + 8:.1f}" stroke="#fff" stroke-width="1.4" stroke-opacity="0.4" stroke-dasharray="3 7"/>')
    out.append(
        f'<path d="M{ship_x - 20:.1f} 384h40v-10h-13v-9h-14v9h-13z" fill="#fff"/>'
        f'<rect x="{ship_x - 2:.1f}" y="350" width="4" height="12" fill="#fff"/>'
        f'<line x1="{x0}" y1="392" x2="{x1}" y2="392" stroke="#2a2a2d" stroke-width="2"/>'
    )
    total = sum(d["count"] for d in days)
    active = len(hits)
    out.append(
        f'<text x="972" y="46" text-anchor="end" class="hi" font-size="20" font-weight="700">SCORE {total:,}</text>'
        f'<text x="972" y="68" text-anchor="end" class="dim" font-size="14">HI {peak}</text>'
        f'<text x="28" y="{H - 14}" class="dim" font-size="15">{active} invaders · bigger invaders are busier days</text>'
    )
    return {
        "w": W, "h": H, "body": "".join(out), "defs": defs, "top": 28,
        "title": "invaders", "cmd": "shoot --last 365d  # active days are invaders",
        "aria": f"Space invaders: {active} invaders for the active days of the last year, score {total:,}",
    }
