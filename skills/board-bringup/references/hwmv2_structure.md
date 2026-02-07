# HWMv2 Directory Structure

Zephyr 3.7+ uses Hardware Model v2 (HWMv2). Boards are organized in a structured tree.

## Directory Layout
```
boards/
└── <vendor>/
    └── <board_name>/
        ├── board.yml          # Core metadata (revisions, SoC, variants)
        ├── Kconfig.board      # Kconfig definition
        ├── <board_name>_defconfig
        ├── CMakeLists.txt     # Board-specific build logic
        ├── <board_name>.dts   # Base devicetree
        └── <board_name>_common.dtsi # Shared DT for revisions
```

## `board.yml` Specification
This file defines the board's identity and its variants.

```yaml
board:
  name: my_custom_board
  vendor: my_company
  revision:
    format: letter
    default: A
    exact: true
    revisions:
      - name: A
      - name: B
  socs:
    - name: nrf52840
  variants:
    - name: ns
```

## Board Naming Scheme
Final board names are constructed as: `<board_name>/<soc>[/<variant>]`
Example: `my_custom_board/nrf52840/ns`
