"""A falling-block puzzle: one column per month, stacked as high as the month was busy."""
from common import MONTHS, W, month_totals

H = 580
COLS, ROWS, CELL = 12, 20, 22
WX, WY = (W - COLS * CELL) // 2, 100
SHADE = [0.38, 0.55, 0.75, 0.95]


def _block(x, y, op):
    return f'<rect x="{x + 1}" y="{y + 1}" width="{CELL - 2}" height="{CELL - 2}" fill="#fff" fill-opacity="{op}"/>'


def render(days):
    rows = month_totals(days, COLS)
    mx = max(v for _, v in rows) or 1
    total = sum(d["count"] for d in days)
    active_months = sum(1 for _, v in rows if v)
    out = [f'<rect x="{WX}" y="{WY}" width="{COLS * CELL}" height="{ROWS * CELL}" fill="none" stroke="#2a2a2d" stroke-width="2"/>']
    grid = "".join(f"M{WX + i * CELL} {WY}v{ROWS * CELL}" for i in range(1, COLS))
    grid += "".join(f"M{WX} {WY + j * CELL}h{COLS * CELL}" for j in range(1, ROWS))
    out.append(f'<path d="{grid}" fill="none" stroke="#2a2a2d" stroke-width="0.6" stroke-opacity="0.7"/>')
    for i, (key, v) in enumerate(rows):
        height = round(v / mx * (ROWS - 4))
        x = WX + i * CELL
        for r in range(height):
            out.append(_block(x, WY + (ROWS - 1 - r) * CELL, SHADE[(i * 3 + r * 5) % 4]))
        out.append(
            f'<text x="{x + CELL / 2}" y="{WY + ROWS * CELL + 20}" text-anchor="middle" class="dim" font-size="11">{MONTHS[int(key[5:7]) - 1][0]}</text>'
        )
    for dx, dy in ((4, 1), (5, 1), (6, 1), (5, 2)):  # a piece on its way down
        out.append(_block(WX + dx * CELL, WY + dy * CELL, 1.0))

    out.append(
        '<text x="60" y="150" class="dim" font-size="14" letter-spacing="2">SCORE</text>'
        f'<text x="60" y="184" class="hi" font-size="34" font-weight="700">{total:,}</text>'
        '<text x="60" y="236" class="dim" font-size="14" letter-spacing="2">LEVEL</text>'
        f'<text x="60" y="270" class="hi" font-size="34" font-weight="700">{active_months}</text>'
        '<text x="60" y="322" class="dim" font-size="14" letter-spacing="2">LINES</text>'
        f'<text x="60" y="356" class="hi" font-size="34" font-weight="700">{sum(1 for d in days if d["count"])}</text>'
    )
    nx, ny = WX + COLS * CELL + 70, 150
    out.append(f'<text x="{nx}" y="{ny - 14}" class="dim" font-size="14" letter-spacing="2">NEXT</text>')
    out.append(f'<rect x="{nx}" y="{ny}" width="{CELL * 4 + 20}" height="{CELL * 3 + 20}" fill="none" stroke="#2a2a2d" stroke-width="2"/>')
    for dx, dy in ((0, 0), (0, 1), (1, 1), (2, 1)):
        out.append(_block(nx + 10 + dx * CELL, ny + 10 + dy * CELL + 6, 0.95))
    return {
        "w": W, "h": H, "body": "".join(out), "defs": "", "foot": WY + ROWS * CELL + 28, "top": 90,
        "caption": f"one column per month · {total:,} contributions · taller stacks are busier months",
        "title": "block-stack", "cmd": "play --last 12mo  # one column per month",
        "aria": f"Falling-block puzzle with one stacked column per month, score {total:,}",
    }
