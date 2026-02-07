# Modbus TCP

Modbus TCP allows the standard Modbus protocol to run over Ethernet or Wi-Fi networks using standard TCP/IP sockets.

## Core Concepts
- **Port 502**: The standard assigned port for Modbus TCP.
- **Unit Identifier**: Replaces the Node Address in RTU (usually set to 0xFF or 0 for TCP).
- **MBAP Header**: A 7-byte header used instead of the RTU CRC for error detection (TCP handles its own error correction).

## Basic Configuration
To enable Modbus TCP in `prj.conf`:

```kconfig
CONFIG_MODBUS=y
CONFIG_MODBUS_ETHERNET=y
CONFIG_NETWORKING=y
CONFIG_NET_TCP=y
CONFIG_NET_IPV4=y
```

## Implementation (Client Example)
Reading registers from a remote server:

```c
#include <zephyr/modbus/modbus.h>

void read_remote_data(void) {
    const char *iface_name = "MODBUS_TCP_0";
    struct modbus_iface_param param = {
        .mode = MODBUS_MODE_RAW, // TCP uses raw mode in the subsystem
        .client = {
            .server_addr = "192.168.1.100",
            .port = 502,
        },
    };
    
    int iface = modbus_iface_get_by_name(iface_name);
    modbus_init_client(iface, param);
    
    uint16_t data[5];
    modbus_read_holding_regs(iface, 1, 0, data, 5);
}
```

## Professional Strategies
- **Concurrency**: Modbus TCP clients can handle multiple connections, but most embedded servers are limited to 1-4 concurrent clients.
- **Recovery**: Implement an auto-reconnect strategy if the TCP socket is closed by the server.
- **Security**: Modbus TCP is inherently insecure (no native encryption). If used over a public network, tunnel it through a VPN or use a gateway that provides TLS.
