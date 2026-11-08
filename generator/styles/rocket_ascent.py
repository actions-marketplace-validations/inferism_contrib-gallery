"""A rocket climbs one flight path. Altitude adds up your contributions, each streak is a burning stage."""
import math
import random

from common import MONTHS, W

H = 520
X0, X1 = 96, W - 70
YB, YT = 440, 140


def _nice(v):
    return f"{v:,}"


def render(days):
    n = len(days)
    total = sum(d["count"] for d in days)
    rnd = random.Random(8)
    span = max(1, n - 1)
    pts, cum = [], 0
    for i, d in enumerate(days):
        cum += d["count"]
        pts.append((X0 + i / span * (X1 - X0), YB - (cum / total if total else 0) * (YB - YT)))

    out = [f'<line x1="{X0 - 30}" y1="{YB}" x2="{X1 + 20}" y2="{YB}" stroke="#2a2a2d" stroke-width="1.5"/>']
    # altitude ticks on the left edge
    marks = [0, 0.25, 0.5, 0.75, 1] if total else [0]
    for f in marks:
        y = YB - f * (YB - YT)
        out.append(
            f'<path d="M{X0 - 30} {y:.1f}h8" stroke="#fff" stroke-opacity="0.5"/>'
            f'<text x="{X0 - 36}" y="{y + 4:.1f}" text-anchor="end" class="dim" font-size="11">{_nice(round(total * f))}</text>'
        )
        if f:
            out.append(f'<line x1="{X0 - 20}" y1="{y:.1f}" x2="{X1 + 20}" y2="{y:.1f}" stroke="#2a2a2d" stroke-dasharray="2 8"/>')
    out.append(f'<text x="{X0 - 30}" y="{YT - 28}" class="dim" font-size="11">altitude (contributions)</text>')
    # month ticks along the ground
    seen = set()
    for i, d in enumerate(days):
        m = d["date"][:7]
        if m not in seen and d["date"][8:10] <= "07":
            seen.add(m)
            out.append(
                f'<path d="M{pts[i][0]:.0f} {YB}v5" stroke="#fff" stroke-opacity="0.4"/>'
                f'<text x="{pts[i][0]:.0f}" y="{YB + 20}" text-anchor="middle" class="dim" font-size="11">{MONTHS[int(m[5:]) - 1]}</text>'
            )

    out.append(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="none" stroke="#fff" stroke-opacity="0.18" stroke-width="1"/>')

    # streaks: thick exhaust segments; a spent stage drops away when one breaks
    i = 0
    while i < n:
        if not days[i]["count"]:
            i += 1
            continue
        j = i
        while j + 1 < n and days[j + 1]["count"]:
            j += 1
        a = pts[i - 1] if i else pts[0]
        seg = " ".join(f"{x:.1f},{y:.1f}" for x, y in ([a] + pts[i:j + 1]))
        out.append(f'<polyline points="{seg}" fill="none" stroke="#fff" stroke-opacity="0.9" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>')
        if j < n - 1:
            x, y = pts[j]
            sx, sy, ang = x + 7 + rnd.uniform(0, 5), y + 16 + rnd.uniform(0, 10), rnd.uniform(-50, 50)
            out.append(
                f'<line x1="{x:.1f}" y1="{y + 3:.1f}" x2="{sx:.1f}" y2="{sy:.1f}" stroke="#fff" stroke-opacity="0.3" stroke-dasharray="1 3"/>'
                f'<rect x="{sx - 2:.1f}" y="{sy - 4:.1f}" width="4" height="8" fill="#fff" fill-opacity="0.55" transform="rotate({ang:.0f} {sx:.1f} {sy:.1f})"/>'
            )
        i = j + 1

    # the rocket at the tip, pointing along the last stretch of the path
    tx, ty = pts[-1]
    k = max(0, n - 15)
    dx, dy = tx - pts[k][0], ty - pts[k][1]
    ang = math.degrees(math.atan2(dy, dx)) if (dx or dy) else 0
    out.append(
        f'<g transform="translate({tx:.1f} {ty:.1f}) rotate({ang:.1f})">'
        '<path d="M-22 0L-10 -5V5Z" fill="#fff" fill-opacity="0.45"/>'  # exhaust
        '<path d="M-12 -6H6Q16 -4 22 0Q16 4 6 6H-12Z" fill="#fff"/>'
        '<path d="M-12 -6L-19 -12V-5ZM-12 6L-19 12V5Z" fill="#fff" fill-opacity="0.75"/>'  # fins
        '<circle cx="3" cy="0" r="2.4" fill="#050507"/></g>'
    )
    stages = sum(1 for k in range(1, n) if days[k]["count"] and not days[k - 1]["count"]) + (1 if n and days[0]["count"] else 0)
    return {
        "w": W, "h": H, "body": "".join(out), "defs": "", "top": YT - 50, "foot": YB + 26,
        "caption": f"{total:,} contributions · {stages} stages · busy stretches climb steeply",
        "title": "rocket-ascent", "cmd": "launch --last 365d  # altitude adds up your contributions",
        "aria": f"A rocket's flight path over the last year, climbing {total:,} contributions high with a stage for each streak",
    }
