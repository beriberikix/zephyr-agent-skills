# SoC Configuration & Hardware Types

Professional hardware integration involves configuring SoC-level parameters that affect all peripherals and the power profile of the device.

## SoC-Level Kconfig
These symbols are typically defined in the `_defconfig` or `Kconfig` files for your board/SoC.

### 1. Essential Parameters
- `CONFIG_SOC_SERIES_...`: Selects the specific chip family.
- `CONFIG_SYS_CLOCK_HW_CYCLES_PER_SEC`: Architecture-specific core clock setting.
- `CONFIG_MAIN_STACK_SIZE`: Sizing the main thread for the SoC's memory capacity.

### 2. Hardware Features
- `CONFIG_HAS_SEGGER_RTT=y`: Enable debugging interface.
- `CONFIG_FPU=y`: Enable hardware floating-point unit (if available).

## Hardware Types Pattern (from Golioth)
Use SoC-level configuration files to streamline multiple boards or variants that share the same chip.

### 1. Common SoC Overlays
Create a `soc_common.dtsi` for common pins and peripherals shared across variants.
```dts
/* my_soc_common.dtsi */
/ {
    soc {
        /* Shared peripheral base addresses */
    };
};
```

### 2. Product-Specific Variant Overlays
Handle different hardware revisions or SKU variants by including the common file and overriding only what's necessary.

## Naming Conventions
Follow the Zephyr vendor naming convention for SoC-specific directories:
`dts/<arch>/<vendor>/<soc_series>/...`

## Professional Tip: SoC Selection
When choosing a new SoC, verify its support level in the Zephyr repo under `boards/` and `soc/`. A chip with a comprehensive `soc.c` and `.dtsi` will be significantly easier to bring up.
