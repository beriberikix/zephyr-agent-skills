# LLEXT (Linkable Extensions)

**LLEXT** is a modern Zephyr feature that allows devices to dynamically load and execute binary modules (ELF files) from storage (SD card, flash) into RAM at runtime.

## Core Concepts
- **Dynamic Loading**: Extends your application's functionality without a full firmware update.
- **Isolation**: Extensions can be isolated using MPU/MMU (optional).
- **Relocation**: The loader handles symbol relocation if the module is built for a different address.

## Configuration
To enable the LLEXT subsystem:

```kconfig
CONFIG_LLEXT=y
CONFIG_LLEXT_STORAGE_FLASH=y
```

## Basic Workflow

### 1. The Extension (Compiled Separately)
Extensions are typically compiled as position-independent code (PIC).

```c
// hello_ext.c
#include <zephyr/kernel.h>

void ext_main(void) {
    printk("Hello from a dynamic extension!\n");
}
```

### 2. Loading the Extension
```c
#include <zephyr/llext/llext.h>

void load_and_run(void) {
    struct llext *ext;
    struct llext_loader l;
    
    // Provide a loader (e.g., from flash or buffer)
    llext_flash_loader_init(&l, "/SD:/hello.elf");
    
    // Load and relocate
    int err = llext_load(&l, "my_ext", &ext, NULL);
    if (!err) {
        // Call a function exported by the extension
        llext_call_fn(ext, "ext_main");
    }
}
```

## Use Cases
- **User Scripts**: Loading "Applets" on a smartwatch or dashboard.
- **Hardware Drivers**: Dynamically loading a driver for a newly attached peripheral.
- **AI Models**: Loading different model weights/logic based on the detected environment.

## Security Considerations

> [!CAUTION]
> **Always verify the signature of an LLEXT module before loading it!** Unsigned or improperly signed extensions can execute arbitrary code with full system privileges. Use the **[security-updates](../../security-updates/SKILL.md)** skill patterns for image signing and verification.

## Best Practices
- **Symbol Export**: Use `EXPORT_SYMBOL(fn_name)` in your main application to make functions available to the extension.
- **Memory Management**: Extensions consume heap or statically reserved RAM. Ensure your system has enough headroom.
- **Version Control**: Track extension versions to prevent loading incompatible modules.
