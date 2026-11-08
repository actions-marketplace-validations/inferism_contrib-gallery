"""A git graph: a main line with a node for every active week, and branches that fork and merge back."""
import random

from common import W, grid_pos

H = 380
MY = 220


def render(days):
    pos = grid_pos(days)
    nw = max(w for w, _ in pos) + 1
    tot = [0] * nw
    for d, (w, _) in zip(days, pos):
        tot[w] += d["count"]
    act = [w for w in range(nw) if tot[w]]
    if not act:
        act = [0]
    rnd = random.Random(33)

    def X(w):
        return 40 + w / max(1, nw - 1) * (W - 80)

    out = [f'<line x1="{X(act[0]):.1f}" y1="{MY}" x2="{X(act[-1]):.1f}" y2="{MY}" stroke="#9a9aa1" stroke-width="2"/>']
    nodes = []
    k = 0
    while k < len(act) - 6:
        if rnd.random() < 0.38:
            span = 2 + int(rnd.random() * 3)
            up = rnd.random() < 0.5
            by = MY + (-1 if up else 1) * (40 + rnd.random() * 40)
            x0, x1 = X(act[k]), X(act[k + span + 1])
            out.append(
                f'<path d="M{x0:.1f} {MY}C{x0 + 10:.1f} {MY},{x0 + 8:.1f} {by:.1f},{x0 + 20:.1f} {by:.1f}'
                f'L{x1 - 20:.1f} {by:.1f}C{x1 - 8:.1f} {by:.1f},{x1 - 10:.1f} {MY},{x1:.1f} {MY}" '
                'fill="none" stroke="#fff" stroke-opacity="0.55" stroke-width="1.6"/>'
            )
            for j in range(1, span + 1):
                nodes.append(
                    f'<circle cx="{x0 + 20 + (x1 - x0 - 40) * j / (span + 1):.1f}" cy="{by:.1f}" r="4" fill="#0b0b0c" stroke="#fff" stroke-width="1.6"/>'
                )
            k += span + 2
        else:
            k += 1
    for w in act:
        nodes.append(f'<circle cx="{X(w):.1f}" cy="{MY}" r="4.5" fill="#fff"/>')
    lx = X(act[-1])
    nodes.append(f'<text x="{lx - 10:.1f}" y="{MY - 18}" text-anchor="end" class="hi" font-size="15">HEAD → main</text>')
    total = sum(d["count"] for d in days)
    return {
        "w": W, "h": H, "body": "".join(out) + "".join(nodes), "defs": "", "foot": MY + 100, "top": 110,
        "caption": f"{len(act)} active weeks · {total:,} contributions · every node is a week you worked",
        "title": "git-graph", "cmd": "git log --graph  # a node for every active week",
        "aria": f"Git graph with a node for each of the {len(act)} active weeks, joined by a main line and branches",
    }
