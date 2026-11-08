"""A space station: a truss with one module docked for each active week. Streaks of three weeks add solar panels."""
import math

from common import W, grid_pos

H = 480
TY = 290
X0, X1 = 70, W - 130


def render(days):
    pos = grid_pos(days)
    nw = max(w for w, _ in pos) + 1
    tot = [0] * nw
    for d, (w, _) in zip(days, pos):
        tot[w] += d["count"]
    top_week = max(tot) or 1
    step = (X1 - X0) / max(1, nw - 1)
    xw = [X0 + (w * step if nw > 1 else (X1 - X0) / 2) for w in range(nw)]
    end = xw[-1] + 40

    # truss: two rails with zigzag braces
    zig, x, up = f"M{X0 - 30} {TY - 5}", X0 - 30, False
    while x < end:
        x = min(end, x + 10)
        zig += f"L{x:.0f} {TY + (-5 if up else 5)}"
        up = not up
    out = [
        f'<path d="M{X0 - 30} {TY - 5}H{end:.0f}M{X0 - 30} {TY + 5}H{end:.0f}" stroke="#fff" stroke-opacity="0.8" stroke-width="1.4"/>',
        f'<path d="{zig}" fill="none" stroke="#fff" stroke-opacity="0.35" stroke-width="1"/>',
    ]

    # solar panels in the gap beside every streak of three or more active weeks
    cols, w = set(), 0
    while w < nw:
        if not tot[w]:
            w += 1
            continue
        e = w
        while e + 1 < nw and tot[e + 1]:
            e += 1
        if e - w + 1 >= 3:
            cols.update((w - 1, e + 1))
        w = e + 1
    pw = min(5, step * 0.22)
    for c in sorted(cols):
        x = X0 + (c * step if nw > 1 else 0)
        if x < X0 - 24 or x > end - 10:
            continue
        lines = "".join(f"M{x - pw:.1f} {TY - 62 + k * 9}h{pw * 2:.1f}" for k in range(1, 14))
        out.append(
            f'<path d="M{x:.1f} {TY - 62}V{TY + 62}" stroke="#fff" stroke-opacity="0.5"/>'
            f'<rect x="{x - pw:.1f}" y="{TY - 62}" width="{pw * 2:.1f}" height="124" fill="#fff" fill-opacity="0.16" stroke="#fff" stroke-opacity="0.6" stroke-width="0.8"/>'
            f'<path d="{lines}" stroke="#fff" stroke-opacity="0.4" stroke-width="0.6"/>'
        )

    # modules: one per active week, alternating above and below the truss
    mods = 0
    for w in range(nw):
        if not tot[w]:
            continue
        mods += 1
        t = math.sqrt(tot[w] / top_week)
        mw = min(36, step * (0.6 + 0.7 * t))
        ln = 24 + t * 64
        sgn = -1 if w % 2 == 0 else 1
        x, op = xw[w], 0.2 + 0.5 * t
        y0 = TY + sgn * 5  # where the module meets the truss
        y1 = y0 + sgn * (4 + ln)
        out.append(
            f'<rect x="{x - 1.5:.1f}" y="{min(y0, y0 + sgn * 4):.1f}" width="3" height="4" fill="#fff" fill-opacity="0.8"/>'
            f'<rect x="{x - mw / 2:.1f}" y="{min(y0 + sgn * 4, y1):.1f}" width="{mw:.1f}" height="{ln:.1f}" fill="#fff" fill-opacity="{op:.2f}" stroke="#fff" stroke-opacity="0.85" stroke-width="1"/>'
            f'<ellipse cx="{x:.1f}" cy="{y1:.1f}" rx="{mw / 2:.1f}" ry="{max(1.2, mw * 0.14):.1f}" fill="#fff" fill-opacity="{op + 0.15:.2f}" stroke="#fff" stroke-opacity="0.85" stroke-width="1"/>'
            f'<path d="M{x - mw / 2:.1f} {(y0 + y1) / 2 + sgn * 4:.1f}h{mw:.1f}" stroke="#fff" stroke-opacity="0.45" stroke-width="0.8"/>'
        )

    # docking port and a small capsule at the newest week
    out.append(
        f'<rect x="{end:.0f}" y="{TY - 8}" width="6" height="16" fill="#fff"/>'
        f'<path d="M{end + 6:.0f} {TY - 6}L{end + 32:.0f} {TY - 9}Q{end + 46:.0f} {TY} {end + 32:.0f} {TY + 9}L{end + 6:.0f} {TY + 6}Z" fill="#fff" fill-opacity="0.4" stroke="#fff" stroke-width="1"/>'
        f'<circle cx="{end + 28:.0f}" cy="{TY}" r="3" fill="#050507" stroke="#fff" stroke-width="0.8"/>'
    )
    total = sum(tot)
    return {
        "w": W, "h": H, "body": "".join(out), "defs": "", "top": TY - 130, "foot": TY + 130,
        "caption": f"{total:,} contributions · {mods} modules · long modules are busier weeks",
        "title": "space-station", "cmd": "dock --last 52w  # a module for every active week",
        "aria": f"A space station with {mods} modules docked along a truss, one for each active week, with solar panels on streaks",
    }
