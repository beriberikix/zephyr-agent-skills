#!/usr/bin/env python3
"""Scan source files for non-negative errno-style returns.

Looks for lines like:
  return EINVAL;   # likely bug, should usually be -EINVAL
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

PATTERN = re.compile(r"\breturn\s+([A-Z][A-Z0-9_]+)\s*;")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Detect likely errno return sign issues")
    parser.add_argument("paths", nargs="+", help="Files or directories to scan")
    return parser.parse_args()


def files_for(paths: list[str]) -> list[Path]:
    exts = {".c", ".h", ".cpp", ".hpp"}
    out: list[Path] = []
    for raw in paths:
        p = Path(raw)
        if p.is_file() and p.suffix in exts:
            out.append(p)
            continue
        if p.is_dir():
            for c in p.rglob("*"):
                if c.is_file() and c.suffix in exts:
                    out.append(c)
    return sorted(set(out))


def main() -> int:
    args = parse_args()
    files = files_for(args.paths)
    if not files:
        print("No source files found.")
        return 2

    hits = []
    for fp in files:
        for ln, line in enumerate(fp.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
            m = PATTERN.search(line)
            if m and m.group(1).startswith("E"):
                hits.append((fp, ln, m.group(1), line.strip()))

    if not hits:
        print(f"No suspicious errno returns found in {len(files)} files.")
        return 0

    print("Potential non-negative errno returns:")
    for fp, ln, sym, text in hits:
        print(f"- {fp}:{ln} -> {sym} :: {text}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
