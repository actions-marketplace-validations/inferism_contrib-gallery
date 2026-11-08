"""A reef growing up from the seabed: a coral branch for every active week, bleached stubs where the weeks went quiet."""
import math
import random

from common import W, grid_pos, level, peak_of

H = 610
BASE = 550
X0, X1 = 44, W - 44
IDLE_RUN = 3  # this many quiet weeks in a row leave bleached stubs


def _pt(b, t):
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = b
    u = 1 - t
    return (u ** 3 * x0 + 3 * u * u * t * x1 + 3 * u * t * t * x2 + t ** 3 * x3,
            u ** 3 * y0 + 3 * u * u * t * y1 + 3 * u * t * t * y2 + t ** 3 * y3)


def _curve(p0, ang, length, sway):
    dx, dy = math.sin(ang), -math.cos(ang)
    nx, ny = -dy, dx
    p1 = (p0[0] + dx * length * 0.35 + nx * sway, p0[1] + dy * length * 0.35 + ny * sway)
    p2 = (p0[0] + dx * length * 0.72 - nx * sway * 0.5, p0[1] + dy * length * 0.72 - ny * sway * 0.5)
    p3 = (p0[0] + dx * length + nx * sway * 0.2, p0[1] + dy * length + ny * sway * 0.2)
    return p0, p1, p2, p3


def _d(b):
    return f"M{b[0][0]:.1f} {b[0][1]:.1f}C{b[1][0]:.1f} {b[1][1]:.1f} {b[2][0]:.1f} {b[2][1]:.1f} {b[3][0]:.1f} {b[3][1]:.1f}"


def render(days):
    peak = peak_of(days)
    pos = grid_pos(days)
    nw = max(w for w, _ in pos) + 1
    tot, busy = [0] * nw, [0] * nw
    for d, (w, _) in zip(days, pos):
        tot[w] += d["count"]
        if level(d["count"], peak) >= 3:
            busy[w] += 1
    pw = max(tot) or 1
    total = sum(tot)
    rnd = random.Random(total * 17 + len(days))

    # which quiet weeks belong to a long idle stretch
    stub = [False] * nw
    w = 0
    while w < nw:
        if tot[w] == 0:
            e = w
            while e < nw and tot[e] == 0:
                e += 1
            if e - w >= IDLE_RUN:
                for k in range(w, e):
                    stub[k] = True
            w = e
        else:
            w += 1

    def xw(k):
        return X0 + (k + 0.5) / nw * (X1 - X0)

    out = []
    # seabed: a soft sandy mound, no wave lines
    out.append(
        f'<path d="M-10 {BASE + 6}C120 {BASE - 8} 230 {BASE + 14} 360 {BASE + 4}S620 {BASE - 10} 760 {BASE + 6}S930 {BASE + 12} 1010 {BASE}'
        f'Q1012 {H} 1000 {H}Q500 {H + 8} 0 {H}Q-12 {H} -10 {BASE + 6}Z" class="dim" fill-opacity="0.22" stroke="#9a9aa1" stroke-width="2" stroke-opacity="0.7"/>'
    )
    for _ in range(46):
        out.append(f'<circle cx="{rnd.uniform(10, 990):.1f}" cy="{rnd.uniform(BASE + 14, H - 8):.1f}" r="{rnd.uniform(0.7, 1.7):.1f}" class="dim" fill-opacity="0.5"/>')

    bleached = 0
    for k in range(nw):
        if stub[k]:
            bleached += 1
            x, h = xw(k) + rnd.uniform(-4, 4), rnd.uniform(9, 24)
            b = _curve((x, BASE + 4), rnd.uniform(-0.25, 0.25), h, rnd.uniform(-3, 3))
            out.append(
                f'<path d="{_d(b)}" fill="none" stroke="#9a9aa1" stroke-width="{rnd.uniform(4, 6):.1f}" stroke-linecap="round" stroke-opacity="0.55"/>'
                f'<circle cx="{b[3][0]:.1f}" cy="{b[3][1]:.1f}" r="2.4" class="dim" fill-opacity="0.6"/>'
            )

    order = sorted((k for k in range(nw) if tot[k]), key=lambda k: -tot[k])  # tall corals behind, small ones in front
    for k in order:
        share = math.sqrt(tot[k] / pw)
        length = 44 + share * 300
        forks = 1 + round(6 * share)
        width = 6 + 11 * share
        op = 0.55 + 0.4 * share
        x = xw(k) + rnd.uniform(-3, 3)
        stem = _curve((x, BASE + 4), rnd.uniform(-0.16, 0.16), length, rnd.uniform(-14, 14) * (0.4 + share))
        branches = [(stem, width)]
        for f in range(forks):
            t = 0.28 + 0.58 * (f + 0.5) / forks
            side = -1 if (f + k) % 2 else 1
            px, py = _pt(stem, t)
            ang = side * rnd.uniform(0.35, 0.8)
            child = _curve((px, py), ang, length * rnd.uniform(0.3, 0.5) * (1 - 0.4 * t), side * rnd.uniform(3, 9))
            branches.append((child, width * 0.72))
            if forks >= 4 and f % 2 == 0:
                sx, sy = _pt(child, rnd.uniform(0.55, 0.8))
                sub = _curve((sx, sy), ang - side * rnd.uniform(0.7, 1.1), length * rnd.uniform(0.12, 0.2), side * rnd.uniform(2, 6))
                branches.append((sub, width * 0.56))
        for b, wd in branches:
            out.append(f'<path d="{_d(b)}" fill="none" class="hi" stroke="#fff" stroke-width="{wd:.1f}" stroke-linecap="round" stroke-opacity="{op:.2f}"/>')
            out.append(f'<circle cx="{b[3][0]:.1f}" cy="{b[3][1]:.1f}" r="{wd * 0.78:.1f}" class="hi" fill-opacity="{min(1, op + 0.1):.2f}"/>')
        for _ in range(min(busy[k], 5)):  # a polyp for each busy day
            b, wd = branches[rnd.randrange(len(branches))]
            px, py = _pt(b, rnd.uniform(0.25, 0.95))
            out.append(
                f'<circle cx="{px + rnd.uniform(-1.5, 1.5):.1f}" cy="{py:.1f}" r="{wd * 0.3 + 1.2:.1f}" fill="#0b0b0c" fill-opacity="0.8"/>'
                f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{wd * 0.14 + 0.8:.1f}" class="txt"/>'
            )
    active = sum(1 for t in tot if t)
    return {
        "w": W, "h": H, "body": "".join(out), "defs": "", "foot": H - 14, "top": 84,
        "caption": f"{active} corals · {bleached} bleached stubs · {total:,} contributions",
        "title": "coral-reef", "cmd": "reef grow --weekly",
        "aria": f"Coral reef growing from the seabed with {active} coral branches, one for each active week, taller and more forked for busier weeks, and {bleached} short bleached stubs where weeks went quiet",
    }
