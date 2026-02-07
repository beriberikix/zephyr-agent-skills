# Modbus RTU (Serial)

Modbus RTU is a serial communication protocol widely used in industrial automation. Zephyr provides a high-level Modbus subsystem that abstracts the serial/UART details.

## Core Concepts
- **RTU (Remote Terminal Unit)**: Binary representation over serial.
- **Master/Client**: The device that initiates requests.
- **Slave/Server**: The device that responds to requests.
- **Registers**: Coils (BOOL), Discrete Inputs (BOOL), Holding Registers (INT16), Input Registers (INT16).

## Basic Configuration
To enable Modbus RTU in `prj.conf`:

```kconfig
CONFIG_MODBUS=y
CONFIG_MODBUS_SERIAL=y
CONFIG_SERIAL=y
CONFIG_UART_ASYNC_API=y # Recommended for better performance
```

## Implementation Patterns

### 1. Modbus Server (Slave)
The device exposes its registers to a master.

```c
#include <zephyr/modbus/modbus.h>

static int holding_reg[10];

static int my_reg_rd(uint16_t addr, uint16_t *reg) {
    if (addr < 10) {
        *reg = holding_reg[addr];
        return 0;
    }
    return -ENOTSUP;
}

static struct modbus_user_callbacks user_cbs = {
    .reg_rd = my_reg_rd,
};

void init_modbus_server(void) {
    const struct device *dev = DEVICE_DT_GET(DT_CHOSEN(zephyr_modbus_serial));
    struct modbus_iface_param param = {
        .mode = MODBUS_MODE_RTU,
        .server = {
            .node_addr = 1,
            .cb = &user_cbs,
        },
        .serial = {
            .baud = 115200,
            .parity = UART_CFG_PARITY_NONE,
        },
    };
    
    modbus_init_server(dev, param);
}
```

## Professional Strategies
- **Physical Layer**: Most industrial Modbus uses RS-485. Ensure your board has an RS-485 transceiver and you handle the DE/RE signals (often via the `uart-rs485` devicetree property).
- **Timeouts**: Modbus RTU relies on 3.5-character time silences to delimit frames. Use a stable clock source for the UART peripheral.
- **Isolation**: Industrial environments often require galvanic isolation for the serial lines to prevent ground loops.
