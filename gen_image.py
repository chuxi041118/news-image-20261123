#!/usr/bin/env python3
"""Render entry.png for news-image-20261123 (Monday 23 November 2026).

Local build tool only -- the graded entry is main.py, which copies the
rendered entry.png to /output/entry.png. Run: python3 gen_image.py
Requires Pillow and DejaVu fonts locally (not needed at grade time).
"""

import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (247, 244, 236)        # off-white paper
NAVY = (20, 33, 61)         # header band / headline ink
INK = (30, 30, 30)          # body ink
MUTED = (90, 88, 80)        # footer ink
GOLD = (198, 148, 42)       # rule under header
RULE = (200, 192, 175)      # row separators

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

TITLE_FONT = ImageFont.truetype(BOLD, 80)
KICKER_FONT = ImageFont.truetype(BOLD, 28)
TAG_FONT = ImageFont.truetype(BOLD, 28)
HEAD_FONT = ImageFont.truetype(BOLD, 40)
SUM_FONT = ImageFont.truetype(REG, 30)
NUM_FONT = ImageFont.truetype(BOLD, 58)
FOOT_FONT = ImageFont.truetype(REG, 24)

STORIES = [
    ("1", "CLIMATE", (46, 125, 50), "COP31 ends with no deal",
     "Climate talks in Antalya collapse after the final text drops all mention of fossil fuels."),
    ("2", "CONFLICT", (179, 38, 30), "Russian warship sunk at Benghazi",
     "Satellite images show the corvette Merkury sunk at its berth after a suspected Ukrainian sea-drone attack."),
    ("3", "POLITICS", (21, 101, 192), "Democrats win 258 House seats",
     "Their biggest House majority since 1992, sealed by a recount win in North Carolina."),
    ("4", "MARKETS", (191, 84, 0), "AI sell-off shakes world markets",
     "The Nasdaq Composite posts its worst week since March 2020, down 10%, as AI stocks slide."),
    ("5", "DISASTER", (106, 27, 154), "Factory fire in Indonesia",
     "At least 24 dead and dozens missing after a blaze at a candy factory in Banten."),
]


def wrap(draw, text, font, max_w):
    """Greedy word wrap measured with the real font; returns list of lines."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Header band
    band_h = 150
    d.rectangle([0, 0, W, band_h], fill=NAVY)
    d.text((48, 18), "MONDAY  \u00b7  23 NOVEMBER 2026", font=KICKER_FONT, fill=(212, 175, 105))
    d.text((48, 52), "WORLD IN BRIEF", font=TITLE_FONT, fill=(255, 255, 255))
    d.rectangle([0, band_h, W, band_h + 6], fill=GOLD)

    # Story rows
    top = band_h + 6
    row_h = (H - top - 44) // 5  # 44 px reserved for the footer
    x_num, x_text = 48, 148
    text_w = W - x_text - 48
    for i, (num, tag, color, head, summary) in enumerate(STORIES):
        y = top + i * row_h
        if i:
            d.line([48, y, W - 48, y], fill=RULE, width=2)
        # number gutter
        d.text((x_num, y + 18), num, font=NUM_FONT, fill=color)
        # colour marker + tag
        d.rectangle([x_text, y + 18, x_text + 13, y + 31], fill=color)
        d.text((x_text + 25, y + 10), tag, font=TAG_FONT, fill=color)
        # headline (one line, shrink until it fits)
        hf, size = HEAD_FONT, 40
        while d.textlength(head, font=hf) > text_w and size > 32:
            size -= 2
            hf = ImageFont.truetype(BOLD, size)
        d.text((x_text, y + 44), head, font=hf, fill=NAVY)
        # summary, up to two lines
        lines = wrap(d, summary, SUM_FONT, text_w)[:2]
        sy = y + 44 + size + 8
        for line in lines:
            d.text((x_text, sy), line, font=SUM_FONT, fill=INK)
            sy += 35

    # Footer
    fy = H - 40
    d.line([48, fy - 10, W - 48, fy - 10], fill=RULE, width=2)
    d.text((48, fy), "Sources: BBC, Reuters  \u00b7  All stories reported 23 November 2026",
           font=FOOT_FONT, fill=MUTED)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
