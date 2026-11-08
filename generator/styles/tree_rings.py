"""A cross-section of a tree trunk: one ring per month, oldest in the centre. Thicker rings are busier months."""
import math
import random

from common import MONTHS, W, month_totals, peak_of

H = 730
CX, CY = 500, 396
R_TOTAL, CORE, FLOOR = 262, 9, 7
PTS = 64


def _closed(points):
    """A smooth closed curve through the points, as cubic Bezier segments."""
    n = len(points)
    d = f"M{points[0][0]:.1f} {points[0][1]:.1f}"
    for i in range(n):
        p0, p1, p2, p3 = points[i - 1], points[i], points[(i + 1) % n], points[(i + 2) % n]
        d += (f"C{p1[0] + (p2[0] - p0[0]) / 6:.1f} {p1[1] + (p2[1] - p0[1]) / 6:.1f} "
              f"{p2[0] - (p3[0] - p1[0]) / 6:.1f} {p2[1] - (p3[1] - p1[1]) / 6:.1f} {p2[0]:.1f} {p2[1]:.1f}")
    return d + "Z"


def render(days):
    peak = peak_of(days)
    rnd = random.Random(sum(d["count"] for d in days) * 31 + len(days))
    months = month_totals(days)
    totals = [t for _, t in months]
    n = len(months)
    counts = [[d["count"] for d in days if d["date"][:7] == k] or [0] for k, _ in months]
    phases = [[rnd.uniform(0, math.tau) for _ in range(3)] for _ in range(n + 1)]
    total = sum(totals)

    # ring thickness grows with the month's total, with a floor so quiet months still show a ring
    avail = R_TOTAL - CORE - n * FLOOR
    thick = [FLOOR + (avail * t / total if total else avail / n) for t in totals]
    radii, r = [], CORE
    for t in thick:
        r += t
        radii.append(r)

    def boundary(i, radius, amp_days, bark=False):
        pts = []
        cnt = counts[i] if i < n else [0]
        ph = phases[min(i, n)]
        steps = 80 if bark else PTS
        for k in range(steps):
            th = k / steps * math.tau
            u = th / math.tau * len(cnt)
            a, b = cnt[int(u) % len(cnt)], cnt[(int(u) + 1) % len(cnt)]
            v = (a + (b - a) * (u - int(u))) / peak
            wob = amp_days * v + 1.6 * math.sin(3 * th + ph[0]) + 1.0 * math.sin(7 * th + ph[1]) + 0.6 * math.sin(13 * th + ph[2])
            if bark:
                wob += rnd.uniform(-2.8, 2.8)
            rr = radius + wob
            ox, oy = (i * 0.45, -i * 0.3) if i < n else (n * 0.45, -n * 0.3)  # real trunks grow off-centre
            pts.append((CX + ox + rr * math.cos(th), CY + oy + rr * math.sin(th)))
        return pts

    edges = [boundary(i, radii[i], 4.5) for i in range(n)]
    best = max(range(n), key=lambda i: totals[i]) if total else None
    pmax = max(totals, default=0) or 1

    out = []
    bark_out = boundary(n, radii[-1] + 11, 2.0, bark=True)
    out.append(
        f'<path d="{_closed(bark_out)}{_closed(edges[-1])}" fill-rule="evenodd" class="dim" fill-opacity="0.5" '
        f'stroke="#d4d4d8" stroke-width="1.6" stroke-opacity="0.8"/>'
    )
    for i in reversed(range(n)):
        d = _closed(edges[i]) + (_closed(edges[i - 1]) if i else "")
        op = 0.10 + 0.30 * totals[i] / pmax
        out.append(f'<path d="{d}" fill-rule="evenodd" class="hi" fill-opacity="{op:.2f}" stroke="#d4d4d8" stroke-width="1.2" stroke-opacity="0.6"/>')
        if thick[i] > 14:  # a faint grain line half-way through wide rings
            mid = boundary(i, radii[i] - thick[i] * 0.5, 3.0)
            out.append(f'<path d="{_closed(mid)}" fill="none" stroke="#9a9aa1" stroke-width="0.8" stroke-opacity="0.45"/>')
    out.append(f'<circle cx="{CX}" cy="{CY}" r="3.2" class="hi"/>')

    # radial cracks running in from the bark
    for _ in range(5):
        a = rnd.uniform(0, math.tau)
        length = rnd.uniform(0.18, 0.42) * R_TOTAL
        r0, d = radii[-1] + 14, ""
        ang = a
        for s in range(5):
            r1 = r0 - length / 5
            ang += rnd.uniform(-0.05, 0.05)
            mx = CX + (r0 - length / 10) * math.cos(ang + rnd.uniform(-0.04, 0.04))
            my = CY + (r0 - length / 10) * math.sin(ang + rnd.uniform(-0.04, 0.04))
            if s == 0:
                d = f"M{CX + r0 * math.cos(a):.1f} {CY + r0 * math.sin(a):.1f}"
            d += f"Q{mx:.1f} {my:.1f} {CX + r1 * math.cos(ang):.1f} {CY + r1 * math.sin(ang):.1f}"
            r0 = r1
        out.append(f'<path d="{d}" fill="none" stroke="#0b0b0c" stroke-width="2.2" stroke-linecap="round"/>')

    if best is not None:
        mid_r = radii[best] - thick[best] / 2
        ang = math.radians(-38)
        px, py = CX + best * 0.45 + mid_r * math.cos(ang), CY - best * 0.3 + mid_r * math.sin(ang)
        ex, ey = CX + R_TOTAL + 30, py - 34
        name = MONTHS[int(months[best][0][5:]) - 1]
        out.append(
            f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3.5" class="hi"/>'
            f'<path d="M{px:.1f} {py:.1f}Q{(px + ex) / 2:.1f} {py:.1f} {ex:.1f} {ey:.1f}" fill="none" stroke="#fff" stroke-width="1.3"/>'
            f'<text x="{ex + 6:.1f}" y="{ey + 5:.1f}" class="hi" font-size="15" font-weight="700">best month: {name}</text>'
            f'<text x="{ex + 6:.1f}" y="{ey + 23:.1f}" class="dim" font-size="13">{totals[best]:,} contributions</text>'
        )
    foot = CY + radii[-1] + 30
    return {
        "w": W, "h": H, "body": "".join(out), "defs": "", "foot": foot, "top": 84,
        "caption": f"{n} rings · {total:,} contributions · oldest month at the centre",
        "title": "tree-rings", "cmd": "dendro --cross-section --last 12m",
        "aria": f"Cross-section of a tree trunk with {n} growth rings, one per month with the oldest in the centre, thicker rings for busier months",
    }
