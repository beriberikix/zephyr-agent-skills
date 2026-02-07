# Flash Management

Properly managing flash memory requires understanding how partitions are defined in Devicetree and how to access hardware layout information at runtime.

## Devicetree Partitions
The `fixed-partitions` node in Devicetree defines how physical flash is carved up for different uses (bootloader, application, storage).

```dts
/ {
    soc {
        flash-controller@4001e000 {
            flash0: flash@0 {
                partitions {
                    compatible = "fixed-partitions";
                    #address-cells = <1>;
                    #size-cells = <1>;

                    boot_partition: partition@0 {
                        label = "mcuboot";
                        reg = <0x00000000 DT_SIZE_K(48)>;
                    };
                    storage_partition: partition@3e000 {
                        label = "storage";
                        reg = <0x0003e000 DT_SIZE_K(8)>;
                    };
                };
            };
        };
    };
};
```

## Runtime Access
Use macros to retrieve partition details without hardcoding addresses.

```c
#include <zephyr/storage/flash_map.h>

#define STORAGE_NODE DT_NODE_BY_FIXED_PARTITION_LABEL(storage)
#define STORAGE_OFFSET FIXED_PARTITION_OFFSET(storage_partition)
#define STORAGE_SIZE FIXED_PARTITION_SIZE(storage_partition)
```

## Flash Layout API
When performing raw flash operations, you must account for the page/sector size of the hardware.

```c
#include <zephyr/drivers/flash.h>

const struct device *flash_dev = DEVICE_DT_GET(DT_CHOSEN(zephyr_flash_controller));
struct flash_pages_info info;

// Get info about a specific page
flash_get_page_info_by_offs(flash_dev, 0x3e000, &info);
printf("Page size: %d, index: %d\n", info.size, info.index);
```

## Professional Strategies
- **Flash Protection**: Use `FLASH_WRITE_PROTECTION` if the hardware supports it to prevent accidental corruption of critical data.
- **Alignment**: Flash writes must often be aligned to a specific boundary (e.g., 4 or 8 bytes). Use `flash_get_write_block_size(flash_dev)` to check this at runtime.
- **Off-Chip Flash**: If using SPI Flash, ensure the `nordic,qspi-nor` or similar compatible driver is correctly configured in Devicetree.
