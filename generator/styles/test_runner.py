"""Test-runner output: one row per month, a dot for every active day and a dash for every quiet one."""
from common import MONTHS, W, level, peak_of

H = 540
X0, PITCH, TOP, ROW = 150, 24, 112, 30


def render(days):
    peak = peak_of(days)
    by_month = {}
    for d in days:
        by_month.setdefault(d["date"][:7], []).append(d)
    keys = sorted(by_month)[-12:]
    span = sum(len(by_month[k]) for k in keys)
    out, seen, passed, skipped = [], 0, 0, 0
    for r, k in enumerate(keys):
        y = TOP + r * ROW
        out.append(f'<text x="28" y="{y + 5}" class="dim" font-size="15">{MONTHS[int(k[5:7]) - 1]} {k[:4]}</text>')
        for i, d in enumerate(by_month[k]):
            cx = X0 + i * PITCH + 8
            if d["count"]:
                passed += 1
                lv = level(d["count"], peak)
                out.append(f'<circle cx="{cx}" cy="{y}" r="{2.4 + lv * 0.5:.1f}" fill="#fff" fill-opacity="{0.5 + lv * 0.125:.2f}"/>')
            else:
                skipped += 1
                out.append(f'<rect x="{cx - 4}" y="{y - 1}" width="8" height="2" fill="#9a9aa1" fill-opacity="0.55"/>')
        seen += len(by_month[k])
        out.append(f'<text x="972" y="{y + 5}" text-anchor="end" class="dim" font-size="15">[{round(seen / span * 100):>3}%]</text>')
    bar = "=" * 28
    deco = f'<text x="28" y="88" class="dim" font-size="14">{bar} test session starts {bar}</text>'
    return {
        "w": W, "h": H, "body": "".join(out), "defs": "", "deco": deco, "foot": TOP + 11 * ROW + 18, "top": 96,
        "caption": f"{passed} passed, {skipped} skipped in {len(days)} days",
        "title": "test-runner", "cmd": "pytest --last 365d  # a dot for every active day",
        "aria": f"Test runner output: {passed} passing days and {skipped} skipped days over the last year",
    }
