#!/usr/bin/env python3
"""Validate basic structure of Zephyr HWMv2 board.yml files."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

NAME_RE = re.compile(r"^[a-z0-9_\-]+$")


class LintError(Exception):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lint board.yml structure")
    parser.add_argument("--board-yml", required=True, help="Path to board.yml")
    return parser.parse_args()


def validate_name(name: str, field: str) -> None:
    if not name:
        raise LintError(f"{field} must not be empty")
    if not NAME_RE.match(name):
        raise LintError(f"{field} must use lowercase letters/digits/_/-: {name}")


def lint_board_entry(entry: dict, idx: int) -> None:
    if not isinstance(entry, dict):
        raise LintError(f"board entry {idx} must be a mapping")

    if "name" not in entry:
        raise LintError(f"board entry {idx} missing required key: name")
    validate_name(str(entry["name"]), f"board entry {idx}.name")

    if "vendor" in entry:
        validate_name(str(entry["vendor"]), f"board entry {idx}.vendor")

    if "revision" in entry and not isinstance(entry["revision"], dict):
        raise LintError(f"board entry {idx}.revision must be a mapping")


def main() -> int:
    args = parse_args()
    board_path = Path(args.board_yml)
    if not board_path.exists():
        print(f"error: file not found: {board_path}")
        return 2

    try:
        data = yaml.safe_load(board_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        print(f"error: invalid YAML: {exc}")
        return 2

    if not isinstance(data, dict):
        print("error: board.yml must be a YAML mapping")
        return 2

    # Accept either a single 'board' object or HWMv2-style 'boards' list.
    if "boards" in data:
        boards = data["boards"]
        if not isinstance(boards, list) or not boards:
            print("error: 'boards' must be a non-empty list")
            return 2
        try:
            for idx, board in enumerate(boards, start=1):
                lint_board_entry(board, idx)
        except LintError as exc:
            print(f"error: {exc}")
            return 1
    elif "board" in data:
        board = data["board"]
        if not isinstance(board, dict):
            print("error: 'board' must be a mapping")
            return 2
        try:
            lint_board_entry(board, 1)
        except LintError as exc:
            print(f"error: {exc}")
            return 1
    else:
        print("error: expected either 'boards' list or 'board' mapping")
        return 2

    print(f"board.yml lint passed: {board_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
