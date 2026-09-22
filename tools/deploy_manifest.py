#!/usr/bin/env python3
"""
Group theme files into upload batches for themeFilesUpsert.

The Admin API takes an array of files per call, so this splits the theme into
batches that stay under a byte budget and prints them as a plan. Pass --json
to emit machine-readable batches.
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THEME_DIRS = ("assets", "blocks", "config", "layout", "locales", "sections", "snippets", "templates")

# Anything here is repo furniture, not theme content.
SKIP_NAMES = {"README.md", "THEME-CONTRACT.md", ".gitignore"}
SKIP_DIRS = {"tools", ".git"}


def theme_files():
    out = []
    for d in THEME_DIRS:
        base = ROOT / d
        if not base.is_dir():
            continue
        for p in sorted(base.rglob("*")):
            if not p.is_file():
                continue
            if p.name in SKIP_NAMES:
                continue
            if any(part in SKIP_DIRS for part in p.parts):
                continue
            out.append(p)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--budget", type=int, default=90_000,
                    help="max bytes of file content per batch")
    ap.add_argument("--max-files", type=int, default=10,
                    help="max files per batch")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    files = theme_files()
    batches, cur, cur_bytes = [], [], 0

    for p in files:
        size = p.stat().st_size
        too_big = cur and (cur_bytes + size > args.budget or len(cur) >= args.max_files)
        if too_big:
            batches.append(cur)
            cur, cur_bytes = [], 0
        cur.append(p)
        cur_bytes += size
    if cur:
        batches.append(cur)

    if args.json:
        print(json.dumps([[str(p.relative_to(ROOT)) for p in b] for b in batches], indent=2))
        return 0

    total = sum(p.stat().st_size for p in files)
    print(f"{len(files)} theme files, {total/1024:.0f} KiB, {len(batches)} batches\n")
    for i, b in enumerate(batches, 1):
        size = sum(p.stat().st_size for p in b)
        print(f"  batch {i:>2}  {len(b):>2} files  {size/1024:>6.1f} KiB")
        for p in b:
            print(f"            {p.relative_to(ROOT)}  ({p.stat().st_size/1024:.1f} KiB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
