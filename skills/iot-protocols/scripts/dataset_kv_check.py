#!/usr/bin/env python3
"""Validate simple key=value dataset files for IoT protocol provisioning."""

from __future__ import annotations

import argparse
from pathlib import Path

REQUIRED_KEYS = {"network_name", "pan_id", "channel", "pskc"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Thread-style dataset key/value file")
    parser.add_argument("--dataset", required=True, help="Path to key=value file")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    path = Path(args.dataset)
    if not path.exists():
        print(f"error: file not found: {path}")
        return 2

    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        raw = line.strip()
        if not raw or raw.startswith("#"):
            continue
        if "=" not in raw:
            print(f"warning: ignoring non key=value line: {raw}")
            continue
        k, v = raw.split("=", 1)
        values[k.strip()] = v.strip()

    missing = sorted(REQUIRED_KEYS - set(values))
    if missing:
        print(f"error: missing keys: {', '.join(missing)}")
        return 1

    print("Dataset key/value check passed")
    for k in sorted(REQUIRED_KEYS):
        print(f"  {k}=<set>")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
