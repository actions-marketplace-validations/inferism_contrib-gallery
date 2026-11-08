"""Every streak as a block along one year. Long streaks get a label."""
from common import W

H = 280
X0, X1, BAR_Y = 28, W - 28, 170


def render(days):
    counts = [d["count"] for d in days]
    n = len(counts)
    runs, start = [], None
    for i, c in enumerate(counts + [0]):
        if c and start is None:
            start = i
        elif not c and start is not None:
            runs.append((start, i - 1))
            start = None
    best = max((b - a + 1 for a, b in runs), default=0)
    span = X1 - X0
    out = [f'<rect x="{X0}" y="{BAR_Y}" width="{span}" height="22" fill="#1b1b1e"/>']
    for a, b in runs:
        x, w = X0 + a / n * span, max(2.0, (b - a + 1) / n * span)
        long_run = b - a + 1 >= 5
        out.append(f'<rect x="{x:.1f}" y="{BAR_Y}" width="{w:.1f}" height="22" fill="#fff" fill-opacity="{1 if long_run else 0.45}"/>')
        if long_run:
            out.append(f'<text x="{x + w / 2:.1f}" y="{BAR_Y - 10}" text-anchor="middle" class="hi" font-size="14">{b - a + 1}d</text>')
    out.append(
        f'<text x="{(X0 + X1) / 2}" y="104" text-anchor="middle" class="hi" font-size="52" font-weight="700">{best}d</text>'
        f'<text x="{(X0 + X1) / 2}" y="128" text-anchor="middle" class="dim" font-size="15">longest streak</text>'
        f'<text x="{X0}" y="{BAR_Y + 46}" class="dim" font-size="13">12 months ago</text>'
        f'<text x="{X1}" y="{BAR_Y + 46}" text-anchor="end" class="dim" font-size="13">today</text>'
    )
    return {
        "w": W, "h": H, "body": "".join(out), "defs": "", "foot": BAR_Y + 56, "top": 70,
        "caption": f"{len(runs)} streaks · every block is a run of active days",
        "title": "streak-timeline", "cmd": "streaks --last 365d",
        "aria": f"Timeline of {len(runs)} streaks over the last year, the longest lasting {best} days",
    }
