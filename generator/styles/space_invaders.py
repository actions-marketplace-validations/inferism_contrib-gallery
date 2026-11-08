"""Every active day is an invader. Busier days are bigger, brighter invaders."""
import math
import random

from common import W, grid_pos, level, peak_of, starfield

H = 430
PERIOD = 9.0  # seconds for the ship to cross and come back

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
    out = []
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
    lo, hi = x0 + 22, x1 - 22
    mid = (lo + hi) / 2
    out.append(
        f'<g class="ship" transform="translate({mid:.1f} 0)"><path d="M-20 384h40v-10h-13v-9h-14v9h-13z" fill="#fff"/>'
        '<rect x="-2" y="350" width="4" height="12" fill="#fff"/></g>'
        f'<line x1="{x0}" y1="392" x2="{x1}" y2="392" stroke="#2a2a2d" stroke-width="2"/>'
    )
    # the ship swings left and right on a sine curve (it starts at the middle); a shot leaves it
    # whenever it passes under one of a few invaders, once on the way right and once on the way back
    quarter = PERIOD / 4
    shots = []
    for tx, ty in rnd.sample(hits, min(3, len(hits))):
        tx = min(hi, max(lo, tx))
        t = PERIOD / math.tau * math.acos(1 - 2 * (tx - lo) / (hi - lo))
        shots += [(tx, ty, t), (tx, ty, PERIOD - t)]
    css = [
        ".ship { animation: sweep " + f"{PERIOD}s cubic-bezier(0.37,0,0.63,1) infinite; animation-delay: -{quarter}s; " + "}",
        f"@keyframes sweep {{ 0% {{ transform: translateX({lo:.1f}px); }} 50% {{ transform: translateX({hi:.1f}px); }} 100% {{ transform: translateX({lo:.1f}px); }} }}",
        ".shot { opacity: 0; animation: shot " + f"{PERIOD}s linear infinite; " + "}",
        "@keyframes shot { 0% { opacity: 1; transform: translateY(0); } 11% { opacity: 0; transform: translateY(var(--rise)); } 100% { opacity: 0; transform: translateY(var(--rise)); } }",
    ]
    for tx, ty, t in shots:
        fire = (t - quarter) % PERIOD
        rise = ty - 346
        out.append(
            f'<rect class="shot" x="{tx - 1.5:.1f}" y="334" width="3" height="12" fill="#fff" '
            f'style="--rise:{rise:.0f}px;animation-delay:-{(PERIOD - fire) % PERIOD:.2f}s"/>'
        )
    total = sum(d["count"] for d in days)
    active = len(hits)
    deco = (
        starfield(W, H, 9, 90, top_clear=100, left_clear=620)
        + f'<text x="972" y="46" text-anchor="end" class="hi" font-size="20" font-weight="700">SCORE {total:,}</text>'
        + f'<text x="972" y="68" text-anchor="end" class="dim" font-size="14">HI {peak}</text>'
    )
    return {
        "w": W, "h": H, "body": "".join(out), "defs": defs, "top": 100, "foot": 396, "deco": deco, "css": " ".join(css),
        "caption": f"{active} invaders · bigger invaders are busier days",
        "title": "invaders", "cmd": "shoot --last 365d  # active days are invaders",
        "aria": f"Space invaders: {active} invaders for the active days of the last year, score {total:,}",
    }
