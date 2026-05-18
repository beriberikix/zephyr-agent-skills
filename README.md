# Zephyr Agent Skills

**A registry of professional, agent-ready skills for building with Zephyr RTOS.**

This repository is a curated collection of "skills" — modular packages of knowledge, code
patterns, and best practices that help AI agents and human developers build high-quality
embedded systems with Zephyr. Each skill is a `SKILL.md` plus supporting `references/`,
`scripts/`, and `assets/`.

## Using the skills

### With `zephyr-cli` (recommended)

[`zephyr-cli`](https://github.com/beriberikix/zephyr-cli) is the primary way agents consume
this registry. It selects the right skill **deterministically** — no guessing:

```bash
zephyr-cli skills suggest "enable an i2c sensor in my devicetree overlay"
zephyr-cli skills install devicetree
```

`skills suggest` scores your task against every skill's keywords, aliases, Kconfig patterns,
and devicetree compatibles and returns a ranked list with the reasons each matched.
`skills install` fetches the chosen skill into your workspace.

### As a Claude Code plugin

The repository can also be added as a Claude Code plugin marketplace:

```bash
claude plugin marketplace add beriberikix/zephyr-agent-skills
claude plugin install zephyr-skills@zephyr-agent-skills
```

The umbrella `zephyr-skills` skill (the repo-root `SKILL.md`) is a broad entry point that
routes agents to `zephyr-cli skills suggest` for deterministic skill selection.

## The registry — `index.json`

`index.json` is the machine-readable registry consumed by `zephyr-cli`. It is a **generated
artifact — do not edit it by hand.** It is built from each skill's `SKILL.md` frontmatter
plus a per-skill `skill-meta.yaml` sidecar:

```bash
python scripts/generate_index.py
```

`skill-meta.yaml` holds the curated matcher metadata — `summary`, `keywords`, `aliases`,
`kconfig_patterns`, `dts_compatible`, and `weight`. `scripts/validate_skills.py` (run in CI)
keeps `index.json`, `.claude-plugin/marketplace.json`, and the skill set consistent.

## Skill catalog

👉 **[Master Skill Catalog](skills/zephyr-index/references/skill_catalog.md)** — every skill,
grouped by domain (foundations & build, hardware & peripherals, connectivity, production &
advanced). Or just run `zephyr-cli skills suggest` and let the matcher pick.

## Repository structure

```
.
├── skills/                       # the skills — one directory each
│   └── <skill>/
│       ├── SKILL.md              # entry point (Quick Start + Validation Checklist)
│       ├── skill-meta.yaml       # curated matcher metadata for the registry
│       ├── references/           # detailed technical guides
│       └── scripts/, assets/     # helper files (where applicable)
├── index.json                    # generated machine-readable registry (consumed by zephyr-cli)
├── SKILL.md                       # umbrella skill — Claude Code entry point
├── scripts/
│   ├── generate_index.py         # regenerates index.json
│   ├── generate_marketplace.py   # regenerates .claude-plugin/marketplace.json
│   └── validate_skills.py        # repository quality gate
└── .claude-plugin/marketplace.json
```

## Contributing

Each skill is a self-contained directory: a `SKILL.md` (with `## Quick Start` and
`## Validation Checklist` sections), a `skill-meta.yaml`, and optional `references/`,
`scripts/`, and `assets/`.

To add or change a skill:

1. Edit or create the skill under `skills/<name>/`.
2. Update its `skill-meta.yaml` matcher metadata (`keywords`/`aliases` quality directly
   drives `zephyr-cli skills suggest` accuracy).
3. Run `python scripts/generate_index.py` and `python scripts/generate_marketplace.py`.
4. Run `python scripts/validate_skills.py` — it must pass.

Commit the regenerated `index.json` and `marketplace.json`; CI verifies they are in sync
with `skills/`.
