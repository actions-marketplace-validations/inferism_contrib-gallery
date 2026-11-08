"""A telescope's light curve: a dot per day, and busier days dip lower, like a planet crossing its star."""
import math
import random

from common import MONTHS, W, peak_of

H = 480
PL, PR, PT, PB = 96, W - 40, 112, 388
YMAX, YMIN = 1.003, 0.983
DEPTH = 0.012


def _y(flux):
    return PT + (YMAX - flux) / (YMAX - YMIN) * (PB - PT)


def render(days):
    n = len(days)
    peak = peak_of(days)
    rnd = random.Random(19)
    span = max(1, n - 1)
    xs = [PL + (i / span if n > 1 else 0.5) * (PR - PL) for i in range(n)]
    depth = [DEPTH * math.sqrt(d["count"] / peak) for d in days]

    out = []
    for f in (1.000, 0.995, 0.990, 0.985):
        y = _y(f)
        dash = ' stroke-dasharray="5 4"' if f == 1.0 else ""
        out.append(
            f'<line x1="{PL}" y1="{y:.1f}" x2="{PR}" y2="{y:.1f}" stroke="#2a2a2d" stroke-width="0.6"{dash}/>'
            f'<path d="M{PL - 5} {y:.1f}h5" stroke="#fff" stroke-opacity="0.6" stroke-width="0.8"/>'
            f'<text x="{PL - 9}" y="{y + 3.5:.1f}" text-anchor="end" class="dim" font-size="10">{f:.3f}</text>'
        )
    out.append(
        f'<path d="M{PL} {PT}V{PB}H{PR}" fill="none" stroke="#fff" stroke-opacity="0.6" stroke-width="0.8"/>'
        f'<text x="{PL - 62}" y="{(PT + PB) / 2:.0f}" text-anchor="middle" class="dim" font-size="11" transform="rotate(-90 {PL - 62} {(PT + PB) / 2:.0f})">normalized flux</text>'
        f'<text x="{(PL + PR) / 2:.0f}" y="{PB + 40}" text-anchor="middle" class="dim" font-size="11">time (months)</text>'
    )
    seen = set()
    for i, d in enumerate(days):
        m = d["date"][:7]
        if m not in seen and d["date"][8:10] <= "07":
            seen.add(m)
            out.append(
                f'<path d="M{xs[i]:.1f} {PB}v5" stroke="#fff" stroke-opacity="0.6" stroke-width="0.8"/>'
                f'<text x="{xs[i]:.1f}" y="{PB + 18}" text-anchor="middle" class="dim" font-size="10">{MONTHS[int(m[5:]) - 1]}</text>'
            )

    bars, dots = [], []
    for i in range(n):
        f = 1 - depth[i] + rnd.gauss(0, 0.0005)
        err = rnd.uniform(0.0005, 0.0011)
        y, ya, yb = _y(f), _y(f + err), _y(f - err)
        bars.append(f"M{xs[i]:.1f} {max(PT, ya):.1f}V{min(PB, yb):.1f}")
        dots.append(f'<circle cx="{xs[i]:.1f}" cy="{min(PB, max(PT, y)):.1f}" r="1.5"/>')
    out.append(f'<path d="{"".join(bars)}" stroke="#fff" stroke-opacity="0.3" stroke-width="0.7" fill="none"/>')
    out.append(f'<g fill="#fff" fill-opacity="0.8">{"".join(dots)}</g>')

    # the fitted line: the dips smoothed over a day or two, drawn as a smooth curve
    sig = 1.6
    fit = []
    for i in range(n):
        lo, hi = max(0, i - 5), min(n, i + 6)
        ws = [math.exp(-((k - i) / sig) ** 2 / 2) for k in range(lo, hi)]
        fit.append((xs[i], _y(1 - sum(w * depth[k] for w, k in zip(ws, range(lo, hi))) / sum(ws))))
    if n > 2:
        d = f"M{fit[0][0]:.1f} {fit[0][1]:.1f}"
        for i in range(1, n - 1):
            mx, my = (fit[i][0] + fit[i + 1][0]) / 2, (fit[i][1] + fit[i + 1][1]) / 2
            d += f"Q{fit[i][0]:.1f} {fit[i][1]:.1f} {mx:.1f} {my:.1f}"
        d += f"L{fit[-1][0]:.1f} {fit[-1][1]:.1f}"
    else:
        d = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in fit)
    out.append(f'<path d="{d}" fill="none" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/>')
    out.append(f'<text x="{PL + 8}" y="{PT - 16}" class="dim" font-size="11">flux vs time · 1 point per day · line is the fit</text>')

    total = sum(d["count"] for d in days)
    dips = sum(1 for v in depth if v > 0)
    return {
        "w": W, "h": H, "body": "".join(out), "defs": "", "top": PT - 36, "foot": PB + 48,
        "caption": f"{total:,} contributions · {dips} transits · busier days dip lower",
        "title": "light-curve", "cmd": "photometry --last 365d  # busier days dip lower",
        "aria": f"A telescope light curve with one point per day of the last year, dipping lower on busier days ({dips} dips)",
    }
