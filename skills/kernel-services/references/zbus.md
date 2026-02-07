# Zephyr Bus (Zbus)

`zbus` is a lightweight many-to-many publish-and-subscribe bus that enables modular, event-driven communication between different threads in a Zephyr application.

## Core Concepts
- **Channels**: The data carriers. Defined at compile-time with a specific data type.
- **Publishers**: Components that send data to a channel.
- **Subscribers**: Components that receive data from a channel via a message queue or a callback (listener).

## Defining a Channel
Channels are typically defined in a common header or a dedicated communication source file.

```c
#include <zephyr/zbus/zbus.h>

struct battery_msg {
    uint8_t percentage;
    bool charging;
};

ZBUS_CHAN_DEFINE(batt_chan, struct battery_msg, NULL, NULL, ZBUS_OBSERVERS_EMPTY, ZBUS_CHAN_DEFAULTS);
```

## Publishing Data
```c
struct battery_msg msg = { .percentage = 85, .charging = false };
zbus_chan_pub(&batt_chan, &msg, K_MSEC(100));
```

## Subscribing to Data
### 1. Message Queue Subscriber
Ideal for threads that need to wait for events.
```c
ZBUS_SUBSCRIBER_DEFINE(my_sub, 4); // Queue size of 4

void listener_thread(void) {
    const struct zbus_channel *chan;
    while (!zbus_sub_wait(&my_sub, &chan, K_FOREVER)) {
        if (chan == &batt_chan) {
            struct battery_msg msg;
            zbus_chan_read(chan, &msg, K_MSEC(10));
            // Handle message
        }
    }
}
```

### 2. Real-time Listeners (Callbacks)
Called directly from the publisher's context. Highly efficient but must not block.
```c
void batt_callback(const struct zbus_channel *chan) {
    // Immediate action
}
ZBUS_LISTENER_DEFINE(my_listener, batt_callback);
```

## Best Practices
- **Decouple Modules**: Modules should only depend on shared channel definitions, not on each other's internals.
- **Use for Event-Driven Logic**: Perfect for sensor updates, state changes, or UI notifications.
- **Avoid Over-Broadcasting**: Only define observers that actually need the data to minimize overhead.
