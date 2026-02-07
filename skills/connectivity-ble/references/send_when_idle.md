# Send-When-Idle Pattern

The "Send-When-Idle" pattern is a professional design strategy for low-power BLE devices to optimize battery life by bundling data and transmitting only when the core application logic is idle.

## Why Use It?
- **Reduces Radio On-Time**: Aggregating updates into a single transmission is more efficient than frequent small bursts.
- **Prevents Contention**: Ensures the radio doesn't stall time-critical local processing.
- **Increases Latency Tolerance**: Ideal for non-real-time telemetry (e.g., environmental monitoring).

## Implementation with Workqueues

### 1. The Accumulator
Use a buffer or a Zbus channel to hold data until ready to send.

### 2. The Idle Timer
Use a `k_work_delayable` to trigger transmission after a period of inactivity.

```c
#include <zephyr/kernel.h>

static struct k_work_delayable send_idle_work;
#define IDLE_TIMEOUT_MS 5000

void on_data_generated(void) {
    // 1. Add data to local buffer
    // 2. Reschedule the idle timer
    k_work_reschedule(&send_idle_work, K_MSEC(IDLE_TIMEOUT_MS));
}

void send_idle_handler(struct k_work *work) {
    // This runs only after 5 seconds of no data being generated
    transmit_bundled_data();
}

void init_pattern(void) {
    k_work_init_delayable(&send_idle_work, send_idle_handler);
}
```

## Professional Pattern: Golioth Pouch Style
- **Combine with SMF**: Use the State Machine Framework to manage the lifecycle (Collecting -> Sending -> Sleeping).
- **Zbus Backbone**: Use Zbus to decouple data producers from the "Send-When-Idle" transmitter module.
- **Power Hooks**: Tie the idle state to system power management states to allow the SoC to enter deep sleep while waiting.

## Benefits for LTE/NB-IoT
While described here for BLE, this pattern is even more critical for cellular connectivity (LTE-M/NB-IoT) where modem wake-up cost is extremely high.
