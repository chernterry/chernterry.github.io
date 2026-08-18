#!/usr/bin/env python3
"""Resize and compress photos for the web.

Drop full-size originals (camera JPEGs, phone photos) into assets/img/_raw/.
That directory is gitignored, so originals never bloat the repo.

Run with:  pixi run optimize-images

Output goes to assets/img/ preserving subdirectories, capped at MAX_WIDTH and
saved as progressive JPEG. EXIF orientation is applied and all other metadata
is stripped -- phone photos carry GPS coordinates, which you do not want to
publish on a public website.
"""
from __future__ import annotations

import sys
from pathlib import Path

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit("Pillow is missing. Run this via `pixi run optimize-images`.")

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "assets" / "img" / "_raw"
OUT = ROOT / "assets" / "img"

MAX_WIDTH = 1600
QUALITY = 82
SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff", ".heic"}


def optimize(src: Path) -> tuple[Path, int, int] | None:
    rel = src.relative_to(RAW).with_suffix(".jpg")
    dest = OUT / rel
    dest.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(src) as im:
        # Honor the EXIF rotation flag, then drop EXIF entirely (incl. GPS)
        im = ImageOps.exif_transpose(im)
        if im.mode not in ("RGB", "L"):
            im = im.convert("RGB")
        if im.width > MAX_WIDTH:
            height = round(im.height * MAX_WIDTH / im.width)
            im = im.resize((MAX_WIDTH, height), Image.LANCZOS)
        im.save(dest, "JPEG", quality=QUALITY, optimize=True, progressive=True)

    return dest, src.stat().st_size, dest.stat().st_size


def main() -> int:
    if not RAW.exists():
        RAW.mkdir(parents=True, exist_ok=True)
        print(f"Created {RAW.relative_to(ROOT)} -- drop your full-size photos there and re-run.")
        return 0

    sources = [p for p in sorted(RAW.rglob("*")) if p.is_file() and p.suffix.lower() in SUFFIXES]
    if not sources:
        print(f"No images found in {RAW.relative_to(ROOT)}/")
        return 0

    total_before = total_after = 0
    for src in sources:
        try:
            result = optimize(src)
        except Exception as exc:  # a single bad file shouldn't abort the batch
            print(f"  SKIP {src.name}: {exc}")
            continue
        dest, before, after = result
        total_before += before
        total_after += after
        print(f"  {src.name} -> {dest.relative_to(ROOT)}  "
              f"({before / 1024:.0f} KB -> {after / 1024:.0f} KB)")

    if total_before:
        saved = 100 * (1 - total_after / total_before)
        print(f"\n{len(sources)} image(s): {total_before / 1e6:.1f} MB -> "
              f"{total_after / 1e6:.1f} MB ({saved:.0f}% smaller)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
