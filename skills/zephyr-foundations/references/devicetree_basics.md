# Devicetree Fundamentals

Devicetree (DT) describes hardware topology. It is NOT for configuration (that's Kconfig).

## Core Syntax
- **Nodes**: Represent hardware components (e.g., `gpio0: gpio@40022000`).
- **Properties**: key-value pairs (e.g., `reg = <0x40022000 0x1000>;`).
- **Labels**: Aliases for nodes (e.g., `&gpio0` points to the node labeled `gpio0`).

## Common Property Types
- `phandle`: Link to another node (e.g., `gpios = <&gpio0 12 GPIO_ACTIVE_LOW>;`).
- `string`: `"text"`.
- `uint32`: `<val>`.
- `boolean`: Just the key presence (e.g., `regulator-boot-on;`).

## Overlays (`.overlay`)
- Applications use overlays to modify base board definitions.
- New in Zephyr 3.7 (HWMv2): Overlays can be SoC-specific.

## Advanced Deletion (from Golioth)
- **/delete-property/ property-name;**: Use this to remove a boolean property or reset an inherited value.
- **/delete-node/ &node_label;**: Completely removes a node and its children. Use when redefining a peripheral or removing hardware items not present in a variant.

## C Macro Integration
- `DT_NODE_HAS_STATUS(node, status)`: Check if a node is "okay".
- `DT_PROP(node, prop)`: Get a property value.
- `DT_GPIO_CTLR(node, prop)`: Get the GPIO controller phandle.
