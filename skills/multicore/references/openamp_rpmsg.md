# OpenAMP & RPMsg

For heterogeneous multicore systems (e.g., Cortex-M7 + Cortex-M4), Zephyr utilizes the **OpenAMP** framework to manage the lifecycle of remote cores and enable communication.

## Core Concepts
- **AMP (Asymmetric Multiprocessing)**: Cores run independent firmware images.
- **RPMsg (Remote Processor Messaging)**: A virtio-based message passing protocol.
- **Vring**: Shared memory buffers used for message exchange.
- **Resource Table**: A structure defined in the remote core binary that describes its memory and IPC requirements to the primary core.

## Configuration
Include OpenAMP as a module and enable it in `prj.conf`:

```kconfig
CONFIG_OPENAMP=y
CONFIG_IPM=y               # Inter-Processor Mailbox (mailbox driver)
CONFIG_OPENAMP_RSC_TABLE=y # Enable resource table support
```

## Implementation Patterns

### 1. Initializing RPMsg
Both cores must initialize the RPMsg stack and establish a "channel".

```c
#include <zephyr/ipc/rpmsg_service.h>

static int endpoint_id;

int rpmsg_cb(struct rpmsg_endpoint *ept, void *data, size_t len, uint32_t src, void *priv) {
    // Handle incoming message
    return RPMSG_SUCCESS;
}

void init_ipc(void) {
    // Register an endpoint
    endpoint_id = rpmsg_service_register_endpoint("my_channel", rpmsg_cb);
}
```

### 2. Sending Messages
```c
void send_to_remote(void *data, size_t len) {
    rpmsg_service_send(endpoint_id, data, len);
}
```

## Linux Interoperability
OpenAMP/RPMsg is compatible with the Linux `rpmsg` driver. This allows a Cortex-M core running Zephyr to communicate seamlessly with an A-class core running Linux (e.g., on an STM32MP1 or i.MX8).

## Professional Strategies
- **Zero-Copy**: For large data transfers (e.g., audio buffers), use shared memory regions directly and only pass pointers/offsets via RPMsg.
- **Lifecycle Management**: Use the primary core to load the remote core's binary into RAM and release it from reset using the `remoteproc` API.
- **Priority**: Use the Inter-Processor Mailbox (IPM) driver for high-priority signaling separate from the standard RPMsg data channel.
