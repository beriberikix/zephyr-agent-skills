---
name: zephyr-agent-skills
description: Zephyr RTOS development — boards and devicetree, the build system (west, Kconfig, CMake, sysbuild), drivers and peripherals, BLE and networking, the kernel, storage, power, testing and debugging, security and OTA. Use this for ANY Zephyr RTOS or embedded-firmware task on a Zephyr project; it routes you to the right specialized skill via the zephyr-cli registry.
---

# Zephyr Agent Skills

The entry point for Zephyr RTOS development. Behind this are 20+ specialized skills
(`devicetree`, `build-system`, `connectivity-ble`, `testing-debugging`, and more) — but do not
guess which one to read. Skill selection is deterministic, via `zephyr-cli`.

## How to get the right skill

1. **Find it** — run `zephyr-cli skills suggest` with a short description of your task. Add
   `--kconfig` symbols or `--dts` compatibles when you know them. It returns the best-matching
   skills, ranked, with scores and the reasons each matched.
2. **Install it** — `zephyr-cli skills install NAME` fetches that skill's `SKILL.md` and its
   reference files into the workspace.
3. **Apply it** — read the installed `SKILL.md` and follow it.

If `zephyr-cli` is not available, browse the human catalog at
[skills/zephyr-index/references/skill_catalog.md](skills/zephyr-index/references/skill_catalog.md).

## Quick Start

    zephyr-cli skills suggest "enable an i2c sensor in my devicetree overlay"
    zephyr-cli skills install devicetree
