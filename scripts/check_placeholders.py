#!/usr/bin/env python3
"""Flag [[PLACEHOLDER]] markers left in the site before you publish.

Run with:  pixi run check
Exits 1 if anything is still unfilled, so it also works as a pre-push guard.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATTERN = re.compile(r"\[\[[^\]]+\]\]")
SCAN_SUFFIXES = {".html", ".css", ".js", ".xml", ".txt", ".md"}
SKIP_DIRS = {".pixi", ".git", "_raw", "scripts", "node_modules"}
SKIP_FILES = {"PLAN.md", "README.md"}


def main() -> int:
    hits: list[tuple[Path, int, str]] = []

    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix not in SCAN_SUFFIXES:
            continue
        if set(path.relative_to(ROOT).parts) & SKIP_DIRS:
            continue
        if path.name in SKIP_FILES:
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        for lineno, line in enumerate(text.splitlines(), 1):
            for match in PATTERN.finditer(line):
                hits.append((path.relative_to(ROOT), lineno, match.group()))

    if not hits:
        print("No placeholders left. Ready to publish.")
        return 0

    print(f"{len(hits)} placeholder(s) still to fill in:\n")
    current: Path | None = None
    for rel, lineno, token in hits:
        if rel != current:
            print(f"  {rel}")
            current = rel
        print(f"    line {lineno:>4}: {token}")

    print("\nFill these in, then re-run `pixi run check`.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
