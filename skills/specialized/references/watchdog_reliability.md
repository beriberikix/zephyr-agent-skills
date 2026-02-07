# Watchdog & System Reliability

In production systems, reliability is paramount. Zephyr provides a standardized **Watchdog (WDT)** API to ensure the system recovers from software hangs or deadlocks.

## Core Concepts
- **Watchdog Timer**: A hardware timer that triggers a system reset if not "fed" or "kicked" regularly.
- **Windowed Watchdog**: Requires feeding within a specific time window (too early or too late triggers reset).
- **Stall Protection**: Detects when a low-priority thread is being starved by a higher-priority one.

## Configuration
```kconfig
CONFIG_WATCHDOG=y
```

## Basic Implementation

### 1. Initializing the Watchdog
```c
#include <zephyr/drivers/watchdog.h>

void init_wdt(void) {
    const struct device *wdt_dev = DEVICE_DT_GET(DT_ALIAS(watchdog0));
    struct wdt_timeout_cfg wdt_config = {
        .window.min = 0,
        .window.max = 5000, // 5 second timeout
        .callback = NULL,    // Set to a function for log cleanup before reset
        .flags = WDT_FLAG_RESET_SOC,
    };

    int wdt_channel = wdt_install_timeout(wdt_dev, &wdt_config);
    wdt_setup(wdt_dev, WDT_OPT_PAUSE_IN_SLEEP);
}
```

### 2. "Feeding" the Watchdog
Ideally, feed the watchdog from your main application loop or a dedicated monitor thread.

```c
void main_loop(void) {
    while (1) {
        // Perform work...
        
        wdt_feed(wdt_dev, wdt_channel);
        k_sleep(K_MSEC(1000));
    }
}
```

## Professional Reliability Patterns
- **Health Checks**: Instead of simple feeding, check the health of all critical threads (e.g., via a bitmask) before calling `wdt_feed()`.
- **Fault Handlers**: Implement a custom `arch_system_halt()` or `k_oops` handler to log the CPU state and stack trace to NVS before the watchdog resets.
- **Power Management**: Ensure the watchdog is correctly paused or re-configured if the device enters a deep sleep mode (e.g., `WDT_OPT_PAUSE_IN_SLEEP`).
