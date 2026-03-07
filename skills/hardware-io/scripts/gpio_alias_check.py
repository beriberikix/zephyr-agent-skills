#!/usr/bin/env python3
"""Check for duplicate alias definitions in DTS/overlay files."""

from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path

ALIAS_RE = re.compile(r"^\s*([a-zA-Z0-9_\-]+)\s*=\s*&[a-zA-Z0-9_]+\s*;")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Detect duplicate alias entries")
    parser.add_argument("paths", nargs="+", help="DTS/overlay files or directories")
    return parser.parse_args()


def collect_files(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    exts = {".dts", ".dtsi", ".overlay"}
    for raw in paths:
        p = Path(raw)
        if p.is_file() and p.suffix in exts:
            files.append(p)
            continue
        if p.is_dir():
            for c in p.rglob("*"):
                if c.is_file() and c.suffix in exts:
                    files.append(c)
    return sorted(set(files))


def main() -> int:
    args = parse_args()
    files = collect_files(args.paths)
    if not files:
        print("No DTS/overlay files found.")
        return 2

    aliases: dict[str, list[str]] = defaultdict(list)
    for fp in files:
        for ln, line in enumerate(fp.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
            m = ALIAS_RE.match(line)
            if m:
                aliases[m.group(1)].append(f"{fp}:{ln}")

    dup = {k: v for k, v in aliases.items() if len(v) > 1}
    if dup:
        print("Duplicate aliases found:")
        for name in sorted(dup):
            print(f"- {name}")
            for ref in dup[name]:
                print(f"  {ref}")
        return 1

    print(f"Alias check passed ({len(aliases)} aliases across {len(files)} files).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
