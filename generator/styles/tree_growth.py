"""A tree that grows a branch for every active week. Longer branches are busier weeks."""
import math
import random

from common import W, grid_pos, peak_of

H = 600


def render(days):
    peak = peak_of(days)
    pos = grid_pos(days)
    nw = max(w for w, _ in pos) + 1
    tot = [0] * nw
    act = [0] * nw
    for d, (w, _) in zip(days, pos):
        tot[w] += d["count"]
        act[w] += 1 if d["count"] else 0
    pw = max(tot) or 1
    rnd = random.Random(5)
    cx, base, top = 500, 548, 238

    out = [
        f'<line x1="120" y1="{base}" x2="880" y2="{base}" stroke="#2a2a2d" stroke-width="2"/>',
        f'<path d="M{cx - 20} {base}Q{cx - 6} {(base + top) / 2:.0f} {cx - 5} {top}H{cx + 5}Q{cx + 6} {(base + top) / 2:.0f} {cx + 20} {base}Z" '
        'fill="#1b1b1e" stroke="#9a9aa1" stroke-width="1.5"/>',
    ]
    for w in range(nw):
        if not tot[w]:
            continue
        y = base - 26 - w / max(1, nw - 1) * (base - top - 30)
        side = -1 if w % 2 == 0 else 1
        length = 30 + math.sqrt(tot[w] / pw) * 215
        ang = math.radians(26 + (w % 3) * 7)
        x1, y1 = cx + side * length * math.cos(ang), y - length * math.sin(ang)
        cxp, cyp = cx + side * length * 0.42, y - length * math.sin(ang) * 0.78
        out.append(
            f'<path d="M{cx} {y:.1f}Q{cxp:.1f} {cyp:.1f} {x1:.1f} {y1:.1f}" fill="none" stroke="#d4d4d8" '
            f'stroke-width="{1 + tot[w] / pw * 2.6:.1f}" stroke-opacity="0.7" stroke-linecap="round"/>'
        )
        for k in range(min(act[w], 7)):  # one leaf per active day, up to seven
            t = 0.4 + 0.6 * (k + 1) / (min(act[w], 7) + 0.3)
            bx = (1 - t) ** 2 * cx + 2 * (1 - t) * t * cxp + t * t * x1
            by = (1 - t) ** 2 * y + 2 * (1 - t) * t * cyp + t * t * y1
            r = 2 + rnd.random() * 2.6 + tot[w] / pw * 2
            out.append(
                f'<circle cx="{bx + rnd.uniform(-4, 4):.1f}" cy="{by + rnd.uniform(-9, -2):.1f}" r="{r:.1f}" '
                f'fill="#fff" fill-opacity="{0.45 + rnd.random() * 0.5:.2f}"/>'
            )
    out.append(f'<circle cx="{cx}" cy="{top - 4}" r="5" fill="#fff"/>')
    weeks = sum(1 for t in tot if t)
    total = sum(d["count"] for d in days)
    out.append(f'<text x="28" y="{H - 22}" class="dim" font-size="15">{weeks} branches · {total:,} contributions · oldest weeks at the roots</text>')
    return {
        "w": W, "h": H, "body": "".join(out), "defs": "",
        "title": "tree", "cmd": "grow --last 365d  # a branch for every active week",
        "aria": f"Tree with {weeks} branches, one for each active week of the last year",
    }
