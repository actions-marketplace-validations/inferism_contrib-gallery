"""A meandering river seen from above, flowing through the year. Wider in busy weeks, with sharper bends and sandbanks."""
import math
import random

from common import MONTHS, W, grid_pos

H = 620
X0, X1 = 44, W - 44
CY = 350
S = 5          # samples per week along the curve
DRY = 8        # channel width of a dry week
CSS = ".flow { stroke-dasharray: 3 15; animation: flow 3.2s linear infinite; } @keyframes flow { to { stroke-dashoffset: -36; } }"


def _spline(pts):
    """Catmull-Rom through (x, y, w) control points, S samples between each pair."""
    out = []
    n = len(pts)
    for i in range(n - 1):
        p0, p1, p2, p3 = pts[max(i - 1, 0)], pts[i], pts[i + 1], pts[min(i + 2, n - 1)]
        for s in range(S):
            t = s / S
            out.append(tuple(
                0.5 * (2 * p1[c] + (-p0[c] + p2[c]) * t + (2 * p0[c] - 5 * p1[c] + 4 * p2[c] - p3[c]) * t * t + (-p0[c] + 3 * p1[c] - 3 * p2[c] + p3[c]) * t ** 3)
                for c in range(3)))
    out.append(pts[-1])
    return out


def _smooth(pts, move=True):
    """A smooth run of quadratic segments through the midpoints."""
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}" if move else ""
    for i in range(1, len(pts) - 1):
        d += f"Q{pts[i][0]:.1f} {pts[i][1]:.1f} {(pts[i][0] + pts[i + 1][0]) / 2:.1f} {(pts[i][1] + pts[i + 1][1]) / 2:.1f}"
    return d + f"L{pts[-1][0]:.1f} {pts[-1][1]:.1f}" if len(pts) > 1 else d


