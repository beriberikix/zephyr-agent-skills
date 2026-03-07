#!/usr/bin/env python3
"""Basic sanity checks for Zephyr devicetree overlay files."""

from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check overlay text for common issues")
    parser.add_argument("--overlay", required=True, help="Path to .overlay file")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    path = Path(args.overlay)
    if not path.exists():
        print(f"error: file not found: {path}")
        return 2

    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()

    if "{" not in text or "};" not in text:
        print("error: overlay appears to be missing node braces")
        return 1

    if "/delete-node/" in text and "&" not in text:
        print("warning: delete-node directive present without obvious label reference")

    status_lines = [ln for ln in lines if "status" in ln and "=" in ln]
    bad_status = [ln for ln in status_lines if '"okay"' not in ln and '"disabled"' not in ln]
    if bad_status:
        print("warning: found non-standard status assignments:")
        for ln in bad_status:
            print(f"  {ln.strip()}")

    print(f"Overlay check passed: {path} ({len(lines)} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
