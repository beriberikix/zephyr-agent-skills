#!/usr/bin/env python3
"""Simple keyword matcher from task text to recommended Zephyr skill.

Uses a CSV mapping with columns: keyword,skill
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Match a task string to likely Zephyr skill")
    parser.add_argument("--task", required=True, help="Task description text")
    parser.add_argument("--map", required=True, help="CSV keyword map file")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    map_path = Path(args.map)
    if not map_path.exists():
        print(f"error: file not found: {map_path}")
        return 2

    task = args.task.lower()
    matches: dict[str, int] = {}

    with map_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for col in ("keyword", "skill"):
            if col not in (reader.fieldnames or []):
                print(f"error: missing column '{col}'")
                return 2

        for row in reader:
            kw = (row.get("keyword") or "").strip().lower()
            skill = (row.get("skill") or "").strip()
            if not kw or not skill:
                continue
            if kw in task:
                matches[skill] = matches.get(skill, 0) + 1

    if not matches:
        print("No keyword matches found.")
        return 1

    print("Suggested skills (highest score first):")
    for skill, score in sorted(matches.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"- {skill}: {score}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