def render(days):
    pos = grid_pos(days)
    nw = max(w for w, _ in pos) + 1
    tot = [0] * nw
    for d, (w, _) in zip(days, pos):
        tot[w] += d["count"]
    pw = max(tot) or 1
    total = sum(tot)
    rnd = random.Random(total * 7 + len(days))
    raw = [math.sqrt(t / pw) for t in tot]
    sm = [0.25 * raw[max(k - 1, 0)] + 0.5 * raw[k] + 0.25 * raw[min(k + 1, nw - 1)] for k in range(nw)]

    # the centre line: busy weeks bend harder and more often, calm ones drift
    dx, phase, ctrl = (X1 - X0) / nw, rnd.uniform(0, math.tau), []
    for k in range(nw):
        phase += math.tau * dx / (700 - 320 * sm[k])
        y = CY + 30 * math.sin(k / nw * math.tau * 0.8 + 1) + (30 + 95 * sm[k]) * math.sin(phase)
        width = 12 + 42 * raw[k] if tot[k] else DRY
        ctrl.append((X0 + (k + 0.5) * dx, y, width))
    pts = _spline(ctrl)
    m = len(pts)
    tan, nor = [], []
    for j in range(m):
        a, b = pts[max(j - 1, 0)], pts[min(j + 1, m - 1)]
        tx, ty = b[0] - a[0], b[1] - a[1]
        l = math.hypot(tx, ty) or 1
        tan.append((tx / l, ty / l))
        nor.append((-ty / l, tx / l))
    left = [(p[0] + nor[j][0] * p[2] / 2, p[1] + nor[j][1] * p[2] / 2) for j, p in enumerate(pts)]
    right = [(p[0] - nor[j][0] * p[2] / 2, p[1] - nor[j][1] * p[2] / 2) for j, p in enumerate(pts)]
    kappa = [0.0] * m
    for j in range(2, m - 2):
        kappa[j] = (tan[j + 2][0] * tan[j - 2][1] - tan[j + 2][1] * tan[j - 2][0]) / max(1.0, math.hypot(pts[j + 2][0] - pts[j - 2][0], pts[j + 2][1] - pts[j - 2][1]))

    runs, k = [], 0
    while k < nw:
        wet = tot[k] > 0
        e = k
        while e < nw and (tot[e] > 0) == wet:
            e += 1
        runs.append((max(0, k * S - S // 2), min(m - 1, (e - 1) * S + S // 2), wet))
        k = e

    out, wet_weeks = [], sum(1 for t in tot if t)
    sand, water, dry, flow = [], [], [], []
    for a, b, wet in runs:
        if b - a < 2:
            continue
        L, R, C = left[a:b + 1], right[a:b + 1], pts[a:b + 1]
        if wet:
            end = pts[b]
            t_end, t_start = tan[b], tan[a]
            cap_e = (end[0] + t_end[0] * end[2] * 0.7, end[1] + t_end[1] * end[2] * 0.7)
            cap_s = (pts[a][0] - t_start[0] * pts[a][2] * 0.7, pts[a][1] - t_start[1] * pts[a][2] * 0.7)
            d = _smooth(L) + f"Q{cap_e[0]:.1f} {cap_e[1]:.1f} {R[-1][0]:.1f} {R[-1][1]:.1f}" + _smooth(R[::-1], False) + f"Q{cap_s[0]:.1f} {cap_s[1]:.1f} {L[0][0]:.1f} {L[0][1]:.1f}Z"
            water.append(f'<path d="{d}" class="hi" fill-opacity="0.30" stroke="#fff" stroke-width="1.6" stroke-opacity="0.85" stroke-linejoin="round"/>')
            flow.append(f'<path d="{_smooth(C)}" fill="none" class="flow" stroke="#fff" stroke-width="1.3" stroke-opacity="0.65" stroke-linecap="round"/>')
            # sandbanks on the inner side of each bend
            j = a
            while j < b:
                sign = 1 if kappa[j] > 0 else -1
                if abs(kappa[j]) < 0.006:
                    j += 1
                    continue
                e = j
                while e < b and abs(kappa[e]) >= 0.006 and (kappa[e] > 0) == (kappa[j] > 0):
                    e += 1
                if e - j >= 6:
                    peak_k = max(abs(kappa[i]) for i in range(j, e))
                    smax = 7 + 14 * min(1, peak_k / 0.03)
                    bank = left if sign > 0 else right
                    out_dir = 1 if sign > 0 else -1
                    inner = [bank[i] for i in range(j, e)]
                    outer = [(bank[i][0] + nor[i][0] * out_dir * smax * math.sin(math.pi * (i - j) / (e - j)),
                              bank[i][1] + nor[i][1] * out_dir * smax * math.sin(math.pi * (i - j) / (e - j))) for i in range(j, e)]
                    sand.append(f'<path d="{_smooth(inner)}{_smooth(outer[::-1], False)}Z" class="dim" fill-opacity="0.38"/>')
                    for _ in range((e - j) // 2):
                        i = rnd.randrange(j, e)
                        f = rnd.uniform(0.15, 0.85) * smax * math.sin(math.pi * (i - j) / (e - j))
                        sand.append(f'<circle cx="{bank[i][0] + nor[i][0] * out_dir * f:.1f}" cy="{bank[i][1] + nor[i][1] * out_dir * f:.1f}" r="{rnd.uniform(0.6, 1.3):.1f}" class="txt" fill-opacity="0.55"/>')
                j = e
        else:  # a dry riverbed: dotted banks and pebbles
            for side in (L, R):
                dry.append(f'<path d="{_smooth(side)}" fill="none" stroke="#9a9aa1" stroke-width="2.6" stroke-linecap="round" stroke-dasharray="0.1 7" stroke-opacity="0.8"/>')
            for j in range(a, b, 2):
                if rnd.random() < 0.6:
                    off = rnd.uniform(-0.3, 0.3) * pts[j][2]
                    dry.append(f'<circle cx="{pts[j][0] + nor[j][0] * off:.1f}" cy="{pts[j][1] + nor[j][1] * off:.1f}" r="{rnd.uniform(0.7, 1.5):.1f}" class="dim" fill-opacity="0.6"/>')

    labels, seen = [], ""
    for i, d in enumerate(days):
        if d["date"][:7] != seen:
            seen = d["date"][:7]
            j = min(m - 1, max(0, pos[i][0]) * S)
            p = pts[j]
            above = p[1] > CY
            ly = p[1] - p[2] / 2 - 24 if above else p[1] + p[2] / 2 + 32
            labels.append(f'<text x="{p[0]:.1f}" y="{ly:.1f}" class="dim" font-size="12" text-anchor="middle">{MONTHS[int(seen[5:]) - 1]}</text>')
    body = "".join(sand + dry + water + flow + labels)
    return {
        "w": W, "h": H, "body": body, "defs": "", "css": CSS, "foot": H - 36, "top": 84,
        "caption": f"{wet_weeks} wet weeks · {nw - wet_weeks} dry · {total:,} contributions · flows from January to today",
        "title": "river", "cmd": "flow --meander weekly",
        "aria": f"River seen from above, flowing left to right through the year, wider with sharper bends in busy weeks and a dry dotted riverbed in idle weeks, with {wet_weeks} wet weeks and month labels along the banks",
    }
