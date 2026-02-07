# Zephyr Agent Skill Catalog

This catalog maps common Zephyr RTOS development tasks to the appropriate **Agent Skill**. Use this to find the right tool for your specific objective.

## Master Index
- **[zephyr-index](SKILL.md)**: Navigation hub and decision tree for all skills.

---

## Phase 1: Foundations & Essential Workflows

| Skill | Triggers / Use Cases |
| :--- | :--- |
| **[zephyr-foundations](../../zephyr-foundations/SKILL.md)** | Embedded C patterns (BIT, CONTAINER_OF), concurrency primitives, hardware literacy, defensive programming. |
| **[build-system](../../build-system/SKILL.md)** | West workspace management, Sysbuild multi-image builds, Kconfig configuration, CMake integration. |
| **[devicetree](../../devicetree/SKILL.md)** | DT syntax, bindings, overlays, /delete-node/ and /delete-property/ operations. |
| **[native-sim](../../native-sim/SKILL.md)** | Building and testing for Linux/macOS/Windows simulation targets. |
| **[board-bringup](../../board-bringup/SKILL.md)** | Creating new board definitions using Hardware Model v2 (HWMv2). |
| **[zephyr-module](../../zephyr-module/SKILL.md)** | Creating out-of-tree modules and module.yml configuration. |
| **[kernel-basics](../../kernel-basics/SKILL.md)** | Thread management, logging subsystem, shell command integration. |

---

## Phase 2: Common Features

| Skill | Triggers / Use Cases |
| :--- | :--- |
| **[kernel-services](../../kernel-services/SKILL.md)** | Zbus, SMF (State Machine), Work Queues, IRQs, Settings, Events. |
| **[hardware-io](../../hardware-io/SKILL.md)** | Pinctrl, GPIO, Sensors, DMA, ADC, DAC, Input subsystem. |
| **[power-performance](../../power-performance/SKILL.md)** | Power management (PM), performance tuning, code/data relocation. |

---

## Phase 3: Connectivity & Advanced Workflows

| Skill | Triggers / Use Cases |
| :--- | :--- |
| **[connectivity-ble](../../connectivity-ble/SKILL.md)** | Bluetooth Low Energy (GAP, GATT, pairing), Send-When-Idle pattern. |
| **[connectivity-ip](../../connectivity-ip/SKILL.md)** | IPv4/IPv6, LwM2M, CoAP, MQTT, modular IP stack configuration. |
| **[connectivity-usb-can](../../connectivity-usb-can/SKILL.md)** | USB Device classes (CDC ACM, HID), CAN bus diagnostics and adapters. |
| **[storage](../../storage/SKILL.md)** | Flash storage (NVS), partitions, flash layout management. |
| **[testing-debugging](../../testing-debugging/SKILL.md)** | Twister test suites, Ztest frameworks, Tracing, Thread Analyzer. |

---

## Phase 4: Production & Specialized 

| Skill | Triggers / Use Cases |
| :--- | :--- |
| **[security-updates](../../security-updates/SKILL.md)** | MCUboot, TF-M (Trusted Firmware-M), DFU/FOTA, Crypto, mbedTLS. |
| **[iot-protocols](../../iot-protocols/SKILL.md)** | OpenThread, Golioth, LoRaWAN, Matter. |
| **[multicore](../../multicore/SKILL.md)** | SMP, AMP, IPC (OpenAMP), LLEXT (Linkable Extensions), Userspace. |
| **[industrial](../../industrial/SKILL.md)** | Modbus RTU/TCP, CANopen. |
| **[specialized](../../specialized/SKILL.md)** | Audio (I2S/Codec), Display (LVGL), Fault injection/Watchdogs. |
