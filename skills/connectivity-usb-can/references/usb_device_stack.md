# USB Device Stack

Zephyr includes a modular USB device stack that supports multiple device classes and can be configured via Kconfig and Devicetree.

## Core Concepts
- **USB Controller**: The hardware peripheral that communicates with the host.
- **Device Classes**: Standardized protocols for specific functions (e.g., CDC ACM for serial, HID for mouse/keyboard).
- **USB Descriptor**: Data structures that describe the device to the host.

## Basic Configuration
To enable the USB stack, add the following to your `prj.conf`:

```kconfig
CONFIG_USB_DEVICE_STACK=y
CONFIG_USB_DEVICE_PRODUCT="My Zephyr Device"
CONFIG_USB_DEVICE_VID=0x1234
CONFIG_USB_DEVICE_PID=0x5678
```

## Standard Classes

### 1. CDC ACM (Virtual Serial Port)
Commonly used for shell access or simple data transfer.
```kconfig
CONFIG_USB_CDC_ACM=y
CONFIG_SERIAL=y
CONFIG_UART_LINE_CTRL=y
```

### 2. HID (Human Interface Device)
Used for keyboards, mice, or custom data reports.
```kconfig
CONFIG_USB_DEVICE_HID=y
CONFIG_USB_HID_DEVICE_COUNT=1
```

### 3. Mass Storage Class (MSC)
Allows the device to act as a USB drive.
```kconfig
CONFIG_USB_DEVICE_NETWORK_MSC=y
```

## Enabling the Stack
The USB stack must be explicitly initialized and started in your code:

```c
#include <zephyr/usb/usb_device.h>

void main(void) {
    int ret = usb_enable(NULL);
    if (ret != 0) {
        // Handle error
    }
}
```

## Best Practices
- **VID/PID**: Always use a unique Vendor ID and Product ID. For development, use the testing IDs allocated by the USB-IF.
- **Power Delivery**: If using USB-C, ensure `CONFIG_USBC_STACK` is configured to handle PD negotiations.
- **Composite Devices**: Zephyr supports multiple classes on a single USB device (e.g., CDC ACM + HID). Use `USB_DEVICE_BCC_DEFINE` for advanced configurations.
