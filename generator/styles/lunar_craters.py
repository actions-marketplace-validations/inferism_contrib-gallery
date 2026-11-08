"""The moon's surface from orbit: every active day leaves a crater, bigger and deeper when busier."""
import math
import random

from common import W, grid_pos, peak_of

H = 500
TOP, FOOT = 96, 450


def render(days):
    peak = peak_of(days)
    pos = grid_pos(days)
    weeks = max(w for w, _ in pos) + 1
    rnd = random.Random(31)
    x0, x1 = 44, W - 44
    cw = (x1 - x0) / max(1, weeks)
    y0, rh = TOP + 26, (FOOT - TOP - 52) / 6

    out = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="#fff" fill-opacity="0.1"/>']
    for _ in range(90):  # fine grain on the ground
        out.append(
            f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, H):.0f}" r="{rnd.uniform(0.6, 1.6):.1f}" '
            f'fill="#fff" fill-opacity="{rnd.uniform(0.04, 0.1):.2f}"/>'
        )

    # biggest first, and each crater shrinks until it fits between the ones already placed
    todo = []
    for d, (w, dow) in zip(days, pos):
        x = x0 + (w + 0.5) * cw + rnd.uniform(-0.35, 0.35) * cw
        y = y0 + dow * rh + rnd.uniform(-0.28, 0.28) * rh
        todo.append((d["count"], x, y))
    placed, dust = [], []
    for c, x, y in sorted(todo, key=lambda t: -t[0]):
        if not c:
            if rnd.random() < 0.5:
                dust.append((x, y))
            continue
        r = 3.5 + math.sqrt(c / peak) * 20
        while r >= 2.4 and any(math.hypot(x - px, y - py) < (r + pr) * 0.85 for px, py, pr, _ in placed):
            r *= 0.88
        if r < 2.4:
            dust.append((x, y))
        else:
            placed.append((x, y, r, math.sqrt(c / peak)))

    for x, y, r, t in placed:
        s = max(0.9, r * 0.12)
        sx, sy = x + r * 0.12, y + r * 0.14
        out.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="#050507" fill-opacity="{0.45 + t * 0.35:.2f}"/>'  # bowl
            f'<circle cx="{x + r * 0.22:.1f}" cy="{y + r * 0.22:.1f}" r="{r * 0.68:.1f}" fill="#fff" fill-opacity="0.13"/>'  # lit far wall
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="none" stroke="#fff" stroke-opacity="{0.4 + t * 0.4:.2f}" stroke-width="{s:.1f}"/>'  # raised rim
            f'<path d="M{sx - r * 0.78:.1f} {sy + r * 0.72:.1f}A{r:.1f} {r:.1f} 0 0 0 {sx + r * 0.72:.1f} {sy + r * 0.78:.1f}" fill="none" '
            f'stroke="#050507" stroke-opacity="0.5" stroke-width="{s * 1.6:.1f}"/>'  # shadow
        )
    for x, y in dust:
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.uniform(0.5, 1.2):.1f}" fill="#fff" fill-opacity="{rnd.uniform(0.15, 0.35):.2f}"/>')

    out.append(
        f'<path d="M{W - 150} {FOOT - 4}h80M{W - 150} {FOOT - 9}v10M{W - 70} {FOOT - 9}v10" fill="none" stroke="#fff" stroke-opacity="0.55" stroke-width="1.5"/>'
        f'<text x="{W - 110}" y="{FOOT - 14}" text-anchor="middle" class="txt" font-size="11" fill-opacity="0.8">50 km</text>'
    )
    total = sum(d["count"] for d in days)
    return {
        "w": W, "h": H, "body": "".join(out), "defs": "", "top": TOP, "foot": FOOT,
        "caption": f"{total:,} contributions · {len(placed)} craters · bigger craters are busier days",
        "title": "lunar-craters", "cmd": "survey --last 365d  # a crater for every active day",
        "aria": f"The moon's surface seen from orbit with {len(placed)} craters for the active days of the last year, bigger for busier days",
    }
