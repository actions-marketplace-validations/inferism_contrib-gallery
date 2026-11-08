"""Blocks stack up one column per week, and a few more keep dropping in."""
import random

from common import W, grid_pos

H = 420
BASE, BLOCK = 360, 17.6
MAX_ROWS = 14


def render(days):
    pos = grid_pos(days)
    nw = max(w for w, _ in pos) + 1
    tot = [0] * nw
    for d, (w, _) in zip(days, pos):
        tot[w] += d["count"]
    top_week = max(tot) or 1
    rnd = random.Random(8)
    pitch = (W - 56) / nw
    heights = [round(t / top_week * MAX_ROWS) if t else 0 for t in tot]

    def block(x, y, op, cls=""):
        return (
            f'<rect {cls}x="{x + 1:.1f}" y="{y + 1:.1f}" width="{pitch - 2:.1f}" height="{BLOCK - 2:.1f}" rx="2" fill="#fff" fill-opacity="{op:.2f}"/>'
        )

    out = [f'<line x1="28" y1="{BASE + 2}" x2="{W - 28}" y2="{BASE + 2}" stroke="#2a2a2d" stroke-width="2"/>']
    for w, h in enumerate(heights):
        for r in range(h):
            out.append(block(28 + w * pitch, BASE - (r + 1) * BLOCK, 0.9 if r == h - 1 else 0.38 + 0.4 * (r % 3) / 2))
    live = [w for w, h in enumerate(heights) if h] or [0]
    for k in range(7):  # pieces still on their way down, landing on top of a column
        w = rnd.choice(live)
        y = BASE - (heights[w] + 1) * BLOCK
        out.append(
            f'<g class="drop" style="animation-delay:-{k * 0.9:.1f}s"><rect x="{28 + w * pitch + 1:.1f}" y="{y + 1:.1f}" '
            f'width="{pitch - 2:.1f}" height="{BLOCK - 2:.1f}" rx="2" fill="#fff"/></g>'
        )
    css = (
        ".drop { animation: drop 6.3s ease-in infinite; } "
        "@keyframes drop { 0% { transform: translateY(-260px); opacity: 0; } 10% { opacity: 1; } "
        "62%, 90% { transform: translateY(0); opacity: 1; } 100% { transform: translateY(0); opacity: 0; } }"
    )
    total = sum(tot)
    return {
        "w": W, "h": H, "body": "".join(out), "defs": "", "css": css, "foot": BASE + 8, "top": BASE - MAX_ROWS * BLOCK - 20,
        "caption": f"{total:,} contributions · one column per week",
        "title": "falling-blocks", "cmd": "drop --last 52w  # a column for every week",
        "aria": f"Blocks stacked into {nw} weekly columns, with more blocks dropping in",
    }
