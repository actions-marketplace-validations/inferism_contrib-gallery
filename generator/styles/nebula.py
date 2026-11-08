"""A nebula: one soft cloud of gas per week, thicker and brighter when busier, blending into one long cloud."""
import math
import random

from common import MONTHS, W, grid_pos, starfield

H = 410
CY = 205


def render(days):
    pos = grid_pos(days)
    nw = max(w for w, _ in pos) + 1
    tot = [0] * nw
    for d, (w, _) in zip(days, pos):
        tot[w] += d["count"]
    top_week = max(tot) or 1
    rnd = random.Random(47)
    x0, x1 = 70, W - 70
    step = (x1 - x0) / max(1, nw - 1)
    ph = [rnd.uniform(0, math.tau) for _ in range(3)]

    defs = (
        '<radialGradient id="nbg"><stop offset="0" stop-color="#fff" stop-opacity="1"/>'
        '<stop offset="0.45" stop-color="#fff" stop-opacity="0.4"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
        '<filter id="nbblur" x="-10%" y="-40%" width="120%" height="180%"><feGaussianBlur stdDeviation="9"/></filter>'
    )
    puffs, stars, centers = [], [], []
    for w in range(nw):
        x = x0 + (w * step if nw > 1 else (x1 - x0) / 2)
        y = CY + 46 * math.sin(w * 0.19 + ph[0]) + 24 * math.sin(w * 0.47 + ph[1]) + 10 * math.sin(w * 1.1 + ph[2])
        t = math.sqrt(tot[w] / top_week) if tot[w] else 0
        centers.append((x, y, t))
        count = 3 if t else 1
        for _ in range(count):
            rx = (46 + 70 * t) * rnd.uniform(0.8, 1.25)
            ry = (24 + 52 * t) * rnd.uniform(0.8, 1.25)
            op = 0.05 + 0.3 * t if t else 0.045
            puffs.append(
                f'<ellipse cx="{x + rnd.uniform(-14, 14):.0f}" cy="{y + rnd.uniform(-0.5, 0.5) * ry:.0f}" rx="{rx:.0f}" ry="{ry:.0f}" '
                f'fill="url(#nbg)" fill-opacity="{op:.2f}"/>'
            )
        if t > 0.55:  # young stars in the thickest clouds
            for _ in range(1 + int(t * 3)):
                sx, sy = x + rnd.uniform(-24, 24), y + rnd.uniform(-26, 26)
                r = rnd.uniform(0.9, 1.9)
                stars.append(
                    f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="{r:.1f}" fill="#fff"/>'
                    f'<path d="M{sx - r * 3.2:.1f} {sy:.1f}h{r * 6.4:.1f}M{sx:.1f} {sy - r * 3.2:.1f}v{r * 6.4:.1f}" stroke="#fff" stroke-opacity="0.5" stroke-width="0.7"/>'
                )

    # a thin trail of dust connecting the clouds, then the cloud itself
    out = [f'<g filter="url(#nbblur)">{"".join(puffs)}</g>', "".join(stars)]

    seen = set()
    for d, (w, _) in zip(days, pos):
        m = d["date"][:7]
        if m not in seen and d["date"][8:10] <= "07":
            seen.add(m)
            x = centers[w][0]
            out.append(
                f'<path d="M{x:.0f} 350v6" stroke="#fff" stroke-opacity="0.35"/>'
                f'<text x="{x:.0f}" y="370" text-anchor="middle" class="dim" font-size="11">{MONTHS[int(m[5:]) - 1]}</text>'
            )
    total = sum(tot)
    return {
        "w": W, "h": H, "body": "".join(out), "defs": defs, "top": 96, "foot": 376, "deco": starfield(W, H, 5, 130),
        "caption": f"{total:,} contributions · one cloud per week, thicker when busier",
        "title": "nebula", "cmd": "image --last 52w  # a cloud of gas for every week",
        "aria": f"A nebula of {nw} soft clouds, one per week, thicker and brighter in busier weeks",
    }
