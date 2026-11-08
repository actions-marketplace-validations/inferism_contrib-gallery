"""Three activity rings: this week, this month against your best, and your streak against your longest."""
import math

from common import W

H = 450
CX, CY = 270, 245
RINGS = (150, 116, 82)
STROKE = 24


def _streaks(counts):
    best = run = 0
    for c in counts:
        run = run + 1 if c else 0
        best = max(best, run)
    cur = 0
    for c in reversed(counts[:-1] if counts and counts[-1] == 0 else counts):
        if not c:
            break
        cur += 1
    return cur, best


def _arc(r, frac):
    frac = max(0.0, min(0.9995, frac))
    if frac <= 0:
        return ""
    a = -math.pi / 2 + frac * math.tau
    large = 1 if frac > 0.5 else 0
    return f"M{CX} {CY - r}A{r} {r} 0 {large} 1 {CX + r * math.cos(a):.1f} {CY + r * math.sin(a):.1f}"


def render(days):
    counts = [d["count"] for d in days]
    week = sum(1 for c in counts[-7:] if c)
    last30 = sum(counts[-30:])
    best30 = max((sum(counts[i:i + 30]) for i in range(max(1, len(counts) - 29))), default=1) or 1
    cur, best = _streaks(counts)
    fracs = [week / 7, last30 / best30, cur / max(best, 1)]
    out = []
    for r, f, op in zip(RINGS, fracs, (1.0, 0.75, 0.5)):
        out.append(f'<circle cx="{CX}" cy="{CY}" r="{r}" fill="none" stroke="#1b1b1e" stroke-width="{STROKE}"/>')
        d = _arc(r, f)
        if d:
            out.append(f'<path d="{d}" fill="none" stroke="#fff" stroke-opacity="{op}" stroke-width="{STROKE}" stroke-linecap="round"/>')
    out.append(f'<text x="{CX}" y="{CY + 14}" text-anchor="middle" class="hi" font-size="44" font-weight="700">{cur}d</text>')
    out.append(f'<text x="{CX}" y="{CY + 38}" text-anchor="middle" class="dim" font-size="14">streak</text>')
    rows = (
        ("WEEK", f"{week}/7", "active days in the last 7", 1.0),
        ("MONTH", f"{round(last30 / best30 * 100)}%", "of your best 30 days", 0.75),
        ("STREAK", f"{cur}d", f"current streak, longest {best}d", 0.5),
    )
    for i, (name, value, sub, op) in enumerate(rows):
        y = 150 + i * 92
        out.append(
            f'<rect x="560" y="{y - 34}" width="10" height="64" rx="5" fill="#fff" fill-opacity="{op}"/>'
            f'<text x="590" y="{y - 14}" class="dim" font-size="14" letter-spacing="2">{name}</text>'
            f'<text x="590" y="{y + 20}" class="hi" font-size="40" font-weight="700">{value}</text>'
            f'<text x="720" y="{y + 20}" class="dim" font-size="15">{sub}</text>'
        )
    return {
        "w": W, "h": H, "body": "".join(out), "defs": "", "foot": CY + RINGS[0] + 24, "top": 70,
        "caption": f"{sum(counts):,} contributions in the last {len(days)} days",
        "title": "activity-rings", "cmd": "rings --week --month --streak",
        "aria": f"Activity rings: {week} of 7 days this week, {round(last30 / best30 * 100)} percent of your best month, a {cur} day streak",
    }
