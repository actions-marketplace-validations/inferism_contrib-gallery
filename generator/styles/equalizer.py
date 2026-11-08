"""An audio equalizer: one bar per week that bounces, taller for busier weeks."""
import random

from common import W, grid_pos

H = 380
BASE, MAXH = 320, 220


def render(days):
    pos = grid_pos(days)
    nw = max(w for w, _ in pos) + 1
    tot = [0] * nw
    for d, (w, _) in zip(days, pos):
        tot[w] += d["count"]
    top_week = max(tot) or 1
    rnd = random.Random(6)
    pitch = (W - 56) / nw
    bars = []
    for w in range(nw):
        h = 3 + (tot[w] / top_week) * MAXH if tot[w] else 3
        x = 28 + w * pitch
        dur, delay = 0.8 + rnd.random() * 0.9, -rnd.random() * 2
        op = 0.35 + 0.65 * tot[w] / top_week if tot[w] else 0.2
        bars.append(
            f'<rect class="eq" x="{x + 1:.1f}" y="{BASE - h:.1f}" width="{pitch - 3:.1f}" height="{h:.1f}" rx="2" fill="#fff" '
            f'fill-opacity="{op:.2f}" style="animation-duration:{dur:.2f}s;animation-delay:{delay:.2f}s"/>'
        )
    css = (
        ".eq { transform-box: fill-box; transform-origin: 50% 100%; animation: eq 1s ease-in-out infinite; } "
        "@keyframes eq { 0%, 100% { transform: scaleY(1); } 50% { transform: scaleY(0.55); } }"
    )
    total = sum(tot)
    body = f'<line x1="28" y1="{BASE + 4}" x2="{W - 28}" y2="{BASE + 4}" stroke="#2a2a2d" stroke-width="2"/>' + "".join(bars)
    return {
        "w": W, "h": H, "body": body, "defs": "", "css": css, "foot": BASE + 12, "top": BASE - MAXH - 10,
        "caption": f"{total:,} contributions · one bar per week",
        "title": "equalizer", "cmd": "play --last 52w  # a bar for every week",
        "aria": f"Equalizer with one bouncing bar for each of the {nw} weeks, taller for busier weeks",
    }
