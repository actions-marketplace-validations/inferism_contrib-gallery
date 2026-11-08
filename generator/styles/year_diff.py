"""A unified diff of this year against the same 26 weeks a year earlier (or the first half against the second)."""
from datetime import date

from common import W, esc, grid_pos

ROW, X0, TOP = 17, 28, 112
HUNK = 4
BAR_X, BAR_W = 430, 470


def _weekly(days):
    pos = grid_pos(days)
    n = pos[-1][0] + 1
    totals = [0] * n
    for d, (wk, _) in zip(days, pos):
        totals[wk] += d["count"]
    first = date.fromisoformat(days[0]["date"]).toordinal()
    sunday = first - (date.fromordinal(first).weekday() + 1) % 7
    return totals, sunday


def _span(sunday, wk, n):
    a, b = date.fromordinal(sunday + wk * 7), date.fromordinal(sunday + (wk + n) * 7 - 1)
    return f"{a.isoformat()}..{b.isoformat()}"


def render(days):
    totals, sunday = _weekly(days)
    n = len(totals)
    if n >= 78:   # two years of data: the last 26 weeks against the same weeks a year earlier
        size, new0, old0, mode = 26, n - 26, n - 78, "year"
    else:         # one year: first half against second half
        size = min(26, n // 2)
        new0, old0, mode = n - size, 0, "half"
    pairs = [(totals[old0 + i], totals[new0 + i]) for i in range(size)]
    peak = max((max(p) for p in pairs), default=0) or 1
    ins = sum(b - a for a, b in pairs if b > a)
    dele = sum(a - b for a, b in pairs if b < a)
    old_name = "previous year" if mode == "year" else "first half"
    new_name = "this year" if mode == "year" else "second half"

    out, y = [], TOP

    def line(text, cls="txt", op=None, bg=None, weight=None):
        nonlocal y
        if bg:
            out.append(f'<rect x="0" y="{y - 13}" width="{W}" height="{ROW}" class="hi" fill-opacity="{bg}"/>')
        o = f' fill-opacity="{op}"' if op else ""
        w = f' font-weight="{weight}"' if weight else ""
        out.append(f'<text x="{X0}" y="{y}" class="{cls}" font-size="13"{o}{w} xml:space="preserve">{esc(text)}</text>')
        y += ROW

    line("diff --git a/contributions b/contributions", "hi", weight=700)
    line(f"--- a/contributions  {_span(sunday, old0, size)}  ({old_name})", "dim")
    line(f"+++ b/contributions  {_span(sunday, new0, size)}  ({new_name})", "dim")

    for h in range(0, size, HUNK):
        cnt = min(HUNK, size - h)
        out.append(f'<rect x="0" y="{y - 13}" width="{W}" height="{ROW}" class="hi" fill-opacity="0.07"/>')
        line(f"@@ -W{h + 1},{cnt} +W{h + 1},{cnt} @@", "hi", op="0.8")
        for i in range(h, h + cnt):
            a, b = pairs[i]
            sign = "+" if b > a else "-" if b < a else " "
            when = date.fromordinal(sunday + (new0 + i) * 7)
            if sign == "+":
                out.append(f'<rect x="0" y="{y - 13}" width="{W}" height="{ROW}" class="hi" fill-opacity="0.15"/>')
            elif sign == "-":
                out.append(f'<rect x="0" y="{y - 13}" width="{W}" height="{ROW}" class="dim" fill-opacity="0.14"/>')
            cls = {"+": "hi", "-": "txt", " ": "dim"}[sign]
            out.append(
                f'<text x="{X0}" y="{y}" class="{cls}" font-size="13" xml:space="preserve">{sign} W{i + 1:<2} {when.strftime("%b %d")}</text>'
                f'<text x="290" y="{y}" class="{cls}" font-size="13" text-anchor="end">{b:,}</text>'
                f'<text x="305" y="{y}" class="dim" font-size="13">was {a:,}</text>'
            )
            bw = b / peak * BAR_W
            if bw:
                op = "0.9" if sign == "+" else "0.45"
                out.append(f'<rect x="{BAR_X}" y="{y - 10}" width="{bw:.1f}" height="9" class="hi" fill-opacity="{op}"/>')
            tick = BAR_X + a / peak * BAR_W
            out.append(f'<path d="M{tick:.1f} {y - 12}v13" class="dim" stroke="#9a9aa1" stroke-width="1.5" fill="none"/>')
            if sign != " ":
                out.append(f'<text x="{W - 28}" y="{y}" class="{cls}" font-size="13" text-anchor="end">{b - a:+,}</text>')
            y += ROW

    y += 6
    total = ins + dele
    scale = 24 / total if total else 0
    plus = round(ins * scale)
    minus = round(dele * scale)
    out.append(
        f'<text x="{X0}" y="{y}" class="txt" font-size="13" xml:space="preserve"> contributions | {total:,} '
        f'<tspan class="hi">{"+" * plus}</tspan><tspan class="dim">{"-" * minus}</tspan></text>'
    )
    y += ROW
    out.append(
        f'<text x="{X0}" y="{y}" class="txt" font-size="13" xml:space="preserve"> {size} weeks changed, '
        f'<tspan class="hi">{ins:,} insertions(+)</tspan>, <tspan class="dim">{dele:,} deletions(-)</tspan></text>'
    )
    label = "this year vs the same weeks last year" if mode == "year" else "first half vs second half of the window"
    return {
        "w": W, "h": y + 56, "body": "".join(out), "defs": "", "foot": y + 4, "top": 96,
        "caption": f"{ins:,} insertions(+), {dele:,} deletions(-) · {label}",
        "title": "year-diff", "cmd": f"git diff {days[0]['date'][:4]}..{days[-1]['date'][:4]} -- contributions",
        "aria": f"Unified diff comparing {label}: {size} weeks, {ins:,} contributions gained and {dele:,} lost, with plus lines for weeks that improved and minus lines for weeks that fell short",
    }
