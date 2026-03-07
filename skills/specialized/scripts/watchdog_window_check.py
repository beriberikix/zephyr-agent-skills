#!/usr/bin/env python3
"""Validate watchdog feed interval against configured watchdog window."""

from __future__ import annotations

import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check watchdog feed interval constraints")
    parser.add_argument("--min-ms", type=float, required=True, help="Watchdog minimum feed window (ms)")
    parser.add_argument("--max-ms", type=float, required=True, help="Watchdog maximum feed window (ms)")
    parser.add_argument("--feed-ms", type=float, required=True, help="Planned feed interval (ms)")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.min_ms < 0 or args.max_ms <= 0 or args.max_ms <= args.min_ms:
        print("error: invalid watchdog window")
        return 2

    if args.feed_ms < args.min_ms:
        print("error: feed interval is too early for watchdog window")
        return 1
    if args.feed_ms > args.max_ms:
        print("error: feed interval is too late for watchdog window")
        return 1

    print("Watchdog window check passed")
    print(f"  window: {args.min_ms}..{args.max_ms} ms")
    print(f"  feed:   {args.feed_ms} ms")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
