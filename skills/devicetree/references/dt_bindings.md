# Devicetree Bindings

Bindings define the schema for devicetree nodes. They use YAML format and are located in `dts/bindings/`.

## Anatomy of a Binding
```yaml
description: My custom sensor binding
compatible: "my-company,my-sensor"
include: [sensor-device.yaml, i2c-device.yaml]

properties:
  reg:
    required: true
  my-custom-prop:
    type: uint32
    description: Some custom parameter
```

## `compatible` String
- The `compatible` property in the `.dts` file maps a node to its binding and eventually to the driver.
- Format: `"<vendor>,<model>"`.

## Common Base Bindings
- `base.yaml`: Base definitions for all nodes.
- `gpio-controller.yaml`: Nodes that provide GPIO pins.
- `i2c-device.yaml`: Devices connected via I2C.
- `spi-device.yaml`: Devices connected via SPI.

## Pinctrl Integration
Modern Zephyr uses `pinctrl` nodes to manage pin muxing.
```dts
&my_timer {
    pinctrl-0 = <&timer0_default>;
    pinctrl-names = "default";
};
```
These link to pin definitions usually found in the board's `pinctrl` file.
