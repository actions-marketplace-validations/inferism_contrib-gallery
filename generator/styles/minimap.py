"""A code editor with its scroll minimap: one line per day, line length is the count, the viewport sits on the latest 30 days."""
from datetime import date

from common import MONTHS, W, esc, grid_pos, level, peak_of

PITCH, VIEW = 1.5, 30
X0, X1 = 28, W - 28
MM_X, MM_W = 724, 236
TAB_Y, BODY_Y = 96, 130
INDENT = [0, 1, 2, 1, 0, 1, 2, 2]  # indentation level by week, so the lines look like nested code


def render(days):
    n = len(days)
    peak = peak_of(days)
    pos = grid_pos(days)
    body_h = max(n * PITCH, VIEW * 18)
    view_n = min(VIEW, n)
    epitch = body_h / VIEW
    out = [
        f'<rect x="{X0}" y="{TAB_Y}" width="{X1 - X0}" height="{BODY_Y + body_h + 34 - TAB_Y}" rx="6" fill="none" stroke="#2a2a2d"/>',
        f'<rect x="{X0}" y="{TAB_Y}" width="170" height="28" class="hi" fill-opacity="0.08"/>'
        f'<path d="M{X0} {TAB_Y + 28}H{X1}" stroke="#2a2a2d"/>'
        f'<circle cx="{X0 + 16}" cy="{TAB_Y + 14}" r="3.5" class="hi"/>'
        f'<text x="{X0 + 28}" y="{TAB_Y + 19}" class="hi" font-size="13">contributions.ts</text>'
        f'<text x="{X0 + 190}" y="{TAB_Y + 19}" class="dim" font-size="13">README.md</text>',
        f'<path d="M{MM_X - 12} {BODY_Y}V{BODY_Y + body_h}" stroke="#2a2a2d"/>',
    ]

    # the minimap: one 1px line per day, split in two so it reads like keyword + identifier
    last_month = ""
    for i, d in enumerate(days):
        y = BODY_Y + i * PITCH
        if d["date"][:7] != last_month:
            last_month = d["date"][:7]
            out.append(f'<text x="{MM_X - 20}" y="{y + 7:.1f}" class="dim" font-size="10" text-anchor="end">{MONTHS[int(last_month[5:]) - 1]}</text>')
        c = d["count"]
        if not c:
            continue
        x = MM_X + INDENT[pos[i][0] % 8] * 8
        length = max(4.0, c / peak * (MM_W - 24))
        op = f"{0.38 + 0.14 * level(c, peak):.2f}"
        head = min(length * 0.35, 28)
        out.append(
            f'<rect x="{x}" y="{y:.1f}" width="{head:.1f}" height="1.1" class="hi" fill-opacity="{op}"/>'
            f'<rect x="{x + head + 2:.1f}" y="{y:.1f}" width="{max(length - head - 2, 1):.1f}" height="1.1" class="txt" fill-opacity="{op}"/>'
        )

    # the viewport box on the latest days
    vy = BODY_Y + (n - view_n) * PITCH
    out.append(
        f'<rect x="{MM_X - 6}" y="{vy:.1f}" width="{MM_W + 12}" height="{max(view_n * PITCH, 4):.1f}" class="hi" fill-opacity="0.14" stroke="#fff" stroke-width="1"/>'
        f'<rect x="{X1 - 8}" y="{vy:.1f}" width="4" height="{max(view_n * PITCH, 4):.1f}" class="hi" fill-opacity="0.7"/>'
    )

    # the editor itself, showing the same latest days as readable code
    for k in range(view_n):
        i = n - view_n + k
        d, c = days[i], days[i]["count"]
        y = BODY_Y + k * epitch
        base = y + epitch * 0.68
        x = 96 + INDENT[pos[i][0] % 8] * 22
        if k == view_n - 1:
            out.append(f'<rect x="{X0 + 1}" y="{y:.1f}" width="{MM_X - 14 - X0}" height="{epitch:.1f}" class="hi" fill-opacity="0.07"/>')
        shown = date.fromisoformat(d["date"]).strftime("%b %d")
        code = (
            f'<tspan class="hi">contribute</tspan><tspan class="txt">({c});</tspan><tspan class="dim">  // {esc(shown)}</tspan>'
            if c else f'<tspan class="dim">// {esc(shown)} idle</tspan>'
        )
        out.append(
            f'<text x="{X0 + 52}" y="{base:.1f}" class="dim" font-size="12" text-anchor="end">{i + 1}</text>'
            f'<text x="{x}" y="{base:.1f}" font-size="14" xml:space="preserve">{code}</text>'
        )
    ey = BODY_Y + (view_n - 1) * epitch
    caret_x = 96 + INDENT[pos[-1][0] % 8] * 22 + (len(f"contribute({days[-1]['count']});  // Nov 07") if days[-1]["count"] else len("// Nov 07 idle")) * 8.4 + 2
    out.append(f'<rect x="{caret_x:.1f}" y="{ey + 2:.1f}" width="2" height="{epitch - 4:.1f}" class="hi blink"/>')

    sb = BODY_Y + body_h + 8
    total = sum(d["count"] for d in days)
    out.append(
        f'<path d="M{X0} {sb - 6}H{X1}" stroke="#2a2a2d"/>'
        f'<text x="{X0 + 14}" y="{sb + 14}" class="dim" font-size="12">Ln {n}, Col 1</text>'
        f'<text x="{X1 - 14}" y="{sb + 14}" class="dim" font-size="12" text-anchor="end">Spaces: 2   UTF-8   TypeScript</text>'
    )
    return {
        "w": W, "h": int(sb + 14 + 56), "body": "".join(out), "defs": "", "foot": sb + 20, "top": 94,
        "caption": f"{n} lines · {total:,} contributions · viewport on the latest {view_n} days",
        "title": "minimap", "cmd": "code contributions.ts",
        "aria": f"Code editor minimap with one line for each of the {n} days, longer lines for busier days, and a highlighted viewport over the latest {view_n} days",
    }
