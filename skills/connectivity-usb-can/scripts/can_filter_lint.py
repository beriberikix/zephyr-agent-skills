#!/usr/bin/env python3
"""Validate CAN filter entries from CSV.

CSV columns:
  id,mask,extended
Values:
  id/mask may be decimal or hex (0x...)
  extended is true/false/1/0
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def parse_int(text: str) -> int:
    text = text.strip().lower()
    return int(text, 16) if text.startswith("0x") else int(text, 10)


def parse_bool(text: str) -> bool:
    t = text.strip().lower()
    if t in {"1", "true", "yes", "y"}:
        return True
    if t in {"0", "false", "no", "n"}:
        return False
    raise ValueError(f"invalid bool value: {text}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lint CAN filter CSV definitions")
    parser.add_argument("--csv", required=True, help="Path to CSV file")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    path = Path(args.csv)
    if not path.exists():
        print(f"error: file not found: {path}")
        return 2

    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for col in ("id", "mask", "extended"):
            if col not in (reader.fieldnames or []):
                print(f"error: missing column '{col}'")
                return 2

        seen = set()
        rows = 0
        for line_no, row in enumerate(reader, start=2):
            try:
                can_id = parse_int(row["id"])
                mask = parse_int(row["mask"])
                extended = parse_bool(row["extended"])
            except Exception as exc:
                print(f"error: line {line_no}: {exc}")
                return 1

            max_id = 0x1FFFFFFF if extended else 0x7FF
            if can_id < 0 or can_id > max_id:
                print(f"error: line {line_no}: id out of range for {'extended' if extended else 'standard'} CAN")
                return 1
            if mask < 0 or mask > max_id:
                print(f"error: line {line_no}: mask out of range")
                return 1

            key = (can_id, mask, extended)
            if key in seen:
                print(f"warning: line {line_no}: duplicate filter tuple {key}")
            seen.add(key)
            rows += 1

    print(f"CAN filter lint passed: {rows} entries checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
