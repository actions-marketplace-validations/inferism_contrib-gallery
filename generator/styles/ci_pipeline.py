"""A CI run view: one stage per month as connected chips. Busy months pass, slow ones warn, empty ones fail."""
from statistics import median

from common import MONTHS, W, esc, month_totals

H = 430
CW, CH, GAP = 60, 126, 20
X0, Y0 = 30, 214


def _icon(cx, cy, r, status):
    if status == "pass":
        return (f'<circle cx="{cx}" cy="{cy}" r="{r}" class="hi"/>'
                f'<path d="M{cx - r * .42:.1f} {cy + r * .02:.1f}l{r * .3:.1f} {r * .32:.1f}l{r * .55:.1f} {-r * .62:.1f}" fill="none" '
                f'stroke="#0b0b0c" stroke-width="{r * .22:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')
    if status == "warn":
        return (f'<circle cx="{cx}" cy="{cy}" r="{r - 1}" fill="none" stroke="#fff" stroke-width="2"/>'
                f'<path d="M{cx} {cy - r * .5:.1f}v{r * .55:.1f}M{cx} {cy + r * .45:.1f}v.1" fill="none" stroke="#fff" '
                f'stroke-width="{r * .2:.1f}" stroke-linecap="round"/>')
    k = r * .38
    return (f'<circle cx="{cx}" cy="{cy}" r="{r - 1}" fill="none" stroke="#9a9aa1" stroke-width="2"/>'
            f'<path d="M{cx - k:.1f} {cy - k:.1f}l{2 * k:.1f} {2 * k:.1f}M{cx + k:.1f} {cy - k:.1f}l{-2 * k:.1f} {2 * k:.1f}" '
            f'fill="none" stroke="#9a9aa1" stroke-width="{r * .2:.1f}" stroke-linecap="round"/>')


def _build_time(count):
    s = 12 + count * 4 if count else 0
    if s < 60:
        return f"{s}s"
    if s < 3600:
        return f"{s // 60}m{s % 60:02d}s"
    return f"{s // 3600}h{s % 3600 // 60:02d}m"


def render(days):
    months = month_totals(days)
    totals = [t for _, t in months]
    total = sum(totals)
    med = median(totals) if totals else 0
    peak = max(totals, default=0) or 1
    status = ["fail" if t == 0 else "pass" if t >= med else "warn" for t in totals]
    n = len(months)
    verdict = ("failed" if "fail" in status else "passed with warnings" if "warn" in status else "passed")
    head = "pass" if verdict == "passed" else "warn" if "fail" not in status else "fail"
    last = days[-1]["date"] if days else ""

    out = [
        _icon(40, 118, 13, head),
        f'<text x="64" y="125" xml:space="preserve"><tspan class="hi" font-size="22" font-weight="700">pipeline #{total}</tspan>'
        f'<tspan class="txt" font-size="18">  · {verdict} in {n} stages</tspan></text>',
        f'<text x="{X0}" y="156" class="dim" font-size="14">Triggered via schedule on {esc(last)} · main · median {med:g} per month</text>',
        f'<text x="{X0}" y="196" class="hi" font-size="13" font-weight="700">JOBS</text>',
    ]
    for i, ((key, t), st) in enumerate(zip(months, status)):
        x = X0 + i * (CW + GAP)
        if i:
            out.append(f'<path d="M{x - GAP} {Y0 + 50}H{x}" stroke="#9a9aa1" stroke-width="2"/>')
        dash = ' stroke-dasharray="5 3"' if st == "warn" else ""
        edge = "#9a9aa1" if st == "fail" else "#fff"
        out.append(
            f'<rect x="{x}" y="{Y0}" width="{CW}" height="{CH}" rx="8" class="hi" fill-opacity="{0.10 if st == "pass" else 0.04}" '
            f'stroke="{edge}" stroke-width="1.6"{dash}><title>{key}: {t} contributions, {st}</title></rect>'
            f'<text x="{x + CW / 2}" y="{Y0 + 24}" class="hi" font-size="14" font-weight="700" text-anchor="middle">{MONTHS[int(key[5:]) - 1]}</text>'
            + _icon(x + CW / 2, Y0 + 50, 12, st)
            + f'<text x="{x + CW / 2}" y="{Y0 + 84}" class="{"dim" if st == "fail" else "txt"}" font-size="12" text-anchor="middle">{st}</text>'
            f'<text x="{x + CW / 2}" y="{Y0 + 102}" class="dim" font-size="12" text-anchor="middle">{_build_time(t)}</text>'
            f'<rect x="{x + 8}" y="{Y0 + 110}" width="{CW - 16}" height="5" rx="2" fill="#1b1b1e"/>'
            + (f'<rect x="{x + 8}" y="{Y0 + 110}" width="{max(2, t / peak * (CW - 16)):.1f}" height="5" rx="2" class="hi"/>' if t else "")
        )
    ok, warn, fail = (status.count(s) for s in ("pass", "warn", "fail"))
    y = Y0 + CH + 40
    out.append(
        f'<text x="{X0}" y="{y}" class="txt" font-size="14">{ok} passed · {warn} warned · {fail} failed</text>'
        f'<text x="{X0}" y="{y + 22}" class="dim" font-size="13">pass: at or above the median month · warn: below it · fail: no contributions</text>'
    )
    return {
        "w": W, "h": H, "body": "".join(out), "defs": "", "foot": y + 28, "top": 96,
        "caption": f"{n} stages · {ok} passed, {warn} warned, {fail} failed · median {med:g} per month",
        "title": "ci-pipeline", "cmd": "gh run view",
        "aria": f"CI pipeline run with {n} stages, one per month: {ok} passed, {warn} warned and {fail} failed, build time grows with that month's contributions",
    }
