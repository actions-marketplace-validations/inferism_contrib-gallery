"""A farm: every day is a plot. Busy days grow from a seed to a ripe crop."""
from common import W, grid_pos, level, peak_of

H = 330
SYMBOLS = (
    '<symbol id="c1" viewBox="0 0 20 24"><circle cx="10" cy="19" r="2.2"/></symbol>'
    '<symbol id="c2" viewBox="0 0 20 24"><rect x="9.2" y="13" width="1.6" height="9"/>'
    '<ellipse cx="6.5" cy="13" rx="3.6" ry="1.8" transform="rotate(-30 6.5 13)"/>'
    '<ellipse cx="13.5" cy="13" rx="3.6" ry="1.8" transform="rotate(30 13.5 13)"/></symbol>'
    '<symbol id="c3" viewBox="0 0 20 24"><rect x="9.2" y="7" width="1.6" height="15"/>'
    '<ellipse cx="6" cy="10" rx="3.8" ry="1.8" transform="rotate(-30 6 10)"/>'
    '<ellipse cx="14" cy="10" rx="3.8" ry="1.8" transform="rotate(30 14 10)"/>'
    '<ellipse cx="6" cy="16" rx="3.8" ry="1.8" transform="rotate(-30 6 16)"/>'
    '<ellipse cx="14" cy="16" rx="3.8" ry="1.8" transform="rotate(30 14 16)"/></symbol>'
    '<symbol id="c4" viewBox="0 0 20 24"><rect x="9.2" y="9" width="1.6" height="13"/>'
    '<ellipse cx="6" cy="14" rx="3.8" ry="1.8" transform="rotate(-30 6 14)"/>'
    '<ellipse cx="14" cy="14" rx="3.8" ry="1.8" transform="rotate(30 14 14)"/>'
    '<circle cx="10" cy="6" r="4.4"/></symbol>'
)


def render(days):
    peak = peak_of(days)
    pos = grid_pos(days)
    weeks = max(w for w, _ in pos) + 1
    x0, top, row = 28, 100, 30
    cw = (W - 56) / weeks
    out = []
    planted = ripe = 0
    for d, (w, dow) in zip(days, pos):
        x, y = x0 + w * cw, top + dow * row
        out.append(f'<rect x="{x + 1:.1f}" y="{y + 1}" width="{cw - 2:.1f}" height="{row - 2}" rx="2" fill="#1b1b1e"/>')
        lv = level(d["count"], peak)
        if lv:
            planted += 1
            ripe += lv == 4
            out.append(
                f'<use href="#c{lv}" x="{x + 1:.1f}" y="{y + 1}" width="{cw - 2:.1f}" height="{row - 2}" '
                f'fill="#fff" fill-opacity="{0.5 + lv * 0.125:.2f}"/>'
            )
    fy0, fy1 = top - 12, top + 7 * row + 10  # a fence around the field
    posts = "".join(f"M{x} {fy0 - 6}v12M{x} {fy1 - 6}v12" for x in range(28, W - 27, 36))
    out.append(
        f'<path d="M28 {fy0}H{W - 28}M28 {fy1}H{W - 28}{posts}" fill="none" stroke="#9a9aa1" stroke-width="1.5" stroke-linecap="square"/>'
    )
    return {
        "w": W, "h": H, "body": "".join(out), "defs": SYMBOLS, "foot": fy1 + 8, "top": 80,
        "caption": f"{planted} crops planted · {ripe} ready to harvest · bigger crops are busier days",
        "title": "farm-plots", "cmd": "plant --last 365d  # a plot for every day",
        "aria": f"Farm with {planted} planted plots and {ripe} ripe crops over the last year",
    }
