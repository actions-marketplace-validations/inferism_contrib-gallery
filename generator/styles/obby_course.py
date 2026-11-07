"""An obstacle course: every active week is a platform, higher when busier, with a runner at the end."""
import math

from common import W, grid_pos

H = 540


def render(days):
    pos = grid_pos(days)
    nw = max(w for w, _ in pos) + 1
    tot = [0] * nw
    for d, (w, _) in zip(days, pos):
        tot[w] += d["count"]
    top_week = max(tot) or 1
    step = (W - 100) / max(1, nw - 1)
    base = 470

    studs = "".join(f"M{x}{base - 4}h8v4h-8z" for x in range(36, W - 40, 22))
    out = [
        f'<rect x="28" y="{base}" width="{W - 56}" height="16" fill="#fff" fill-opacity="0.16"/>',
        f'<path d="{studs}" fill="#fff" fill-opacity="0.16"/>',
    ]
    plats = []
    for w in range(nw):
        if not tot[w]:
            continue
        t = math.sqrt(tot[w] / top_week)
        plats.append((50 + w * step, base - 46 - t * 300, t))
    for x, y, t in plats:
        out.append(
            f'<line x1="{x + 10:.1f}" y1="{y + 12:.1f}" x2="{x + 10:.1f}" y2="{base}" stroke="#2a2a2d" stroke-width="1.5" stroke-dasharray="2 5"/>'
            f'<rect x="{x:.1f}" y="{y:.1f}" width="20" height="12" fill="#fff" fill-opacity="{0.4 + t * 0.55:.2f}"/>'
            f'<path d="M{x + 3:.1f} {y - 3:.1f}h5v3h-5zM{x + 12:.1f} {y - 3:.1f}h5v3h-5z" fill="#fff" fill-opacity="{0.4 + t * 0.55:.2f}"/>'
        )
    if plats:  # the runner on the newest platform
        x, y, _ = plats[-1]
        out.append(
            f'<g fill="#fff"><rect x="{x + 4:.1f}" y="{y - 36:.1f}" width="12" height="12"/>'
            f'<rect x="{x + 2:.1f}" y="{y - 24:.1f}" width="16" height="14"/>'
            f'<rect x="{x - 3:.1f}" y="{y - 24:.1f}" width="4" height="12"/><rect x="{x + 19:.1f}" y="{y - 24:.1f}" width="4" height="12"/>'
            f'<rect x="{x + 3:.1f}" y="{y - 10:.1f}" width="6" height="10"/><rect x="{x + 11:.1f}" y="{y - 10:.1f}" width="6" height="10"/></g>'
            f'<path d="M{x + 26:.1f} {y:.1f}V{y - 44:.1f}l14 6l-14 6" fill="none" stroke="#fff" stroke-width="2.5" stroke-linejoin="round"/>'
        )
    total = sum(d["count"] for d in days)
    return {
        "w": W, "h": H, "body": "".join(out), "defs": "", "foot": base + 18, "top": 100,
        "caption": f"{len(plats)} platforms · {total:,} contributions · higher platforms are busier weeks",
        "title": "obby-course", "cmd": "run --last 365d  # a platform for every active week",
        "aria": f"Obstacle course with {len(plats)} platforms, one for each active week, higher when busier",
    }
