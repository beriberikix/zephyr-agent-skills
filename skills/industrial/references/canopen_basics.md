# CANopen Basics

CANopen is a high-level communication protocol for CAN bus systems, widely used in industrial automation, medical equipment, and electric vehicles.

## Core Concepts
- **Object Dictionary (OD)**: The heart of every CANopen device. It's a structured table of all data and parameters.
- **SDO (Service Data Object)**: Used for point-to-point configuration and accessing the Object Dictionary.
- **PDO (Process Data Object)**: Used for real-time data transfer (high speed, no overhead).
- **NMT (Network Management)**: States like Pre-operational, Operational, Stopped.

## Zephyr Integration
Zephyr typically uses the **CANopenNode** stack, integrated as a module.

```kconfig
CONFIG_CANOPEN=y
CONFIG_CANOPEN_NODE_ID=1
```

## Implementation Workflow

### 1. Object Dictionary Generation
Use the `CANopenEditor` or similar tools to generate the `CO_OD.c/.h` files. These describe your device's capabilities (EDS file).

### 2. Processing PDOs
PDOs are mapped to specific CAN IDs. When a PDO is received, the stack automatically updates the corresponding Object Dictionary entry.

```c
// Example: Checking an attribute in the OD
uint32_t val;
CO_OD_get_u32(CO->OD, 0x6040, 0, &val); // Read 'Controlword'
```

## Professional Patterns
- **Heartbeat**: Always enable the Heartbeat producer to allow other nodes to monitor your device's health.
- **SYNC Objects**: Use SYNC to synchronize the execution of multiple nodes (e.g., ensuring four motor controllers start at the exact same time).
- **Emergency (EMCY)**: Use emergency messages to broadcast critical failures immediately.

## See Also
- **[connectivity-usb-can](../../connectivity-usb-can/SKILL.md)**: For CAN bus fundamentals, filters, and USB-to-CAN adapters.
