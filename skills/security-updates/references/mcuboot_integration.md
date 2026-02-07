# MCUboot Integration

MCUboot is the industry-standard secure bootloader for 32-bit microcontrollers. Zephyr provides deep integration with MCUboot for secure boot and fail-safe firmware updates.

## Flash Partitioning
The foundation of MCUboot is a specific flash layout defined in Devicetree.

### Typical Dual-Slot Layout
```dts
/ {
    chosen {
        zephyr,code-partition = &slot0_partition;
    };
};

&flash0 {
    partitions {
        compatible = "fixed-partitions";
        #address-cells = <1>;
        #size-cells = <1>;

        boot_partition: partition@0 {
            label = "mcuboot";
            reg = <0x00000000 DT_SIZE_K(48)>;
        };
        slot0_partition: partition@c000 {
            label = "image-0";
            reg = <0x0000c000 DT_SIZE_K(200)>;
        };
        slot1_partition: partition@3e000 {
            label = "image-1";
            reg = <0x0003e000 DT_SIZE_K(200)>;
        };
        scratch_partition: partition@70000 {
            label = "image-scratch";
            reg = <0x00070000 DT_SIZE_K(8)>;
        };
        storage_partition: partition@72000 {
            label = "storage";
            reg = <0x00072000 DT_SIZE_K(8)>;
        };
    };
};
```

## Basic Configuration
To build an MCUboot-compatible application, add the following to `prj.conf`:

```kconfig
CONFIG_BOOTLOADER_MCUBOOT=y
```

## Building MCUboot
MCUboot is usually built as a separate Zephyr application located in `bootloader/mcuboot/boot/zephyr`.

```bash
west build -b <board> bootloader/mcuboot/boot/zephyr
```

## Best Practices
- **Slot Alignment**: `slot0` and `slot1` must be identical in size to ensure updates can swap correctly.
- **Hardware-Specific Offsets**: Always consult your SoC's reference manual for the correct starting address of the flash.
- **Sysbuild**: In modern Zephyr, use **Sysbuild** to build both MCUboot and your application in a single command.
