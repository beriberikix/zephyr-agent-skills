#!/usr/bin/env python3
"""Repository-level quality gates for Zephyr skill documents.

Checks performed:
- Every skill has a valid SKILL.md frontmatter (via quick_validate.py).
- Every skill includes both "## Quick Start" and "## Validation Checklist" sections.
- All local markdown links in SKILL.md resolve.
- Cross-skill deep links to references/assets/scripts are rejected.
- Catalog and marketplace entries match skill directories.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
CATALOG_FILE = REPO_ROOT / "skills" / "zephyr-index" / "references" / "skill_catalog.md"
MARKETPLACE_FILE = REPO_ROOT / ".claude-plugin" / "marketplace.json"
QUICK_VALIDATE = REPO_ROOT / ".agent" / "skills" / "skill-creator" / "scripts" / "quick_validate.py"

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
DEEP_CROSS_SKILL_RE = re.compile(r"^\.\./[^/]+/(references|assets|scripts)/")


class ValidationError(Exception):
    pass


def iter_skill_dirs(skills_dir: Path) -> list[Path]:
    dirs = []
    for item in sorted(skills_dir.iterdir(), key=lambda p: p.name):
        if item.is_dir() and (item / "SKILL.md").exists():
            dirs.append(item)
    return dirs


def check_frontmatter(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    proc = subprocess.run(
        [sys.executable, str(QUICK_VALIDATE), str(skill_dir)],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        msg = proc.stdout.strip() or proc.stderr.strip() or "unknown quick_validate error"
        errors.append(f"{skill_dir.name}: frontmatter invalid: {msg}")
    return errors


def _normalize_local_link(raw_target: str) -> str:
    target = raw_target.strip()
    target = target.split("#", 1)[0]
    target = target.split("?", 1)[0]
    return target


def check_skill_sections(skill_md: Path) -> list[str]:
    errors: list[str] = []
    content = skill_md.read_text(encoding="utf-8")
    if "## Quick Start" not in content:
        errors.append(f"{skill_md}: missing '## Quick Start' section")
    if "## Validation Checklist" not in content:
        errors.append(f"{skill_md}: missing '## Validation Checklist' section")
    return errors


def check_skill_links(skill_md: Path) -> list[str]:
    errors: list[str] = []
    content = skill_md.read_text(encoding="utf-8")

    for match in LINK_RE.finditer(content):
        raw_target = match.group(1).strip()

        # Ignore external and pure-anchor links.
        if raw_target.startswith(("http://", "https://", "mailto:", "javascript:")):
            continue
        if raw_target.startswith("#"):
            continue

        normalized = _normalize_local_link(raw_target)
        if not normalized:
            continue

        if DEEP_CROSS_SKILL_RE.match(normalized):
            errors.append(
                f"{skill_md}: deep cross-skill link not allowed: {raw_target}"
            )
            continue

        if normalized.startswith("/"):
            resolved = REPO_ROOT / normalized.lstrip("/")
        else:
            resolved = (skill_md.parent / normalized).resolve()

        if not resolved.exists():
            errors.append(f"{skill_md}: broken local link: {raw_target}")

    return errors


def parse_catalog_skills(catalog_file: Path) -> set[str]:
    content = catalog_file.read_text(encoding="utf-8")
    discovered: set[str] = set()

    for target in LINK_RE.findall(content):
        normalized = _normalize_local_link(target)
        if not normalized:
            continue

        if normalized == "SKILL.md":
            discovered.add("zephyr-index")
            continue

        m = re.match(r"^\.\./\.\./([a-z0-9-]+)/SKILL\.md$", normalized)
        if m:
            discovered.add(m.group(1))

    return discovered


def check_catalog(expected_skills: set[str]) -> list[str]:
    errors: list[str] = []
    if not CATALOG_FILE.exists():
        return [f"missing catalog file: {CATALOG_FILE}"]

    catalog_skills = parse_catalog_skills(CATALOG_FILE)
    missing = sorted(expected_skills - catalog_skills)
    extra = sorted(catalog_skills - expected_skills)

    if missing:
        errors.append(f"skill_catalog.md missing skill entries: {', '.join(missing)}")
    if extra:
        errors.append(f"skill_catalog.md has unknown skill entries: {', '.join(extra)}")

    return errors


def check_marketplace(expected_skills: set[str]) -> list[str]:
    errors: list[str] = []
    if not MARKETPLACE_FILE.exists():
        return [f"missing marketplace file: {MARKETPLACE_FILE}"]

    data = json.loads(MARKETPLACE_FILE.read_text(encoding="utf-8"))
    plugins = data.get("plugins")
    if not isinstance(plugins, dict):
        return ["marketplace.json: 'plugins' must be an object"]

    if plugins.get("zephyr-skills") != "..":
        errors.append("marketplace.json: 'zephyr-skills' must map to '..'")

    plugin_skill_keys = {k for k in plugins.keys() if k != "zephyr-skills"}
    missing = sorted(expected_skills - plugin_skill_keys)
    extra = sorted(plugin_skill_keys - expected_skills)

    if missing:
        errors.append(f"marketplace.json missing plugin entries: {', '.join(missing)}")
    if extra:
        errors.append(f"marketplace.json has unknown plugin entries: {', '.join(extra)}")

    for skill in sorted(expected_skills):
        expected_path = f"../skills/{skill}"
        got = plugins.get(skill)
        if got != expected_path:
            errors.append(
                f"marketplace.json: plugin '{skill}' should map to '{expected_path}', got '{got}'"
            )

    return errors


def run_all_checks() -> list[str]:
    if not QUICK_VALIDATE.exists():
        raise ValidationError(f"quick validator not found: {QUICK_VALIDATE}")

    skill_dirs = iter_skill_dirs(SKILLS_DIR)
    expected_skills = {d.name for d in skill_dirs}

    errors: list[str] = []

    for skill_dir in skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        errors.extend(check_frontmatter(skill_dir))
        errors.extend(check_skill_sections(skill_md))
        errors.extend(check_skill_links(skill_md))

    errors.extend(check_catalog(expected_skills))
    errors.extend(check_marketplace(expected_skills))

    return errors


def main() -> int:
    try:
        errors = run_all_checks()
    except ValidationError as exc:
        print(f"ERROR: {exc}")
        return 2

    if errors:
        print("Skill quality validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("Skill quality validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
