"""An RPG character sheet built from the year: level, XP, and a few stat bars."""
import math

from common import W, peak_of

H = 430
TICKS, PITCH = 26, 12


def _streaks(counts):
    best = run = 0
    for c in counts:
        run = run + 1 if c else 0
        best = max(best, run)
    cur = 0
    for c in reversed(counts[:-1] if counts and counts[-1] == 0 else counts):
        if not c:
            break
        cur += 1
    return cur, best


def _title(level):
    for cap, name in [(5, "Novice"), (10, "Apprentice"), (15, "Journeyman"), (20, "Veteran")]:
        if level < cap:
            return name
    return "Archmage"


def _bar(x, y, frac):
    filled = round(max(0.0, min(1.0, frac)) * TICKS)
    return "".join(
        f'<rect x="{x + i * PITCH}" y="{y - 14}" width="4" height="18" fill="{"#fff" if i < filled else "#1b1b1e"}"/>'
        for i in range(TICKS)
    )


def render(days):
    counts = [d["count"] for d in days]
    total = sum(counts)
    peak = peak_of(days)
    cur, best = _streaks(counts)
    active = sum(1 for c in counts if c)
    last30 = sum(counts[-30:])
    lv = int(math.sqrt(total)) + 1
    xp, need = total - (lv - 1) ** 2, lv ** 2 - (lv - 1) ** 2

    out = [
        '<text x="52" y="150" class="dim" font-size="20" letter-spacing="3">LEVEL</text>'
        f'<text x="48" y="238" class="hi" font-size="92" font-weight="700">{lv}</text>'
        f'<text x="52" y="278" class="txt" font-size="20">{_title(lv)} Committer</text>'
        f'<text x="52" y="326" class="dim" font-size="14">XP {xp} / {need}</text>'
        + "".join(
            f'<rect x="{52 + i * 11}" y="336" width="4" height="16" fill="{"#fff" if i < round(xp / need * 24) else "#1b1b1e"}"/>'
            for i in range(24)
        )
    ]
    rows = [
        ("HP", "current streak", cur, 30, f"{cur}d"),
        ("VIT", "best streak", best, 60, f"{best}d"),
        ("DEX", "active days", active, 365, f"{active}"),
        ("CRIT", "best day", peak, 100, f"{peak}"),
        ("MANA", "last 30 days", last30, 300, f"{last30}"),
    ]
    for i, (name, desc, val, cap, shown) in enumerate(rows):
        y = 150 + i * 54
        out.append(
            f'<text x="420" y="{y}" class="hi" font-size="19" font-weight="700">{name}</text>'
            f'<text x="420" y="{y + 18}" class="dim" font-size="12">{desc}</text>'
            + _bar(530, y, val / cap)
            + f'<text x="972" y="{y}" text-anchor="end" class="hi" font-size="19" font-weight="700">{shown}</text>'
        )
    out.append(
        f'<line x1="420" y1="396" x2="972" y2="396" stroke="#2a2a2d" stroke-width="1.5" stroke-dasharray="2 5"/>'
        f'<text x="420" y="{H - 10}" class="dim" font-size="14">&gt; {total:,} XP earned this year, +{last30} in the last 30 days</text>'
    )
    return {
        "w": W, "h": H, "body": "".join(out), "defs": "",
        "title": "character-sheet", "cmd": "stats --last 365d",
        "aria": f"RPG character sheet: level {lv} {_title(lv)} with a {cur} day streak and {total:,} contributions",
    }
