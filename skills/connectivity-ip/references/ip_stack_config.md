# IP Stack Configuration

Zephyr's IP stack is highly modular. For resource-constrained devices, you must explicitly disable what you don't use to save Flash and RAM.

## Trimming the Stack
A full IPv6 stack can be large. Use these Kconfig strategies to optimize.

### 1. Version Selection
Disable IPv6 if your network only supports IPv4 (or vice versa).
```kconfig
CONFIG_NET_IPV6=n
CONFIG_NET_IPV4=y
```

### 2. Disabling Unused Protocols
```kconfig
CONFIG_NET_UDP=y
CONFIG_NET_TCP=n  # Save significant RAM if using only CoAP/LwM2M
CONFIG_NET_ICMP=n
```

### 3. Buffer Sizing (Critical)
The number and size of network buffers determine how much data the stack can handle simultaneously.
```kconfig
CONFIG_NET_PKT_RX_COUNT=4
CONFIG_NET_PKT_TX_COUNT=4
CONFIG_NET_BUF_RX_COUNT=16
CONFIG_NET_BUF_TX_COUNT=16
```

## Advanced Features
- **IP Autoconfiguration**: Enable DHCPv4 or IPv6 SLAAC.
- **DNS**: Essential for cloud connectivity.
```kconfig
CONFIG_DNS_RESOLVER=y
CONFIG_DNS_SERVER_IP_ADDRESSES=y
CONFIG_DNS_SERVER1="8.8.8.8"
```

## Logging & Debugging
The network stack provides granular logging to help identify why packets are being dropped.
```kconfig
CONFIG_NET_LOG=y
CONFIG_NET_IPV4_LOG_LEVEL_DBG=y
```

## Professional Tip
Use `west build -t ram_report` to see how much memory the networking buffers and thread stacks are consuming. Networking is often the largest consumer of RAM in an IoT application.
