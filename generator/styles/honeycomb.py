"""A hive: one hexagonal cell per day in week columns. The honey level in each cell is the day's count against the peak."""
import math

from common import W, grid_pos, peak_of

R = 22
SQ = math.sqrt(3)
TOP, BAND_GAP = 104, 30
CSS = ".bee { animation: bob 2.6s ease-in-out infinite; } @keyframes bob { 50% { transform: translateY(-4px); } }"


def _hex(cx, cy, r):
    return [(cx + r * math.cos(math.radians(60 * k)), cy + r * math.sin(math.radians(60 * k))) for k in range(6)]


def _below(poly, y):
    """The part of a polygon at or under a horizontal line (y grows downward)."""
    out = []
    for i, a in enumerate(poly):
        b = poly[(i + 1) % len(poly)]
        ina, inb = a[1] >= y, b[1] >= y
        if ina:
            out.append(a)
        if ina != inb:
            t = (y - a[1]) / (b[1] - a[1])
            out.append((a[0] + (b[0] - a[0]) * t, y))
    return out


def _pts(poly):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in poly)


def _bee(x, y, s, delay):
    return (
        f'<g class="bee" style="animation-delay:-{delay:.1f}s"><g transform="translate({x:.1f} {y:.1f}) scale({s})">'
        '<ellipse cx="-1" cy="-6.5" rx="5" ry="2.6" transform="rotate(-25 -1 -6.5)" class="txt" fill-opacity="0.75" stroke="#0b0b0c" stroke-width="0.8"/>'
        '<ellipse cx="3" cy="-6.5" rx="5" ry="2.6" transform="rotate(20 3 -6.5)" class="txt" fill-opacity="0.75" stroke="#0b0b0c" stroke-width="0.8"/>'
        '<ellipse cx="0" cy="0" rx="8" ry="5" class="hi" stroke="#0b0b0c" stroke-width="1.6"/>'
        '<path d="M-1 -4.6Q1.5 0 -1 4.6M3.5 -4.2Q5.5 0 3.5 4.2" fill="none" stroke="#0b0b0c" stroke-width="1.8"/>'
        '<circle cx="-8.6" cy="0" r="3" class="hi" stroke="#0b0b0c" stroke-width="1.2"/>'
        '<path d="M8 0q3 0 4.5 1.6" fill="none" stroke="#0b0b0c" stroke-width="1.4" stroke-linecap="round"/>'
        '</g></g>'
    )


def render(days):
    peak = peak_of(days)
    pos = grid_pos(days)
    nw = max(w for w, _ in pos) + 1
    nc = (nw + 1) // 2
    band_w = (nc - 1) * 1.5 * R + 2 * R
    bx = (W - band_w) / 2
    band_h = 7 * SQ * R + SQ / 2 * R
    tot = [0] * nw
    out = []

    def centre(w, row):
        band, c = divmod(w, nc)
        cx = bx + R + 1.5 * R * c
        cy = TOP + band * (band_h + BAND_GAP) + SQ / 2 * R + SQ * R * row + (SQ / 2 * R if c % 2 else 0)
        return cx, cy

    active = 0
    for d, (w, row) in zip(days, pos):
        tot[w] += d["count"]
        cx, cy = centre(w, row)
        c = d["count"]
        wall = _hex(cx, cy, R - 1.2)
        if not c:  # an open cell
            out.append(
                f'<polygon points="{_pts(wall)}" fill="#0b0b0c" fill-opacity="0.55" stroke="#9a9aa1" stroke-width="1.3" stroke-opacity="0.75"/>'
                f'<polygon points="{_pts(_hex(cx, cy, R * 0.66))}" fill="none" stroke="#9a9aa1" stroke-width="0.8" stroke-opacity="0.35"/>'
            )
            continue
        active += 1
        frac = max(0.12, c / peak)
        inner = _hex(cx, cy, R * 0.82)
        ytop = cy + SQ / 2 * R * 0.82 * (1 - 2 * frac)
        honey = _below(inner, ytop)
        out.append(
            f'<polygon points="{_pts(wall)}" fill="#0b0b0c" fill-opacity="0.55" stroke="#fff" stroke-width="1.4" stroke-opacity="0.7"/>'
            f'<polygon points="{_pts(honey)}" class="hi" fill-opacity="{0.45 + 0.5 * frac:.2f}"><title>{d["date"]}: {c}</title></polygon>'
        )
        if frac < 0.995:  # the honey line, with a slight meniscus
            xs = [p[0] for p in honey if abs(p[1] - ytop) < 0.01]
            if len(xs) >= 2:
                out.append(f'<path d="M{min(xs):.1f} {ytop:.1f}Q{(min(xs) + max(xs)) / 2:.1f} {ytop - 2.2:.1f} {max(xs):.1f} {ytop:.1f}" fill="none" stroke="#fff" stroke-width="1.2"/>')

    total = sum(tot)
    if total:  # bees hover over the column of the busiest week
        w = max(range(nw), key=lambda k: (tot[k], -k))
        band, c = divmod(w, nc)
        x = bx + R + 1.5 * R * c
        y0 = TOP + band * (band_h + BAND_GAP)
        for k, (dx, row, s) in enumerate(((-30, 1.0, 1.9), (18, 3.0, 2.2), (-10, 5.1, 1.8))):
            bxp, byp = x + dx, y0 + row * SQ * R
            out.append(f'<path d="M{bxp - 46:.1f} {byp + 12:.1f}Q{bxp - 24:.1f} {byp - 14:.1f} {bxp - 12:.1f} {byp:.1f}" fill="none" stroke="#fff" stroke-width="1.2" stroke-dasharray="1 5" stroke-linecap="round" stroke-opacity="0.8"/>')
            out.append(_bee(bxp, byp, s, k * 0.9))
    foot = TOP + 2 * band_h + BAND_GAP
    return {
        "w": W, "h": int(foot + 70), "body": "".join(out), "defs": "", "css": CSS, "foot": foot + 6, "top": 90,
        "caption": f"{active} filled cells · {len(days) - active} open · {total:,} contributions · bees over the busiest week",
        "title": "honeycomb", "cmd": "apiary inspect --hive",
        "aria": f"Honeycomb with a hexagonal cell for each of the {len(days)} days in week columns, honey level showing the day's count against the peak, open cells for empty days and bees over the busiest week",
    }
