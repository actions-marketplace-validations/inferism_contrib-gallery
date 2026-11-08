"""A chomping circle eats the days one row at a time, left to right and back again."""
from common import W, grid_pos, level, peak_of

H = 320
TOP = 100
ROW = 28
DURATION = 26.0
OPEN = "M0 0L10 -6A11.6 11.6 0 1 0 10 6Z"
SHUT = "M0 0L11.5 -0.8A11.6 11.6 0 1 0 11.5 0.8Z"


def render(days):
    peak = peak_of(days)
    pos = grid_pos(days)
    weeks = max(w for w, _ in pos) + 1
    cw = (W - 56) / weeks
    by_cell = {pos[i]: i for i in range(len(days))}

    def center(w, dow):
        return 28 + w * cw + cw / 2, TOP + dow * ROW

    order = []
    for dow in range(7):  # row by row, alternating direction
        cols = range(weeks) if dow % 2 == 0 else range(weeks - 1, -1, -1)
        order += [(w, dow) for w in cols if (w, dow) in by_cell]
    steps = len(order)

    dots = []
    for step, key in enumerate(order):
        c = days[by_cell[key]]["count"]
        x, y = center(*key)
        if c:
            lv = level(c, peak)
            t = (step + 0.5) / steps
            op = 0.5 + lv * 0.125
            dots.append(
                f'<circle cx="{x:.1f}" cy="{y}" r="{2 + lv * 0.9:.1f}" fill="#fff" fill-opacity="{op:.2f}">'
                f'<animate attributeName="fill-opacity" calcMode="discrete" values="{op:.2f};0" keyTimes="0;{t:.4f}" dur="{DURATION}s" repeatCount="indefinite"/></circle>'
            )
        else:
            dots.append(f'<circle cx="{x:.1f}" cy="{y}" r="1" fill="#2a2a2d"/>')

    path = "M" + "L".join(f"{x:.1f} {y}" for x, y in (center(*k) for k in order))
    pac = (
        f'<path d="{OPEN}" fill="#fff">'
        f'<animate attributeName="d" values="{OPEN};{SHUT};{OPEN}" dur="0.32s" repeatCount="indefinite"/>'
        f'<animateMotion path="{path}" dur="{DURATION}s" rotate="auto" repeatCount="indefinite"/></path>'
    )
    eaten = sum(1 for d in days if d["count"])
    return {
        "w": W, "h": H, "body": "".join(dots) + pac, "defs": "", "foot": TOP + 6 * ROW + 20, "top": 80,
        "caption": f"{eaten} active days to eat · one row at a time",
        "title": "pac-man", "cmd": "chomp --last 365d  # eat every active day",
        "aria": f"A chomping circle eating the {eaten} active days of the last year, row by row",
    }
