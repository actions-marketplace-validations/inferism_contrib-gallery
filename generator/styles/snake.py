"""A snake that eats its way across the year, one day at a time, and starts over when it reaches the end."""
from common import W, grid_pos, level, peak_of

H = 280
TOP = 100
SEGMENTS = 9
DURATION = 24.0


def render(days):
    peak = peak_of(days)
    pos = grid_pos(days)
    weeks = max(w for w, _ in pos) + 1
    cell = (W - 56) / weeks
    cell_at = {pos[i]: i for i in range(len(days))}

    def center(w, dow):
        return 28 + w * cell + cell / 2, TOP + dow * cell + cell / 2

    order = []  # the snake goes down one week, then back up the next
    for w in range(weeks):
        rows = range(7) if w % 2 == 0 else range(6, -1, -1)
        order += [(w, r) for r in rows if (w, r) in cell_at]
    total_steps = len(order)

    cells = []
    for step, key in enumerate(order):
        c = days[cell_at[key]]["count"]
        x, y = center(*key)
        size = cell - 3
        if c:
            op = 0.45 + level(c, peak) * 0.13
            t = (step + 0.5) / total_steps
            cells.append(
                f'<rect x="{x - size / 2:.1f}" y="{y - size / 2:.1f}" width="{size:.1f}" height="{size:.1f}" rx="3" fill="#fff" fill-opacity="{op:.2f}">'
                f'<animate attributeName="fill-opacity" calcMode="discrete" values="{op:.2f};0.06" keyTimes="0;{t:.4f}" dur="{DURATION}s" repeatCount="indefinite"/></rect>'
            )
        else:
            cells.append(f'<rect x="{x - size / 2:.1f}" y="{y - size / 2:.1f}" width="{size:.1f}" height="{size:.1f}" rx="3" fill="#1b1b1e"/>')

    path = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in (center(*k) for k in order))
    snake = []
    lag = DURATION / total_steps * 1.6
    for k in range(SEGMENTS, -1, -1):  # tail first, so the head is drawn on top
        r = max(3.2, cell / 2 - 1.2 - k * 0.5)
        snake.append(
            f'<circle r="{r:.1f}" fill="#fff" fill-opacity="{1 - k * 0.07:.2f}">'
            f'<animateMotion path="{path}" dur="{DURATION}s" begin="{k * lag:.2f}s" repeatCount="indefinite"/></circle>'
        )
    eaten = sum(1 for d in days if d["count"])
    return {
        "w": W, "h": H, "body": "".join(cells) + "".join(snake), "defs": "", "foot": TOP + 7 * cell + 8, "top": 80,
        "caption": f"{eaten} days to eat · the snake restarts when it reaches today",
        "title": "snake", "cmd": "play --last 365d  # eat every active day",
        "aria": f"A snake eating its way through the {eaten} active days of the last year",
    }
