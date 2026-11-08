"""An obstacle course: every active week is a platform, higher when busier. The runner hops along the course and starts over."""
import math

from common import W, grid_pos

H = 540
START, FADE = 0.8, 0.5  # seconds standing on the first platform, and fading out at the flag
LIFT = 34  # how high a hop rises above the straight line between two platforms


def _pct(sec, total):
    return f"{sec / total * 100:.3f}%"


def _runner_css(plats, hops):
    """Keyframes for the run: one translate keyframe per landing, plus an arc for each hop."""
    hop = 0.7
    total = min(20.0, max(8.0, START + hops * hop + 2.0))
    hop = min(1.2, (total - START - 1.6) / hops)  # long courses speed up, short ones linger at the flag
    land = [START + k * hop for k in range(hops + 1)]
    x0, y0, _ = plats[0]
    run = "".join(
        f"{_pct(t, total)} {{ transform: translate({x - x0:.1f}px, {y - y0:.1f}px); }} "
        for t, (x, y, _) in zip(land, plats)
    )
    first = f"0% {{ transform: translate(0px, 0px); }} "
    arc = "0% { transform: translateY(0); animation-timing-function: cubic-bezier(0.2,0.7,0.4,1); } "
    for k in range(hops):
        mid = (land[k] + land[k + 1]) / 2
        arc += (
            f"{_pct(land[k], total)} {{ transform: translateY(0); animation-timing-function: cubic-bezier(0.2,0.7,0.4,1); }} "
            f"{_pct(mid, total)} {{ transform: translateY({-LIFT}px); animation-timing-function: cubic-bezier(0.6,0,0.8,0.3); }} "
        )
    arc += f"{_pct(land[-1], total)} {{ transform: translateY(0); }} 100% {{ transform: translateY(0); }} "
    fade = (
        f"0% {{ opacity: 0; }} {_pct(0.3, total)} {{ opacity: 1; }} "
        f"{_pct(total - FADE, total)} {{ opacity: 1; }} {_pct(total - 0.1, total)} {{ opacity: 0; }} 100% {{ opacity: 0; }} "
    )
    return (
        f".run {{ animation: obrun {total:.2f}s linear infinite, obfade {total:.2f}s linear infinite; animation-delay: -0.5s; }} "
        f".hop {{ animation: obhop {total:.2f}s linear infinite; animation-delay: -0.5s; }} "
        f"@keyframes obrun {{ {first}{run}100% {{ transform: translate({plats[-1][0] - x0:.1f}px, {plats[-1][1] - y0:.1f}px); }} }} "
        f"@keyframes obhop {{ {arc}}} "
        f"@keyframes obfade {{ {fade}}}"
    )


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
    css = ""
    if plats:
        fx, fy, _ = plats[-1]  # the flag stays on the newest platform
        out.append(f'<path d="M{fx + 26:.1f} {fy:.1f}V{fy - 44:.1f}l14 6l-14 6" fill="none" stroke="#fff" stroke-width="2.5" stroke-linejoin="round"/>')
        # the runner is drawn on the first platform and moved by translate keyframes, one per landing.
        # Without animation it stands on the newest platform, as before.
        x, y, _ = plats[0]
        sprite = (
            f'<g fill="#fff"><rect x="{x + 4:.1f}" y="{y - 36:.1f}" width="12" height="12"/>'
            f'<rect x="{x + 2:.1f}" y="{y - 24:.1f}" width="16" height="14"/>'
            f'<rect x="{x - 3:.1f}" y="{y - 24:.1f}" width="4" height="12"/><rect x="{x + 19:.1f}" y="{y - 24:.1f}" width="4" height="12"/>'
            f'<rect x="{x + 3:.1f}" y="{y - 10:.1f}" width="6" height="10"/><rect x="{x + 11:.1f}" y="{y - 10:.1f}" width="6" height="10"/></g>'
        )
        out.append(
            f'<g class="run" transform="translate({fx - x:.1f} {fy - y:.1f})"><g class="hop">{sprite}</g></g>'
        )
        hops = len(plats) - 1
        if hops:
            css = _runner_css(plats, hops)
    total = sum(d["count"] for d in days)
    return {
        "w": W, "h": H, "body": "".join(out), "defs": "", "foot": base + 18, "top": 100, "css": css,
        "caption": f"{len(plats)} platforms · {total:,} contributions · higher platforms are busier weeks",
        "title": "obby-course", "cmd": "run --last 365d  # a platform for every active week",
        "aria": f"Obstacle course with {len(plats)} platforms, one for each active week, higher when busier",
    }
