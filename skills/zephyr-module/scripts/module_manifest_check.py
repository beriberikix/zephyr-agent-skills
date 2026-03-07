#!/usr/bin/env python3
"""Validate a Zephyr module.yml file for common integration requirements."""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml


class ManifestError(Exception):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate zephyr/module.yml content")
    parser.add_argument("--module-yml", required=True, help="Path to zephyr/module.yml")
    return parser.parse_args()


def require_string(mapping: dict, key: str, ctx: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ManifestError(f"{ctx}.{key} must be a non-empty string")
    return value


def main() -> int:
    args = parse_args()
    module_path = Path(args.module_yml)
    if not module_path.exists():
        print(f"error: file not found: {module_path}")
        return 2

    try:
        data = yaml.safe_load(module_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        print(f"error: invalid YAML: {exc}")
        return 2

    if not isinstance(data, dict):
        print("error: module.yml must be a YAML mapping")
        return 2

    build = data.get("build")
    if not isinstance(build, dict):
        print("error: missing required mapping: build")
        return 1

    try:
        cmake = require_string(build, "cmake", "build")
        kconfig = require_string(build, "kconfig", "build")
    except ManifestError as exc:
        print(f"error: {exc}")
        return 1

    depends = data.get("depends")
    if depends is not None:
        if not isinstance(depends, list) or not all(isinstance(x, str) for x in depends):
            print("error: depends must be a list of strings when provided")
            return 1

    print("module.yml check passed")
    print(f"  build.cmake: {cmake}")
    print(f"  build.kconfig: {kconfig}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
