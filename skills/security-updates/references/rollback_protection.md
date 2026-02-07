# Rollback Protection & Fail-Safe Updates

The most critical requirement for a field-deployed device is the ability to recover from a failed firmware update. Zephyr and MCUboot provide an atomic swap mechanism that guarantees a working system.

## The Swap Mechanism
MCUboot manages two primary "slots":
1. **Slot 0 (Primary)**: The currently running firmware.
2. **Slot 1 (Secondary)**: The newly downloaded firmware.

### Atomic Swap
When an update is triggered, MCUboot swaps the contents of Slot 0 and Slot 1. If Slot 0 becomes corrupt during the swap (e.g., power loss), MCUboot can resume the process on the next boot.

## Image Confirmation
By default, MCUboot treats a new image as "pending" for a single boot.

### The "Test" State
If you use `mcumgr image test`, the device reboots into the new firmware. If the application does **not** confirm the image, MCUboot will automatically swap back to the old, known-good firmware on the next reboot.

### Confirming the Image
Your application must explicitly confirm it is healthy after a successful boot:

```c
#include <zephyr/dfu/mcuboot.h>

void main(void) {
    // Perform self-tests...
    
    // If healthy, confirm the image
    if (boot_is_img_confirmed() == 0) {
        int err = boot_write_img_confirmed();
        if (err) {
            // Handle error
        }
    }
}
```

## Rollback Protection
MCUboot can be configured to prevent "downgrades" to older versions that may have security flaws.

```kconfig
# Prevent booting an image with a lower version than currently running
CONFIG_BOOT_UPGRADE_ONLY=y
```

## Professional Strategy: Connectivity Check
A common professional pattern is to require a successful cloud connection (e.g., to Golioth) *before* calling `boot_write_img_confirmed()`. This ensures that even if the app boots, if it can't communicate with the server, it will roll back so it can be updated again.
