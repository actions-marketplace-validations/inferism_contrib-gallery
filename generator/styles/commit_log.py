"""Your ten busiest days, sorted like terminal output."""
from datetime import date

from common import W

H = 560
TICKS, PITCH, BX = 38, 13, 340


def render(days):
    ranked = sorted((d for d in days if d["count"]), key=lambda d: (-d["count"], d["date"]))[:10]
    peak = ranked[0]["count"] if ranked else 1
    out = []
    for i, d in enumerate(ranked):
        y = 116 + i * 38
        filled = round(d["count"] / peak * TICKS)
        when = date.fromisoformat(d["date"])
        out.append(
            f'<text x="28" y="{y}" class="dim" font-size="15">{i + 1:>2}</text>'
            f'<text x="130" y="{y}" text-anchor="end" class="hi" font-size="24" font-weight="700">{d["count"]}</text>'
            f'<text x="152" y="{y}" class="txt" font-size="18">{d["date"]}</text>'
            f'<text x="268" y="{y}" class="dim" font-size="15">{when.strftime("%a")}</text>'
            + "".join(
                f'<rect x="{BX + t * PITCH}" y="{y - 15}" width="4" height="20" fill="{"#fff" if t < filled else "#1b1b1e"}"/>'
                for t in range(TICKS)
            )
        )
    active = sum(1 for d in days if d["count"])
    return {
        "w": W, "h": H, "body": "".join(out), "defs": "", "foot": 116 + max(0, len(ranked) - 1) * 38 + 14, "top": 96,
        "caption": f"top {len(ranked)} of {active} active days · contributions on the left",
        "title": "commit-log", "cmd": "sort --busiest --last 365d | head -10",
        "aria": f"The {len(ranked)} busiest days of the last year, busiest first, with {peak} contributions on the best day",
    }
