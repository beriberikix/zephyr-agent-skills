# OpenThread Integration

Zephyr includes a built-in OpenThread stack, an open-source implementation of the Thread networking protocol. Thread is a low-power, secure, and reliable mesh network for IoT devices.

## Core Concepts
- **Thread Role**: Devices can be Leaders, Routers, OR REEDs (Router Eligible End Devices), or Sleepy End Devices (SED).
- **L2 Layer**: Zephyr integrates OpenThread at the Link Layer (L2).
- **Dataset**: Configuration (PAN ID, Network Name, Master Key) used to join a Thread network.

## Basic Configuration
To enable OpenThread in `prj.conf`:

```kconfig
CONFIG_NETWORKING=y
CONFIG_NET_L2_OPENTHREAD=y
CONFIG_OPENTHREAD_DEBUG=y
CONFIG_OPENTHREAD_L2_DEBUG=y

# Choose OpenThread role
CONFIG_OPENTHREAD_FTD=y   # Full Thread Device (Router capable)
# OR
# CONFIG_OPENTHREAD_MTD=y # Minimal Thread Device (End device)
```

## Initializing the Stack
The stack can be managed via the Zephyr Shell or the OpenThread API.

```c
#include <zephyr/net/openthread.h>
#include <openthread/thread.h>

void init_ot(void) {
    struct openthread_context *ot_ctx = openthread_get_default_context();
    
    // Start OpenThread
    openthread_start(ot_ctx);
    
    // Optional: Set network parameters programmatically
    otInstance *instance = ot_ctx->instance;
    otThreadSetEnabled(instance, true);
}
```

## Shell Management
If `CONFIG_OPENTHREAD_SHELL=y` is enabled, you can manage the device via CLI:
```bash
ot state          # Check device state
ot dataset init new
ot dataset commit active
ot ifconfig up
ot thread start
```

## Best Practices
- **Sleepy End Devices (SED)**: Use `CONFIG_OPENTHREAD_MTD_SED` for battery-powered devices to enable duty-cycling.
- **Border Routers**: A Border Router is required to bridge the Thread mesh to an external IP network (Wi-Fi/Ethernet).
- **Commissioning**: Use Bluetooth Low Energy (BLE) for secure initial network commissioning (see **Matter** reference).
