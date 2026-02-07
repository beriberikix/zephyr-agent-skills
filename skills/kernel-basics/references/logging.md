# Logging Subsystem

Zephyr provides a unified logging API with multiple levels and backends (UART, Shell, RTT).

## Log Levels
1. `LOG_ERR`: Essential errors. Red on supporting terminals.
2. `LOG_WRN`: Warnings about potential issues. Yellow.
3. `LOG_INF`: General informational messages (e.g., "System started").
4. `LOG_DBG`: Detailed debug info. Hidden by default in production.

## Registering a Module
Always register your module at the top of your `.c` file.
```c
#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(my_app, CONFIG_APP_LOG_LEVEL);
```

## Logging Macros
```c
LOG_INF("Temperature: %d C", temp);
LOG_HEXDUMP_DBG(buffer, len, "Buffer Content");
```

## Useful Kconfig Symbols
- `CONFIG_LOG=y`: Enable the logging subsystem.
- `CONFIG_LOG_MODE_IMMEDIATE=y`: Process logs as they happen (good for debugging crashes, bad for performance).
- `CONFIG_LOG_MODE_DEFERRED=y`: (Default) Process logs in a background thread.
- `CONFIG_LOG_BACKEND_UART=y`: Send logs to the system UART.
