# Golioth SDK Integration

Golioth is a cloud platform specifically designed for hardware fleets. Its SDK is built as a first-class Zephyr module, utilizing the native networking stack.

## Core Features
1. **LightDB State**: Real-time state synchronization (key-value) between device and cloud.
2. **LightDB Stream**: High-frequency telemetry data storage.
3. **OTA Updates**: Secure firmware updates with release and cohort management.
4. **Remote Logging**: Streaming device logs to the cloud.

## Basic Configuration
Include Golioth in your `west.yml` manifest and enable it in `prj.conf`:

```kconfig
CONFIG_GOLIOTH=y
CONFIG_GOLIOTH_SYSTEM_CLIENT=y

# Authentication
CONFIG_GOLIOTH_DEVICE_ID="my-device@my-project"
CONFIG_GOLIOTH_DEVICE_PSK="my-pre-shared-key"
```

## Implementation Patterns

### 1. Connecting to the Cloud
```c
#include <zephyr/net/golioth/system_client.h>

void main(void) {
    struct golioth_client *client = golioth_system_client_get();
    
    // The system client handles reconnection and authentication
    // in the background.
    golioth_system_client_start();
}
```

### 2. Updating LightDB State
```c
void update_temp(float temp) {
    struct golioth_client *client = golioth_system_client_get();
    
    // Asynchronously push data to "sensor/temp"
    golioth_set_float_async(client, "sensor/temp", temp, NULL, NULL);
}
```

## Professional Strategies
- **Observe Pattern**: Use `golioth_observe()` to receive real-time updates when a value changes on the cloud side (e.g., a "target_state" variable).
- **Settings Sync**: Sync local Zephyr settings with the Golioth cloud using the **Settings Hub** feature.
- **Diagnostics**: Push core dumps and stack statistics to Golioth during development to debug field issues (see **testing-debugging** skill).
