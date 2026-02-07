# Devicetree Syntax Reference

Core syntax elements for `.dts` and `.dtsi` files.

## Nodes
Nodes are the building blocks of the Devicetree.
```dts
node_label: node-name@unit-address {
    ...
};
```
- `node_label`: Optional. Used to reference the node elsewhere (e.g., `&node_label`).
- `node-name`: Human-readable name.
- `unit-address`: Primary address (e.g., I2C address, memory address).

## Properties
Properties are key-value pairs.
- `status = "okay";` (or `"disabled"`)
- `compatible = "vendor,model";`
- `reg = <address size>;`
- `label = "Human Readable Name";` (Deprecating in favor of node labels)
- `interrupts = <number priority>;`

## Essential Nodes
### `/` (Root Node)
The top of the tree. Contains child nodes like `soc`, `cpus`, `aliases`, and `chosen`.

### `aliases`
Short names for nodes, used by application code.
```dts
aliases {
    led0 = &green_led;
};
```

### `chosen`
Links generic roles to specific hardware.
```dts
chosen {
    zephyr,console = &uart0;
};
```

## Tips for Success
1. **Always use labels**: Reference nodes via `&label` to avoid deep path nesting.
2. **Check your board's `.dts`**: Before writing an overlay, check the base board's final devicetree in `build/zephyr/zephyr.dts`.
3. **Use the binding search**: Search for the `compatible` string in the Zephyr repo to find the corresponding YAML binding.

## Using Devicetree in C Code
Access devicetree data at compile-time using the DT macros:

```c
#include <zephyr/devicetree.h>

#define LED0_NODE DT_ALIAS(led0)

#if DT_NODE_HAS_STATUS(LED0_NODE, okay)
    const struct gpio_dt_spec led = GPIO_DT_SPEC_GET(LED0_NODE, gpios);
#else
    #error "LED0 not available"
#endif
```

