"""A piano roll: weekdays are keys, weeks run left to right, active days are notes."""
from common import W, grid_pos, level, peak_of

H = 380
DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]


def render(days):
    peak = peak_of(days)
    pos = grid_pos(days)
    weeks = max(w for w, _ in pos) + 1
    top, row = 104, 34
    kx, kw = 28, 76
    x0, x1 = 118, W - 28
    cw = (x1 - x0) / weeks
    out = []
    for r in range(7):
        y = top + r * row
        if r % 2 == 0:
            out.append(f'<rect x="{x0}" y="{y}" width="{x1 - x0}" height="{row}" fill="#111113"/>')
        out.append(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="#2a2a2d" stroke-width="1"/>')
    out.append(f'<line x1="{x0}" y1="{top + 7 * row}" x2="{x1}" y2="{top + 7 * row}" stroke="#2a2a2d" stroke-width="1"/>')
    for w in range(0, weeks, 4):
        x = x0 + w * cw
        out.append(f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{top + 7 * row}" stroke="#2a2a2d" stroke-width="1"/>')
    for r in range(7):  # white keys with their labels
        y = top + r * row
        out.append(
            f'<rect x="{kx}" y="{y + 1}" width="{kw}" height="{row - 2}" rx="2" fill="#d4d4d8"/>'
            f'<text x="{kx + kw - 8}" y="{y + row / 2 + 4:.1f}" text-anchor="end" font-size="12" fill="#0b0b0c">{DAYS[r]}</text>'
        )
    for r in (1, 2, 4, 5, 6):  # black keys sit between the white ones
        y = top + r * row
        out.append(f'<rect x="{kx}" y="{y - 9}" width="46" height="18" rx="2" fill="#0b0b0c" stroke="#2a2a2d" stroke-width="1"/>')
    active = 0
    for d, (w, dow) in zip(days, pos):
        c = d["count"]
        if not c:
            continue
        active += 1
        lv = level(c, peak)
        wd = max(4.0, cw * (0.5 + lv * 0.12))
        out.append(
            f'<rect x="{x0 + w * cw + 1:.1f}" y="{top + dow * row + 6}" width="{wd:.1f}" height="{row - 12}" rx="3" '
            f'fill="#fff" fill-opacity="{0.4 + lv * 0.15:.2f}"/>'
        )
    total = sum(d["count"] for d in days)
    out.append(f'<text x="28" y="{H - 22}" class="dim" font-size="15">{active} notes · {total:,} contributions · longer notes are busier days</text>')
    return {
        "w": W, "h": H, "body": "".join(out), "defs": "",
        "title": "piano-roll", "cmd": "play --last 365d  # weekdays are keys, weeks go left to right",
        "aria": f"Piano roll with {active} notes for the active days of the last year",
    }
