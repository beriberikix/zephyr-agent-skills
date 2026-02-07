# Zephyr Quick Reference

Common tasks and the corresponding **Agent Skill** to use.

## Workspace & Build
- "How do I add a repo to west.yml?" -> **build-system**
- "How do I build for MCUboot?" -> **build-system** (sysbuild)
- "My build is failing with Kconfig errors." -> **build-system**
- "I need to add an out-of-tree module." -> **zephyr-module**

## Hardware & Devicetree
- "How do I map this pin in DTS?" -> **devicetree**
- "I need to delete a regulator property in my overlay." -> **devicetree**
- "How do I create a new board for Hardware Model v2?" -> **board-bringup**
- "How do I configure this I2C sensor?" -> **hardware-io**

## Kernel & Logic
- "How do I create a thread with a specific priority?" -> **kernel-basics**
- "I need to use Zbus for inter-thread communication." -> **kernel-services**
- "How do I implement a state machine in Zephyr?" -> **kernel-services** (SMF)
- "How do I save settings to persistent flash?" -> **kernel-services**

## Connectivity
- "How do I scan for BLE heart rate monitors?" -> **connectivity-ble**
- "How do I send an MQTT message?" -> **connectivity-ip**
- "How do I use USB CDC-ACM?" -> **connectivity-usb-can**

## Production
- "I need to sign my image for MCUboot." -> **security-updates**
- "How do I run tests with Twister?" -> **testing-debugging**
- "How do I isolate a process using userspace?" -> **multicore**
