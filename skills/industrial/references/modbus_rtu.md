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

## Validation Workflow

Use this quick sequence before system integration:

1. **Static map validation**
     - Keep register allocations in a CSV and run:
     - `python ../scripts/modbus_register_lint.py --csv ../assets/modbus_register_map_template.csv`
2. **Frame-level sanity check**
     - Verify slave node address, baud, parity, and stop bits are exactly matched on both ends.
     - Confirm function-code behavior for at least one read and one write path.
3. **Timing check**
     - Confirm inter-frame silent interval is not violated under peak polling load.
4. **Error-path check**
     - Validate exception responses for invalid register addresses and unsupported function codes.

## Troubleshooting Patterns

- **No response at all**:
    - Check RS-485 transceiver DE/RE direction control and wiring polarity (A/B lines).
    - Confirm node address and UART parity settings.
- **Intermittent CRC/framing errors**:
    - Lower baud rate and inspect grounding/isolation.
    - Verify cable length and termination/biasing for the bus segment.
- **Wrong data from valid frames**:
    - Review register addressing convention (`0-based` vs `40001` style in tooling).
    - Confirm endianness/word-order assumptions for multi-register values.
- **System stalls during polling**:
    - Move Modbus processing to work queue/thread context and avoid long blocking handlers.
    - Add watchdog-aware timeout and retry limits for external bus faults.
