"""A memory allocator view: streaks are allocated blocks, gaps are free blocks."""
from common import W, esc

H = 560
X0, X1 = 124, W - 28
PER_ROW, BLOCK_H, PITCH, TOP = 75, 40, 54, 156


def _runs(days):
    """[(start, end_exclusive, active)] for each streak and each gap."""
    runs, i = [], 0
    while i < len(days):
        on = days[i]["count"] > 0
        j = i
        while j < len(days) and (days[j]["count"] > 0) == on:
            j += 1
        runs.append((i, j, on))
        i = j
    return runs


def render(days):
    n = len(days)
    cell = (X1 - X0) / PER_ROW
    runs = _runs(days)
    used = sum(e - s for s, e, on in runs if on)
    gaps = sum(1 for _, _, on in runs if not on)
    allocs = [r for r in runs if r[2]]
    frag = gaps / used * 100 if used else 0.0
    means = {r[0]: sum(d["count"] for d in days[r[0]:r[1]]) / (r[1] - r[0]) for r in allocs}
    top_mean = max(means.values(), default=1) or 1

    out = [
        '<text x="28" y="108" class="dim" font-size="13">==2026== Massif, a heap profiler</text>',
        f'<text x="28" y="126" class="dim" font-size="13">==2026== Command: ./contributions  ({n} blocks of 16 bytes)</text>',
    ]
    rows = (n + PER_ROW - 1) // PER_ROW
    for r in range(rows):
        y = TOP + r * PITCH
        out.append(f'<text x="28" y="{y + 25}" class="dim" font-size="12">0x{r * PER_ROW * 16:05x}</text>')
        out.append(f'<rect x="{X0}" y="{y}" width="{(min(n - r * PER_ROW, PER_ROW)) * cell:.1f}" height="{BLOCK_H}" fill="#1b1b1e" fill-opacity="0.5"/>')

    for s, e, on in runs:
        segs = []
        for r in range(s // PER_ROW, (e - 1) // PER_ROW + 1):
            a, b = max(s, r * PER_ROW), min(e, (r + 1) * PER_ROW)
            segs.append((r, a, b))
        widest = max(segs, key=lambda t: t[2] - t[1])
        for r, a, b in segs:
            x, w, y = X0 + (a - r * PER_ROW) * cell, (b - a) * cell, TOP + r * PITCH
            length = e - s
            if on:
                mean = means[s]
                op = 0.30 + 0.62 * mean / top_mean
                out.append(
                    f'<rect x="{x + .5:.1f}" y="{y + .5}" width="{w - 1:.1f}" height="{BLOCK_H - 1}" class="hi" fill-opacity="{op:.2f}" '
                    f'stroke="#fff" stroke-width="1"><title>{esc(days[s]["date"])} · allocated {length}d, avg {mean:.1f}</title></rect>'
                )
                if a == s:  # the allocator's chunk header
                    out.append(f'<rect x="{x + 1:.1f}" y="{y + 1}" width="{min(3, w - 2):.1f}" height="{BLOCK_H - 2}" fill="#0b0b0c" fill-opacity="0.55"/>')
                label, cls = f"{length}d", ("" if op >= 0.6 else ' class="txt"')
                fill = ' fill="#0b0b0c"' if op >= 0.6 else ""
            else:
                out.append(
                    f'<rect x="{x + .5:.1f}" y="{y + .5}" width="{w - 1:.1f}" height="{BLOCK_H - 1}" fill="none" '
                    f'stroke="#9a9aa1" stroke-width="1" stroke-dasharray="3 3" stroke-opacity="0.6"><title>free {length}d</title></rect>'
                )
                label, cls, fill = f"free {length}d", ' class="dim"', ""
            if (r, a, b) == widest and len(label) * 6.8 + 10 <= w:
                out.append(f'<text x="{x + w / 2:.1f}" y="{y + 25}" font-size="12" text-anchor="middle"{cls}{fill}>{label}</text>')

    y = TOP + rows * PITCH + 26
    free = n - used
    pct = lambda v: f"{v / n * 100:.0f}%" if n else "0%"
    out.append(
        f'<rect x="28" y="{y - 11}" width="16" height="14" class="hi" fill-opacity="0.8" stroke="#fff"/>'
        f'<text x="52" y="{y}" class="txt" font-size="14">used {used}d ({pct(used)})</text>'
        f'<rect x="262" y="{y - 11}" width="16" height="14" fill="none" stroke="#9a9aa1" stroke-dasharray="3 3"/>'
        f'<text x="286" y="{y}" class="txt" font-size="14">free {free}d ({pct(free)})</text>'
        f'<text x="500" y="{y}" class="hi" font-size="14" font-weight="700">fragmentation {frag:.1f}%</text>'
        f'<text x="28" y="{y + 26}" class="dim" font-size="13">{len(allocs)} allocations · {gaps} free blocks / {used} active days = {frag:.1f}% fragmented</text>'
    )
    return {
        "w": W, "h": H, "body": "".join(out), "defs": "", "foot": y + 32, "top": 94,
        "caption": f"{len(allocs)} allocations · {used}d used, {free}d free · {frag:.1f}% fragmentation",
        "title": "heap-map", "cmd": "valgrind --tool=massif",
        "aria": f"Heap map of the year: {len(allocs)} allocated blocks for streaks of active days and {gaps} free blocks for gaps, {used} days used, {free} free, {frag:.1f} percent fragmentation",
    }
