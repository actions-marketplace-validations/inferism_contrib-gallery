"""Each day is one byte. Busy days are bigger hex values, like opening a binary file."""
from common import W

H = 700
PER_ROW, ROW_H = 16, 24


def render(days):
    data = [min(255, d["count"] * 7) for d in days]
    out = []
    for r in range(0, len(data), PER_ROW):
        y = 112 + (r // PER_ROW) * ROW_H
        chunk = data[r:r + PER_ROW]
        out.append(f'<text x="28" y="{y}" class="dim" font-size="15">{r:08x}</text>')
        for i, b in enumerate(chunk):
            cls = "dim" if b == 0 else "hi"
            op = "" if b == 0 else f' fill-opacity="{0.55 + 0.45 * b / 255:.2f}"'
            out.append(f'<text x="{150 + i * 33}" y="{y}" class="{cls}" font-size="15"{op}>{b:02x}</text>')
        ascii_ = "".join(chr(33 + min(90, b // 3)) if b else "." for b in chunk).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        out.append(f'<text x="710" y="{y}" class="txt" font-size="15" textLength="{len(chunk) * 9.4:.0f}" lengthAdjust="spacing" xml:space="preserve">{ascii_}</text>')
    rows = (len(data) + PER_ROW - 1) // PER_ROW
    total = sum(d["count"] for d in days)
    return {
        "w": W, "h": H, "body": "".join(out), "defs": "", "foot": 112 + rows * ROW_H, "top": 96,
        "caption": f"{len(data)} bytes · {total:,} contributions · one byte per day",
        "title": "hex-dump", "cmd": "xxd contributions.bin",
        "aria": f"Hex dump with one byte for each of the {len(data)} days, larger values for busier days",
    }
