# Zephyr Agent Skill Catalog

This catalog maps common Zephyr RTOS development tasks to the appropriate **Agent Skill**. Use this to find the right tool for your specific objective.

## Master Index
- **[zephyr-index](file:///Users/jberi/code/zephyr-agent-skills/skills/zephyr-index/SKILL.md)**: Navigation hub and decision tree for all skills.

---

## Phase 1: Foundations & Essential Workflows

| Skill | Triggers / Use Cases |
| :--- | :--- |
| **[zephyr-foundations](file:///Users/jberi/code/zephyr-agent-skills/skills/zephyr-foundations/SKILL.md)** | Embedded C patterns (BIT, CONTAINER_OF), concurrency primitives, hardware literacy, defensive programming. |
| **[build-system](file:///Users/jberi/code/zephyr-agent-skills/skills/build-system/SKILL.md)** | West workspace management, Sysbuild multi-image builds, Kconfig configuration, CMake integration. |
| **[devicetree](file:///Users/jberi/code/zephyr-agent-skills/skills/devicetree/SKILL.md)** | DT syntax, bindings, overlays, /delete-node/ and /delete-property/ operations. |
| **[native-sim](file:///Users/jberi/code/zephyr-agent-skills/skills/native-sim/SKILL.md)** | Building and testing for Linux/macOS/Windows simulation targets. |
| **[board-bringup](file:///Users/jberi/code/zephyr-agent-skills/skills/board-bringup/SKILL.md)** | Creating new board definitions using Hardware Model v2 (HWMv2). |
| **[zephyr-module](file:///Users/jberi/code/zephyr-agent-skills/skills/zephyr-module/SKILL.md)** | Creating out-of-tree modules and module.yml configuration. |
| **[kernel-basics](file:///Users/jberi/code/zephyr-agent-skills/skills/kernel-basics/SKILL.md)** | Thread management, logging subsystem, shell command integration. |

---

## Phase 2: Common Features

| Skill | Triggers / Use Cases |
| :--- | :--- |
| **[kernel-services](file:///Users/jberi/code/zephyr-agent-skills/skills/kernel-services/SKILL.md)** | Zbus, SMF (State Machine), Work Queues, IRQs, Settings, Events. |
| **[hardware-io](file:///Users/jberi/code/zephyr-agent-skills/skills/hardware-io/SKILL.md)** | Pinctrl, GPIO, Sensors, DMA, ADC, DAC, Input subsystem. |
| **[power-performance](file:///Users/jberi/code/zephyr-agent-skills/skills/power-performance/SKILL.md)** | Power management (PM), performance tuning, code/data relocation. |

---

## Phase 3: Advanced Features *(Coming Soon)*

| Skill | Triggers / Use Cases |
| :--- | :--- |
| **connectivity-ble** | Bluetooth Low Energy (GAP, GATT, pairing, bonding). |
| **connectivity-ip** | IPv4/IPv6 sockets, LwM2M, CoAP, MQTT. |
| **connectivity-usb-can** | USB Device classes (CDC-ACM, HID, etc.), CAN and CAN-FD. |
| **storage** | Flash storage (NVS, FCB), filesystems (LittleFS), partitions. |
| **testing-debugging** | Twister, Ztest, Thread Analyzer, Tracing, GDB/Coredump. |

---

## Phase 4: Production & Specialized *(Coming Soon)*

| Skill | Triggers / Use Cases |
| :--- | :--- |
| **security-updates** | MCUboot, TF-M (Trusted Firmware-M), DFU/FOTA, Crypto, mbedTLS. |
| **iot-protocols** | OpenThread, Golioth, LoRaWAN, Matter. |
| **multicore** | SMP, AMP, IPC (OpenAMP), LLEXT (Linkable Extensions), Userspace. |
| **industrial** | Modbus RTU/TCP, CANopen. |
| **specialized** | Audio (I2S/Codec), Display (LVGL), Fault injection/Watchdogs. |
