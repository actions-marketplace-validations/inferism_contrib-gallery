"""Months as system-monitor bars with percentages."""
from common import BRIGHT, MONTHS, W, month_totals

TICKS, PITCH, BX = 40, 14, 124


def render(days):
    rows = month_totals(days)
    mx = max(v for _, v in rows) or 1
    y0 = 104
    out = []
    for r, (k, v) in enumerate(rows):
        y = y0 + r * 32
        filled = round(v / mx * TICKS)
        out.append(
            f'<text x="28" y="{y}" class="txt" font-size="18">{MONTHS[int(k[5:7]) - 1]}</text>'
            f'<text x="{BX - 16}" y="{y}" class="dim" font-size="20">[</text>'
            + "".join(
                f'<rect x="{BX + i * PITCH}" y="{y - 14}" width="3" height="18" fill="{BRIGHT if i < filled else "#1b1b1e"}"/>'
                for i in range(TICKS)
            )
            + f'<text x="{BX + TICKS * PITCH}" y="{y}" class="dim" font-size="20">]</text>'
            f'<text x="{W - 190}" y="{y}" text-anchor="end" class="hi" font-size="18" font-weight="700">{round(v / mx * 100)}%</text>'
            f'<text x="{W - 40}" y="{y}" text-anchor="end" class="txt" font-size="18">{v}</text>'
        )
    n = len(days)
    active = sum(1 for d in days if d["count"])
    ye = y0 + len(rows) * 32 + 14
    out.append(f'<text x="28" y="{ye + 20}" class="dim" font-size="16">Tasks: {active} active days, {n} total</text>')
    out.append(f'<text x="28" y="{ye + 46}" class="dim" font-size="16">Uptime: {n} days</text>')
    return {
        "w": W, "h": ye + 76, "body": "".join(out), "defs": "",
        "title": "contribution-monitor", "cmd": "htop --contributions",
        "aria": f"Monthly contribution bars for the last {len(rows)} months, {active} active days",
    }
