"""The usual contribution grid, drawn with text characters like command output."""
from common import W, grid_pos, level, peak_of

H = 320
CHARS = ["·", "░", "▒", "▓", "█"]
DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]


def render(days):
    peak = peak_of(days)
    pos = grid_pos(days)
    weeks = max(w for w, _ in pos) + 1
    x0, top, row = 76, 116, 28
    cw = (W - 28 - x0) / weeks
    out = [f'<text x="28" y="{top + r * row}" class="dim" font-size="14">{DAYS[r]}</text>' for r in range(7)]
    for d, (w, dow) in zip(days, pos):
        lv = level(d["count"], peak)
        cls = "dim" if lv == 0 else "hi"
        op = "" if lv == 0 else f' fill-opacity="{0.4 + lv * 0.15:.2f}"'
        out.append(f'<text x="{x0 + w * cw + cw / 2:.1f}" y="{top + dow * row}" text-anchor="middle" class="{cls}" font-size="20"{op}>{CHARS[lv]}</text>')
    legend = "less · ░ ▒ ▓ █ more"
    total = sum(d["count"] for d in days)
    return {
        "w": W, "h": H, "body": "".join(out), "defs": "", "foot": top + 6 * row + 14, "top": 96,
        "caption": f"{total:,} contributions · {legend}",
        "title": "terminal-heatmap", "cmd": "cat contributions.txt",
        "aria": f"Contribution grid drawn with text characters, {total:,} contributions over the last year",
    }
