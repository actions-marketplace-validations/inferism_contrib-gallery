"""A fungal network spreading from the start of the year on the left to today on the right. Streaks become thick trunks."""
import math
import random

from common import W, level, peak_of

H = 700
X0, X1 = 44, W - 44
CY = 390
MAX_TWIGS = 420


def _baseline(x, ph):
    """The slow wandering line the whole network grows along."""
    t = (x - X0) / (X1 - X0)
    return CY + 105 * math.sin(t * math.tau * 1.15 + ph) + 40 * math.sin(t * math.tau * 2.7 + ph * 2)


def _q(a, b, bend):
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy) or 1
    return f"M{a[0]:.1f} {a[1]:.1f}Q{mx - dy / n * bend:.1f} {my + dx / n * bend:.1f} {b[0]:.1f} {b[1]:.1f}"


def render(days):
    n = len(days)
    peak = peak_of(days)
    total = sum(d["count"] for d in days)
    rnd = random.Random(total * 13 + n)
    ph = rnd.uniform(0, math.tau)
    tx = lambda i: X0 + i / max(1, n - 1) * (X1 - X0)

    streaks, i = [], 0
    while i < n:
        if days[i]["count"]:
            j = i
            while j < n and days[j]["count"]:
                j += 1
            streaks.append((i, j))
            i = j
        else:
            i += 1

    pos, out, twigs = {}, [], 0
    prev_end = None
    for s, e in streaks:
        m = e - s
        span = min(m * 10, 130) if m > 1 else 0
        xs = min(tx(s), X1 - span)
        xe = min(X1, max(tx(e - 1), xs + span))
        y0 = _baseline(xs, ph) + rnd.uniform(-38, 38)
        wave = rnd.uniform(0, math.tau)
        pts = []
        for k in range(m):
            x = xs + (xe - xs) * (k / (m - 1) if m > 1 else 0)
            y = y0 + (_baseline(x, ph) - _baseline(xs, ph)) + 20 * math.sin(math.tau * (x - xs) / 80 + wave)
            pts.append((x, y))
            pos[s + k] = (x, y)
        # a faint dotted thread carries on from the last streak, like the colony exploring across bare ground
        if prev_end:
            sag = rnd.uniform(-30, 30)
            out.append(f'<path d="{_q(prev_end, pts[0], sag)}" fill="none" stroke="#9a9aa1" stroke-width="3" stroke-linecap="round" stroke-dasharray="0.1 9" stroke-opacity="0.75"/>')
        prev_end = pts[-1]

        if m == 1:  # an isolated day: a thin wisp
            x, y = pts[0]
            for _ in range(5):
                a = rnd.uniform(0, math.tau)
                L = rnd.uniform(12, 28)
                out.append(f'<path d="{_q((x, y), (x + L * math.cos(a), y + L * math.sin(a)), rnd.uniform(-4, 4))}" fill="none" stroke="#d4d4d8" stroke-width="0.8" stroke-opacity="0.6" stroke-linecap="round"/>')
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{1.4 + 1.2 * days[s]["count"] / peak:.1f}" class="hi" fill-opacity="0.85"/>')
            continue

        for k in range(m - 1):
            a, b = days[s + k]["count"], days[s + k + 1]["count"]
            w = 1.6 + 7 * math.sqrt((a + b) / (2 * peak))
            op = 0.5 + 0.4 * math.sqrt((a + b) / (2 * peak))
            out.append(f'<path d="{_q(pts[k], pts[k + 1], rnd.uniform(-1.5, 1.5))}" fill="none" class="hi" stroke="#fff" stroke-width="{w:.1f}" stroke-linecap="round" stroke-opacity="{op:.2f}"/>')
        for k, (x, y) in enumerate(pts):
            c = days[s + k]["count"]
            lv = level(c, peak)
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{1.2 + 2.2 * math.sqrt(c / peak):.1f}" class="hi" fill-opacity="{0.55 + 0.1 * lv:.2f}"/>')
            if twigs < MAX_TWIGS and rnd.random() < 0.12 + 0.12 * lv:  # side hyphae reach out from busy nodes
                twigs += 1
                hd = math.atan2(pts[min(k + 1, m - 1)][1] - pts[max(k - 1, 0)][1], pts[min(k + 1, m - 1)][0] - pts[max(k - 1, 0)][0])
                a = hd + rnd.choice((-1, 1)) * rnd.uniform(0.7, 1.4)
                L = 14 + 40 * math.sqrt(c / peak) * rnd.uniform(0.5, 1)
                end = (x + L * math.cos(a), y + L * math.sin(a))
                tw = 0.9 + 1.8 * math.sqrt(c / peak)
                out.append(f'<path d="{_q((x, y), end, rnd.uniform(-8, 8))}" fill="none" stroke="#d4d4d8" stroke-width="{tw:.1f}" stroke-opacity="0.65" stroke-linecap="round"/>'
                           f'<circle cx="{end[0]:.1f}" cy="{end[1]:.1f}" r="{tw * 0.8 + 0.6:.1f}" class="txt" fill-opacity="0.85"/>')
                if lv >= 2:  # forked tip
                    mid = (x + (end[0] - x) * 0.6, y + (end[1] - y) * 0.6)
                    a2 = a + rnd.choice((-1, 1)) * rnd.uniform(0.6, 1.0)
                    e2 = (mid[0] + L * 0.45 * math.cos(a2), mid[1] + L * 0.45 * math.sin(a2))
                    out.append(f'<path d="{_q(mid, e2, rnd.uniform(-4, 4))}" fill="none" stroke="#d4d4d8" stroke-width="{tw * 0.7:.1f}" stroke-opacity="0.55" stroke-linecap="round"/>')

    if not streaks:  # an empty year still shows the bare substrate the colony would grow on
        pts = [(X0 + k / 24 * (X1 - X0), _baseline(X0 + k / 24 * (X1 - X0), ph)) for k in range(25)]
        d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}" + "".join(
            f"Q{(pts[k][0] + pts[k + 1][0]) / 2:.1f} {pts[k][1] + (pts[k + 1][1] - pts[k][1]) * 0.1:.1f} {pts[k + 1][0]:.1f} {pts[k + 1][1]:.1f}" for k in range(24))
        out.append(f'<path d="{d}" fill="none" stroke="#9a9aa1" stroke-width="3.4" stroke-linecap="round" stroke-dasharray="0.1 10" stroke-opacity="0.8"/>')

    # a mushroom on each of the five busiest days
    top5 = sorted((k for k in pos), key=lambda k: (-days[k]["count"], k))[:5]
    for k in top5:
        x, y = pos[k]
        share = math.sqrt(days[k]["count"] / peak)
        h, cw = 20 + 24 * share, 13 + 12 * share
        sway = rnd.uniform(-5, 5)
        ty = y - h
        out.append(
            f'<path d="M{x:.1f} {y:.1f}Q{x + sway:.1f} {y - h * 0.5:.1f} {x + sway * 0.6:.1f} {ty:.1f}" fill="none" stroke="#d4d4d8" stroke-width="{3 + 2 * share:.1f}" stroke-linecap="round"/>'
            f'<path d="M{x + sway * 0.6 - cw:.1f} {ty + 3:.1f}Q{x + sway * 0.6 - cw:.1f} {ty - cw * 1.1:.1f} {x + sway * 0.6:.1f} {ty - cw * 1.1:.1f}'
            f'Q{x + sway * 0.6 + cw:.1f} {ty - cw * 1.1:.1f} {x + sway * 0.6 + cw:.1f} {ty + 3:.1f}Q{x + sway * 0.6:.1f} {ty + 9:.1f} {x + sway * 0.6 - cw:.1f} {ty + 3:.1f}Z" '
            f'class="hi" fill-opacity="0.92" stroke="#fff" stroke-width="1"/>'
            f'<circle cx="{x + sway * 0.6 - cw * 0.35:.1f}" cy="{ty - cw * 0.55:.1f}" r="{cw * 0.14:.1f}" fill="#0b0b0c" fill-opacity="0.55"/>'
            f'<circle cx="{x + sway * 0.6 + cw * 0.3:.1f}" cy="{ty - cw * 0.35:.1f}" r="{cw * 0.1:.1f}" fill="#0b0b0c" fill-opacity="0.55"/>'
        )
    active = sum(1 for d in days if d["count"])
    return {
        "w": W, "h": H, "body": "".join(out), "defs": "", "foot": H - 40, "top": 84,
        "caption": f"{active} nodes · {len(streaks)} colonies · {total:,} contributions · mushrooms on the 5 busiest days",
        "title": "mycelium", "cmd": "spawn --substrate soil",
        "aria": f"Fungal network spreading from left to right across the year with a node for each of the {active} active days, thick trunks for streaks, thin wisps for isolated days and mushrooms on the five busiest days",
    }
