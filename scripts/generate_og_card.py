#!/usr/bin/env python3
"""Generate assets/img/og-card.jpg from the site's own design tokens.

Not part of the normal build -- run by hand whenever the name, title, or
site palette (assets/css/style.css :root) changes:

    pixi run python3 scripts/generate_og_card.py

Reads the portrait crop straight from assets/img/_raw/portrait.jpg so the
card uses a full-resolution source instead of the already-compressed
og-unrelated output.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "img" / "og-card.jpg"
PORTRAIT_RAW = ROOT / "assets" / "img" / "_raw" / "portrait.jpg"
PORTRAIT_FALLBACK = ROOT / "assets" / "img" / "portrait.jpg"

FONT_PATH = "/usr/share/fonts/truetype/ubuntu/UbuntuSans[wdth,wght].ttf"

# ---- design tokens, copied from assets/css/style.css :root (light palette) --
BG = "#fbfaf8"
TEXT = "#1c1b19"
TEXT_MUTED = "#5f5c56"
ACCENT = "#0f6f6c"

W, H = 1200, 630
TOP_BAR_H = 6
DIVIDER_X = 792
DIVIDER_W = 4
PHOTO_X0 = DIVIDER_X + DIVIDER_W
LEFT_MARGIN = 72
TEXT_RIGHT = DIVIDER_X - 32


def font(size: int, weight: str = "Regular") -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(FONT_PATH, size)
    f.set_variation_by_name(weight)
    return f


def draw_tracked(draw: ImageDraw.ImageDraw, xy, text, fnt, fill, tracking=0):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        w = draw.textlength(ch, font=fnt)
        x += w + tracking
    return x


def wrap_text(draw, text, fnt, max_width):
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def cover_crop(im: Image.Image, target_w: int, target_h: int) -> Image.Image:
    target_ratio = target_w / target_h
    ratio = im.width / im.height
    if ratio > target_ratio:
        new_w = round(im.height * target_ratio)
        left = (im.width - new_w) // 2
        im = im.crop((left, 0, left + new_w, im.height))
    else:
        new_h = round(im.width / target_ratio)
        top = round((im.height - new_h) * 0.28)  # bias up: keep the face, not the gown
        im = im.crop((0, top, im.width, top + new_h))
    return im.resize((target_w, target_h), Image.LANCZOS)


def main() -> None:
    card = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(card)

    # top accent bar
    draw.rectangle([0, 0, W, TOP_BAR_H], fill=ACCENT)

    # photo panel, right-aligned, cover-cropped
    src_path = PORTRAIT_RAW if PORTRAIT_RAW.exists() else PORTRAIT_FALLBACK
    with Image.open(src_path) as photo:
        photo = ImageOps.exif_transpose(photo).convert("RGB")
        panel_w, panel_h = W - PHOTO_X0, H - TOP_BAR_H
        photo = cover_crop(photo, panel_w, panel_h)
        card.paste(photo, (PHOTO_X0, TOP_BAR_H))

    # divider seam between text and photo
    draw.rectangle([DIVIDER_X, 0, DIVIDER_X + DIVIDER_W, H], fill=ACCENT)

    # -- text block --
    eyebrow_font = font(21, "SemiBold")
    name_font = font(80, "Bold")
    tagline_font = font(29, "Medium")
    domain_font = font(23, "SemiBold")

    eyebrow = "PHD, BIOMEDICAL ENGINEERING · COLUMBIA"
    y = 168
    draw_tracked(draw, (LEFT_MARGIN, y), eyebrow, eyebrow_font, ACCENT, tracking=2)

    y += 46
    draw.text((LEFT_MARGIN, y), "Terry Chern", font=name_font, fill=TEXT)

    y += 108
    draw.rectangle([LEFT_MARGIN, y, LEFT_MARGIN + 56, y + 4], fill=ACCENT)

    y += 34
    tagline = "Wearable devices and digital health — from sensor to clinical evidence."
    max_w = TEXT_RIGHT - LEFT_MARGIN
    lines = wrap_text(draw, tagline, tagline_font, max_w)
    line_h = 42
    for line in lines:
        draw.text((LEFT_MARGIN, y), line, font=tagline_font, fill=TEXT_MUTED)
        y += line_h

    # domain watermark, bottom-left
    draw.text((LEFT_MARGIN, H - 66), "terrychern.com", font=domain_font, fill=ACCENT)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    card.save(OUT, "JPEG", quality=90, optimize=True, progressive=True)
    print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
