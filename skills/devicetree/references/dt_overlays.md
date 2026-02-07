# Devicetree Overlays & HWMv2

Overlays allow modification of the base board devicetree without changing the board definition itself.

## Hardware Model v2 (HWMv2)
Zephyr 3.7+ uses a structured board naming scheme: `board/soc/variant`.
Overlays can now be targeted more precisely:
- `boards/<board>.overlay`: Applies to all variants of the board.
- `boards/<board>_<revision>.overlay`: Applies to a specific revision.
- `boards/<board>_<soc>_<variant>.overlay`: Most specific targeting.

## Overlay Logic
- Overlays are essentially `.dtsi` files that are appended to the main `.dts` during processing.
- You can add property values, add new nodes, or modify existing ones using their labels (e.g., `&i2c0 { ... };`).

## Advanced Customization (from Golioth)
Use deletion patterns to handle "optional" hardware or variant-specific removals:

### Deleting Properties
Useful for boolean properties like `regulator-boot-on` which have no value.
```dts
&my_regulator {
    /delete-property/ regulator-boot-on;
};
```

### Deleting Nodes
Useful when a peripheral exists in hardware but should be ignored or redefined in software.
```dts
/delete-node/ &mode_button;
mode_button: mode-button {
    gpios = <&gpio0 12 GPIO_ACTIVE_HIGH>;
};
```

## Chosen Board Identifier
The `zephyr,chosen` node is used to link generic roles (like `zephyr,console`) to specific hardware nodes.
```dts
chosen {
    zephyr,console = &uart0;
    zephyr,shell-uart = &uart0;
};
```
