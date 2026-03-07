#!/usr/bin/env python3
"""Lint a Modbus register map CSV for duplicates and overlaps.

Expected CSV columns:
  table,address,name,size

Where:
- table: coil|discrete_input|holding_register|input_register
- address: non-negative integer
- size: positive integer (defaults to 1 if omitted)
"""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass
from pathlib import Path

VALID_TABLES = {
    "coil",
    "discrete_input",
    "holding_register",
    "input_register",
}


@dataclass(frozen=True)
class Entry:
    table: str
    address: int
    name: str
    size: int
    line: int


class CsvError(Exception):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lint Modbus register map CSV")
    parser.add_argument("--csv", required=True, help="Path to register map CSV")
    return parser.parse_args()


def parse_int(value: str, field: str, line: int) -> int:
    try:
        parsed = int(value, 10)
    except ValueError as exc:
        raise CsvError(f"line {line}: invalid {field} '{value}'") from exc
    return parsed


def load_entries(csv_path: Path) -> list[Entry]:
    if not csv_path.exists():
        raise CsvError(f"file not found: {csv_path}")

    entries: list[Entry] = []

    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"table", "address", "name", "size"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise CsvError(f"missing CSV columns: {', '.join(sorted(missing))}")

        for line_no, row in enumerate(reader, start=2):
            table = (row.get("table") or "").strip().lower()
            if table not in VALID_TABLES:
                raise CsvError(
                    f"line {line_no}: invalid table '{table}', expected one of {sorted(VALID_TABLES)}"
                )

            address = parse_int((row.get("address") or "").strip(), "address", line_no)
            size = parse_int((row.get("size") or "1").strip(), "size", line_no)
            name = (row.get("name") or "").strip()

            if address < 0:
                raise CsvError(f"line {line_no}: address must be >= 0")
            if size <= 0:
                raise CsvError(f"line {line_no}: size must be > 0")
            if not name:
                raise CsvError(f"line {line_no}: name must not be empty")

            entries.append(
                Entry(table=table, address=address, name=name, size=size, line=line_no)
            )

    return entries


def lint(entries: list[Entry]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    by_key: dict[tuple[str, int], list[Entry]] = {}
    by_table: dict[str, list[Entry]] = {}

    for entry in entries:
        by_key.setdefault((entry.table, entry.address), []).append(entry)
        by_table.setdefault(entry.table, []).append(entry)

    for (table, addr), same_addr in sorted(by_key.items()):
        if len(same_addr) > 1:
            lines = ", ".join(str(e.line) for e in same_addr)
            names = ", ".join(e.name for e in same_addr)
            errors.append(
                f"duplicate start address: {table}@{addr} used by [{names}] (lines: {lines})"
            )

    for table, table_entries in sorted(by_table.items()):
        ordered = sorted(table_entries, key=lambda e: (e.address, e.size, e.name))
        for prev, curr in zip(ordered, ordered[1:]):
            prev_end = prev.address + prev.size - 1
            if curr.address <= prev_end:
                errors.append(
                    "overlap: "
                    f"{table} '{prev.name}' [{prev.address}-{prev_end}] line {prev.line} "
                    f"overlaps '{curr.name}' [{curr.address}-{curr.address + curr.size - 1}] line {curr.line}"
                )

    sparse_threshold = 1024
    for table, table_entries in sorted(by_table.items()):
        addresses = sorted(e.address for e in table_entries)
        if not addresses:
            continue
        spread = addresses[-1] - addresses[0]
        if spread > sparse_threshold and len(addresses) < 10:
            warnings.append(
                f"{table} map is sparse (spread={spread}, entries={len(addresses)}); verify address plan"
            )

    return errors, warnings


def main() -> int:
    args = parse_args()

    try:
        entries = load_entries(Path(args.csv))
    except CsvError as exc:
        print(f"error: {exc}")
        return 2

    errors, warnings = lint(entries)

    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"- {warning}")

    if errors:
        print("Errors:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Register map OK ({len(entries)} entries checked).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
