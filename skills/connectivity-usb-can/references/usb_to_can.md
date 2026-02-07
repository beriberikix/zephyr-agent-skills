# USB-to-CAN Integration Patterns

Integrating USB and CAN allows for creating diagnostic tools, gateways, and adapters. These patterns are inspired by the "CANnectivity" project.

## Hardware Requirements
- A microcontroller with both a **USB Device Controller** and a **CAN Controller**.
- Appropriate pinctrl and devicetree configuration for both peripherals.

## Architecture
The most common pattern is to bridge a **CDC ACM (Serial)** interface to the **CAN Controller**.

### 1. Packetization (gs_usb Protocol)
Most professional USB-to-CAN adapters use the `gs_usb` protocol, which defines a binary packet structure for CAN frames over USB.

### 2. Buffering & Throughput
CAN can generate high-frequency traffic. Use Thread-safe buffers (like `k_msgq` or `k_fifo`) to bridge data between the USB and CAN threads.

```c
#include <zephyr/drivers/can.h>
#include <zephyr/usb/usb_device.h>

K_MSGQ_DEFINE(can_rx_msgq, sizeof(struct can_frame), 10, 4);

void usb_to_can_thread(void) {
    struct can_frame frame;
    while (1) {
        // 1. Read from USB CDC ACM
        // 2. Parse into can_frame
        // 3. Send to CAN bus
        can_send(can_dev, &frame, K_MSEC(100), NULL, NULL);
    }
}
```

## Kconfig Configuration
```kconfig
CONFIG_USB_DEVICE_STACK=y
CONFIG_USB_CDC_ACM=y
CONFIG_CAN=y
CONFIG_CAN_MAX_FILTER=5
```

## Integration Patterns
- **Zbus Integration**: Use Zbus to distribute CAN messages to multiple internal application modules (e.g., telemetry, local logging, and the USB bridge).
- **Filtering**: Use hardware CAN filters to only pass relevant messages to the USB interface, reducing CPU load.
- **Status LEDs**: Mirror CAN bus activity or errors to LEDs using the GPIO API to provide immediate visual feedback.

## Professional Insight: CANnectivity
The "CANnectivity" project demonstrates how to implement a portable, open-source USB-to-CAN adapter. Key takeaways:
- **Zero-Copy**: Utilize internal buffers effectively to minimize memory copy operations.
- **Multi-Instance**: Support multiple CAN controllers if the hardware provides them.
