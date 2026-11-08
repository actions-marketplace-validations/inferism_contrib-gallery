"""Two twisting strands with a rung for every active day."""
import math

from common import W, level, peak_of

H = 330
CY, AMP = 200, 78


def render(days):
    peak = peak_of(days)
    n = len(days)
    k = math.tau * 3 / (W - 56)
    x0 = 28

    def y1(x):
        return CY + AMP * math.sin(k * (x - x0))

    a = "M" + "L".join(f"{x} {y1(x):.1f}" for x in range(x0, W - 27, 4))
    b = "M" + "L".join(f"{x} {2 * CY - y1(x):.1f}" for x in range(x0, W - 27, 4))
    rungs = []
    for i, d in enumerate(days):
        if not d["count"]:
            continue
        x = x0 + i / max(1, n - 1) * (W - 56)
        lv = level(d["count"], peak)
        rungs.append(
            f'<line x1="{x:.1f}" y1="{y1(x):.1f}" x2="{x:.1f}" y2="{2 * CY - y1(x):.1f}" stroke="#fff" '
            f'stroke-width="{0.7 + lv * 0.4:.1f}" stroke-opacity="{0.3 + lv * 0.15:.2f}"/>'
        )
    total = sum(d["count"] for d in days)
    return {
        "w": W, "h": H, "body": f'<path d="{a}" fill="none" stroke="#fff" stroke-width="2"/><path d="{b}" fill="none" stroke="#9a9aa1" stroke-width="2"/>' + "".join(rungs),
        "defs": "", "foot": CY + AMP + 14, "top": CY - AMP - 14,
        "caption": f"{len(rungs)} rungs · {total:,} contributions · one rung for every active day",
        "title": "dna-helix", "cmd": "sequence --last 365d",
        "aria": f"DNA helix with {len(rungs)} rungs, one for each active day of the last year",
    }
