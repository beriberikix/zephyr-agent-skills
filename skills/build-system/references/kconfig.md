# Kconfig Configuration

Kconfig is used to configure software features and drivers at compile-time.

## configuration Files
- `prj.conf`: Primary application configuration.
- `boards/<board>.conf`: Board-specific configuration.
- `<board>_<revision>.conf`: Revision-specific configuration.
- `socs/<soc>_<variant>.conf`: (HWMv2) SoC-level common configuration.

## Essential Commands
- `west build -t menuconfig`: Launch the interactive configuration editor.
  - `/`: Search for symbols.
  - `?`: View help and dependencies for a symbol.
- `west build -t guiconfig`: Launch the GUI configuration editor.

## Symbol Types
- `bool`: `y` or `n`.
- `int`: Decimal or hex integer.
- `string`: `"text string"`.
- `choice`: Select one of multiple options.

## Patterns & Best Practices
- **Never** use `CONFIG_` prefix in `.conf` files; it is added by the build system.
- Use `select` in Kconfig files to enforce dependencies.
- Use `depends on` to hide options that are not applicable.
- **HWMv2 Strategy**: Move networking and common peripheral settings to `socs/` configs to avoid duplication across board variants.
