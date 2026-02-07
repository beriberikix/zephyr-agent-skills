# Zephyr Agent Skills

**A comprehensive knowledge base of professional skills for building with Zephyr RTOS.**

This repository contains a curated collection of "skills"—modular packages of knowledge, code patterns, and best practices—designed to assist AI agents and human developers in building high-quality embedded systems with Zephyr.

## 📚 Skill Catalog

The master index for all skills is located within the `zephyr-index` skill:

👉 **[Master Skill Catalog](skills/zephyr-index/references/skill_catalog.md)**

### Quick Links by Category

#### Phase 1: Foundations
*   **[zephyr-foundations](skills/zephyr-foundations/SKILL.md)**: Embedded C patterns & safe coding.
*   **[build-system](skills/build-system/SKILL.md)**: West, Sysbuild, Kconfig, & CMake.
*   **[devicetree](skills/devicetree/SKILL.md)**: Syntax, bindings, & hardware description.
*   **[native-sim](skills/native-sim/SKILL.md)**: Simulation & host-based testing.
*   **[board-bringup](skills/board-bringup/SKILL.md)**: Custom board definitions (HWMv2).

#### Phase 2: Core Features
*   **[kernel-services](skills/kernel-services/SKILL.md)**: Threads, Work Queues, Zbus, & Logging.
*   **[hardware-io](skills/hardware-io/SKILL.md)**: GPIO, I2C, SPI, DMA, & Sensors.
*   **[power-performance](skills/power-performance/SKILL.md)**: PM states, optimized builds, & RAM tuning.

#### Phase 3: Connectivity
*   **[connectivity-ble](skills/connectivity-ble/SKILL.md)**: Bluetooth Low Energy (GAP/GATT).
*   **[connectivity-ip](skills/connectivity-ip/SKILL.md)**: IPv6, CoAP, MQTT, & LwM2M.
*   **[connectivity-usb-can](skills/connectivity-usb-can/SKILL.md)**: USB device classes & CAN bus.

#### Phase 4: Production & Specialized
*   **[security-updates](skills/security-updates/SKILL.md)**: MCUboot, Image Signing, & DFU.
*   **[iot-protocols](skills/iot-protocols/SKILL.md)**: OpenThread, Matter, & Golioth.
*   **[multicore](skills/multicore/SKILL.md)**: SMP, OpenAMP, & IPC.
*   **[industrial](skills/industrial/SKILL.md)**: Modbus RTU/TCP & CANopen.
*   **[specialized](skills/specialized/SKILL.md)**: Audio, LVGL GUI, & Reliability.

---

## 📂 Repository Structure

```
.
├── skills/                 # The core collection of skills
│   ├── zephyr-index/       # Navigation hub
│   ├── zephyr-foundations/ # Essential C & RTOS patterns
│   └── ... (see catalog)
├── .agent/                 # Agent-specific configurations
└── README.md               # This file
```

## 🛠 Usage

### For AI Agents
*   **Discovery**: Start by reading `skills/zephyr-index/SKILL.md` to understand the available capabilities.
*   **Implementation**: When a user requests a task (e.g., "Add BLE support"), locate the corresponding skill (`connectivity-ble`) and strictly follow the patterns in its `references/` directory.
*   **Verification**: Use the code examples provided in `references/` as ground truth for syntax and API usage.

### For Human Developers
*   **Learning**: Treat each skill as a focused tutorial. The `references/` folder in each skill contains "cheat sheets" for specific topics.
*   **Best Practices**: The content emphasizes professional, production-ready patterns over simple "Hello World" examples.

## 🤝 Contributing

Each skill is a self-contained directory with the following structure:
*   `SKILL.md`: Entry point and quick start.
*   `references/*.md`: Detailed technical guides and code snippets.
*   `scripts/` & `assets/`: Helper files (where applicable).

To add a new skill, use the `skill-creator` utility or follow the structure of existing skills.
