#!/usr/bin/env python3
"""Generate index.json (registry schema v2) from skills/ + skill-meta.yaml.

index.json is a generated artifact — do not hand-edit it. To change it, edit a
skill's SKILL.md frontmatter `description` or its `skill-meta.yaml`, then re-run
this script. Consumed by `zephyr-cli skills list/show/suggest/install`.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
INDEX_FILE = REPO_ROOT / "index.json"
REPO_SLUG = "beriberikix/zephyr-agent-skills"

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)


def skill_files(skill_dir: Path) -> list[str]:
    """Content files in the skill, relative + sorted. Excludes skill-meta.yaml
    (registry-build metadata, not skill content) and hidden/cache files."""
    out: list[str] = []
    for p in sorted(skill_dir.rglob("*")):
        if not p.is_file():
            continue
        parts = p.relative_to(skill_dir).parts
        if any(part.startswith(".") or part == "__pycache__" for part in parts):
            continue
        rel = p.relative_to(skill_dir).as_posix()
        # Match skill-meta.yaml by basename, not just at the skill root, so a
        # stray copy in a subdirectory is still excluded from `files`.
        if p.name == "skill-meta.yaml" or rel.endswith(".pyc"):
            continue
        out.append(rel)
    return out


def load_frontmatter(skill_md: Path) -> dict:
    m = FRONTMATTER_RE.match(skill_md.read_text(encoding="utf-8"))
    if not m:
        raise SystemExit(f"{skill_md}: no YAML frontmatter")
    return yaml.safe_load(m.group(1)) or {}


def build_skill(skill_dir: Path) -> dict:
    name = skill_dir.name
    fm = load_frontmatter(skill_dir / "SKILL.md")
    if fm.get("name") != name:
        raise SystemExit(
            f"{name}: SKILL.md frontmatter name '{fm.get('name')}' != directory name"
        )

    meta_file = skill_dir / "skill-meta.yaml"
    meta: dict = {}
    if meta_file.exists():
        meta = yaml.safe_load(meta_file.read_text(encoding="utf-8")) or {}
    else:
        print(f"WARNING: {name}: no skill-meta.yaml — matcher metadata will be empty")

    return {
        "name": name,
        "description": fm.get("description", ""),
        "summary": meta.get("summary", ""),
        "keywords": meta.get("keywords", []),
        "aliases": meta.get("aliases", []),
        "kconfig_patterns": meta.get("kconfig_patterns", []),
        "dts_compatible": meta.get("dts_compatible", []),
        "weight": meta.get("weight", 1.0),
        "path": f"skills/{name}",
        "files": skill_files(skill_dir),
    }


def main() -> None:
    # Preserve `updated` from the existing index.json so regeneration never
    # churns the file (keeps the CI diff gate stable); bump it by hand when
    # cutting a registry release.
    updated = "2026-05-18"
    if INDEX_FILE.exists():
        try:
            updated = json.loads(INDEX_FILE.read_text(encoding="utf-8"))["updated"]
        except (json.JSONDecodeError, KeyError, OSError):
            pass

    skills = [
        build_skill(d)
        for d in sorted(SKILLS_DIR.iterdir(), key=lambda p: p.name)
        if d.is_dir() and (d / "SKILL.md").exists()
    ]

    index = {
        "schema_version": "2",
        "repo": REPO_SLUG,
        "updated": updated,
        "skills": skills,
    }
    INDEX_FILE.write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    print(f"Generated {INDEX_FILE} — {len(skills)} skills (schema v2)")


if __name__ == "__main__":
    main()
