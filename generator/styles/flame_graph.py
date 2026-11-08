"""A profiler flame graph: year at the bottom, then months, weeks and days. Width is the share of contributions."""
from common import MONTHS, W, esc, grid_pos, level, peak_of

H = 380
X0, X1 = 28, W - 28
ROW, TOP = 40, 132  # row height and y of the top (day) row; the year bar is the bottom row
CHAR = 7.3          # rough width of one character at font-size 12


def _pick(labels, width):
    """The first label that fits inside a bar, or None."""
    for text in labels:
        if len(text) * CHAR + 10 <= width:
            return text
    return None


def _bar(x, w, row, label, tip, op):
    y = TOP + row * ROW
    out = (
        f'<rect x="{x:.2f}" y="{y}" width="{max(w, 0.4):.2f}" height="{ROW - 2}" class="hi" fill-opacity="{op:.2f}" '
        f'stroke="#0b0b0c" stroke-width="1"><title>{esc(tip)}</title></rect>'
    )
    if label:
        out += f'<text x="{x + 5:.2f}" y="{y + 24}" font-size="12" fill="#0b0b0c" pointer-events="none">{esc(label)}</text>'
    return out


def render(days):
    total = sum(d["count"] for d in days)
    pos = grid_pos(days)
    out = [
        f'<text x="{X0}" y="108" class="dim" font-size="13">Flame Graph</text>',
        f'<rect x="{W - 250}" y="94" width="108" height="20" rx="3" fill="none" stroke="#2a2a2d"/>'
        f'<text x="{W - 196}" y="108" class="dim" font-size="12" text-anchor="middle">Reset Zoom</text>'
        f'<rect x="{W - 134}" y="94" width="106" height="20" rx="3" fill="none" stroke="#2a2a2d"/>'
        f'<text x="{W - 81}" y="108" class="dim" font-size="12" text-anchor="middle">Search</text>',
    ]
    bottom = TOP + 3 * ROW
    if total:
        scale = (X1 - X0) / total
        months = {}
        for d, (wk, _) in zip(days, pos):
            if d["count"]:
                months.setdefault(d["date"][:7], {}).setdefault(wk, []).append(d)
        peak = peak_of(days)
        x = X0
        out.append(_bar(X0, X1 - X0, 3, _pick([f"all · {total:,}", "all"], X1 - X0), f"all ({total:,} contributions, 100%)", 0.9))
        for mi, key in enumerate(sorted(months)):
            weeks = months[key]
            mt = sum(d["count"] for ds in weeks.values() for d in ds)
            mw = mt * scale
            name = f"{MONTHS[int(key[5:]) - 1]}"
            out.append(_bar(x, mw, 2, _pick([f"{name} {key[:4]} · {mt:,}", f"{name} · {mt:,}", name], mw),
                            f"{name} {key[:4]} ({mt:,} contributions, {mt / total:.1%})", 0.62 + 0.18 * (mi % 2)))
            wx = x
            for wi, wk in enumerate(sorted(weeks)):
                ds = weeks[wk]
                wt = sum(d["count"] for d in ds)
                ww = wt * scale
                out.append(_bar(wx, ww, 1, _pick([f"w{wk + 1} · {wt}", f"w{wk + 1}"], ww),
                                f"week {wk + 1} ({wt} contributions)", 0.6 + 0.2 * ((wi + mi) % 2)))
                dx = wx
                for d in ds:
                    dw = d["count"] * scale
                    out.append(_bar(dx, dw, 0, _pick([str(d["count"])], dw), f'{d["date"]} ({d["count"]} contributions)',
                                    0.45 + 0.1 * level(d["count"], peak)))
                    dx += dw
                wx += ww
            x += mw
    else:
        out.append(_bar(X0, X1 - X0, 3, "all · 0", "all (0 contributions)", 0.9))
    out.append(f'<text x="{X0}" y="{bottom + 52}" class="dim" font-size="13">Function: all ({total:,} samples, 100%)</text>')
    return {
        "w": W, "h": H, "body": "".join(out), "defs": "", "foot": bottom + 56, "top": 94,
        "caption": f"{total:,} samples · bar width is share of contributions, quiet stretches squeeze out",
        "title": "flame-graph", "cmd": "perf script | flamegraph.pl",
        "aria": f"Flame graph of the year with {total:,} contributions: the year at the bottom, then months, weeks and days stacked above it, each as wide as its share",
    }
