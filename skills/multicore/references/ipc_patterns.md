# IPC Patterns & Services

Inter-Processor Communication (IPC) in Zephyr is handled by several subsystems depending on the level of abstraction and hardware capabilities.

## High-Level: IPC Service
The **IPC Service** provides a generic endpoint-based API that abstracts the underlying transport (RPMsg, shared memory, etc.).

```kconfig
CONFIG_IPC_SERVICE=y
CONFIG_IPC_SERVICE_BACKEND_RPMSG=y
```

### Usage
```c
#include <zephyr/ipc/ipc_service.h>

void endpoint_cb(const void *data, size_t len, void *priv) {
    // Handle received data
}

void init_ipc_service(void) {
    const struct device *ipc_dev = DEVICE_DT_GET(DT_NODELABEL(ipc0));
    struct ipc_ept_cfg cfg = {
        .name = "my_endpoint",
        .cb = { .recv = endpoint_cb },
    };
    
    ipc_service_register_endpoint(ipc_dev, &ept, &cfg);
}
```

## Low-Level: IPM (Inter-Processor Mailbox)
The **IPM** driver handles hardware mailboxes or doorbells for simple signaling between cores.

```kconfig
CONFIG_IPM=y
```

### Usage
```c
#include <zephyr/drivers/ipm.h>

void send_signal(void) {
    const struct device *ipm_dev = DEVICE_DT_GET(DT_NODELABEL(mailbox0));
    
    // Send a 32-bit value to the remote core
    ipm_send(ipm_dev, 0, 0x12345678, NULL, 0);
}
```

## Shared Memory & Zero-Copy
For high-bandwidth data (e.g., image sensors), allocate a specific memory region shared by both cores.

### Devicetree for Shared RAM
```dts
reserved-memory {
    shared_ram: shared_ram@20040000 {
        reg = <0x20040000 0x8000>;
    };
};
```

### Accessing Shared Memory
```c
#include <zephyr/devicetree.h>

#define SHARED_RAM_ADDR DT_REG_ADDR(DT_NODELABEL(shared_ram))
#define SHARED_RAM_SIZE DT_REG_SIZE(DT_NODELABEL(shared_ram))

void access_shared(void) {
    volatile uint8_t *shared_ptr = (uint8_t *)SHARED_RAM_ADDR;
    // Perform zero-copy data operations
}
```

## Best Practices
- **Cache Management**: Before reading from shared RAM, ensure you invalidate the cache. Before writing, ensure you flush (clean) the cache.
- **Mutex vs. Spinlock**: Use `k_mutex` for long synchronization inside threads on a single core, but **must** use `k_spinlock` for cross-core synchronization.
- **Protocol Standardization**: Use RPMsg if you need a standard protocol; use raw shared memory + IPM signaling if you need absolute minimum latency.
