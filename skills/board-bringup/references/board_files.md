# Core Board Files

Each custom board requires a set of configuration files to be recognized by West.

## `Kconfig.board`
Defines the board symbol.
```kconfig
config BOARD_MY_BOARD
    bool "My Custom Board"
    depends on SOC_NRF52840_QIAA
```

## `defconfig`
Sets the default Kconfig values for the board.
```kconfig
CONFIG_SOC_SERIES_NRF52X=y
CONFIG_SOC_NRF52840_QIAA=y
CONFIG_BOARD_MY_BOARD=y
CONFIG_CONSOLE=y
CONFIG_UART_CONSOLE=y
CONFIG_SERIAL=y
CONFIG_GPIO=y
```

## `CMakeLists.txt`
Minimal build logic.
```cmake
zephyr_library()
zephyr_library_sources(board.c) # If you have board-specific C code
```

## Managing Revisions
HWMv2 handles revisions natively. You can create `<board_name>_revA.conf` or `<board_name>_revA.overlay` to handle differences between hardware versions.
Check `board.yml` for the revision format.
