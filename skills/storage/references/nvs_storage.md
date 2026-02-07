# Non-Volatile Storage (NVS)

NVS is the recommended backend for Zephyr's settings subsystem. It provides a way to store binary blobs, strings, and integers in flash memory while managing wear leveling.

## Core Concepts
- **NVS File System**: A region of flash partitioned for NVS use.
- **Entry ID**: A unique identifier (16-bit) for each data item stored.
- **Wear Leveling**: NVS automatically cycles through flash sectors to prevent premature wear.

## Basic Configuration
Enable NVS in your `prj.conf`:

```kconfig
CONFIG_NVS=y
CONFIG_FLASH=y
CONFIG_FLASH_PAGE_LAYOUT=y
```

## Implementation

### 1. Initialization
First, define and initialize the NVS file system structure.

```c
#include <zephyr/drivers/flash.h>
#include <zephyr/storage/nvs/nvs.h>

static struct nvs_fs fs;

void init_storage(void) {
    fs.flash_device = DEVICE_DT_GET(DT_CHOSEN(zephyr_flash_controller));
    fs.offset = FIXED_PARTITION_OFFSET(storage_partition);
    
    // Note: The storage_partition label must match a partition defined in your
    // board's Devicetree. See flash_management.md for partition configuration.
    
    struct flash_pages_info info;
    flash_get_page_info_by_offs(fs.flash_device, fs.offset, &info);
    fs.sector_size = info.size;
    fs.sector_count = 3; // Number of sectors allocated

    int rc = nvs_mount(&fs);
    if (rc) {
        printk("NVS mount failed: %d\n", rc);
        return;
    }
}
```

### 2. Reading and Writing
```c
#define BOOT_COUNT_ID 1
uint32_t count = 0;

// Read
nvs_read(&fs, BOOT_COUNT_ID, &count, sizeof(count));

// Write
count++;
nvs_write(&fs, BOOT_COUNT_ID, &count, sizeof(count));
```

## Best Practices
- **ID Management**: Maintain a central header file defining all NVS IDs to avoid collisions.
- **Data Integrity**: NVS entries are protected by a CRC. Always check return codes for `nvs_read` and `nvs_write`.
- **Garbage Collection**: NVS automatically erases old sectors when full. Ensure you have enough sectors (at least 2) for this process to succeed.
