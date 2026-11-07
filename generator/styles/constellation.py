"""Active days are stars. Days close together join into constellations."""
import random

from common import W, grid_pos, peak_of, starfield

H = 400


def render(days):
    peak = peak_of(days)
    rnd = random.Random(3)
    pos = grid_pos(days)
    out = [starfield(W, H, 3, 150)]
    pts = []
    for i, (d, (w, dow)) in enumerate(zip(days, pos)):
        if d["count"] == 0:
            continue
        x = 28 + w / 52 * (W - 56) + (rnd.random() - 0.5) * 6
        y = 112 + dow / 6 * (H - 176) + (rnd.random() - 0.5) * 9
        pts.append((i, x, y, d["count"]))
    for (i0, x0, y0, _), (i1, x1, y1, _) in zip(pts, pts[1:]):
        if i1 - i0 <= 3:
            out.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="#fff" stroke-opacity="0.3"/>')
    for k, (_, x, y, c) in enumerate(pts):
        tw = f' class="tw" style="animation-delay:-{rnd.uniform(0, 4):.1f}s"' if k % 2 == 0 else ""
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{1.3 + c / peak * 4.2:.1f}" fill="#fff"{tw}/>')
    total = sum(d["count"] for d in days)
    out.append(f'<text x="28" y="{H - 22}" class="dim" font-size="15">{len(pts)} active days · {total:,} contributions · peak {peak}/day</text>')
    return {
        "w": W, "h": H, "body": "".join(out), "defs": "",
        "title": "constellation", "cmd": "render-sky --last 365d  # active days as stars",
        "aria": f"Constellation of {len(pts)} active days over the last year",
    }
