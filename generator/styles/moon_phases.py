"""Each day is a moon: a new moon when quiet, a full moon when busy. Shows the last 26 weeks."""
from common import W, grid_pos, level, peak_of

H = 420
WEEKS_SHOWN = 26
R, SP = 13, 35


def render(days):
    peak = peak_of(days)
    pos = grid_pos(days)
    weeks = max(w for w, _ in pos) + 1
    first = weeks - WEEKS_SHOWN
    x0, top = (W - WEEKS_SHOWN * SP) / 2 + SP / 2, 110
    out = []
    for d, (w, dow) in zip(days, pos):
        if w < first:
            continue
        x, y = x0 + (w - first) * SP, top + dow * SP
        f = level(d["count"], peak) / 4
        out.append(f'<circle cx="{x:.1f}" cy="{y}" r="{R}" fill="#111113" stroke="#2a2a2d" stroke-width="1"/>')
        if f >= 1:
            out.append(f'<circle cx="{x:.1f}" cy="{y}" r="{R}" fill="#fff"/>')
        elif f > 0:
            rx = R * abs(1 - 2 * f)
            out.append(
                f'<path d="M{x:.1f} {y - R}A{R} {R} 0 0 1 {x:.1f} {y + R}A{rx:.2f} {R} 0 0 {1 if f < 0.5 else 0} {x:.1f} {y - R}Z" fill="#fff"/>'
            )
    recent = [d for d, (w, _) in zip(days, pos) if w >= first]
    total = sum(d["count"] for d in recent)
    return {
        "w": W, "h": H, "body": "".join(out), "defs": "", "foot": top + 6 * SP + R + 8, "top": 90,
        "caption": f"the last {WEEKS_SHOWN} weeks · {total:,} contributions · a full moon is a busy day",
        "title": "moon-phases", "cmd": "phases --last 26w",
        "aria": f"Moon phases for each day of the last {WEEKS_SHOWN} weeks, fuller moons for busier days",
    }
