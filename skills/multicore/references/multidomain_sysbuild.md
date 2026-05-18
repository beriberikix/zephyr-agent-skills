# Multi-domain Sysbuild (nRF5340 and other multi-core SoCs)

Some SoCs run more than one independent firmware image — most notably the nRF5340, which
pairs an **application core** (`cpuapp`) with a **network core** (`cpunet`). Sysbuild builds
every image ("domain") in a single `west build` invocation and flashes them together.

## Building both cores at once

Point `west build` at the application core; Sysbuild discovers and adds the other domains:

```bash
west build --sysbuild -b nrf5340dk/nrf5340/cpuapp my_app
```

The build tree gets one subdirectory per domain plus a `domains.yaml` manifest:

```
build/
├── my_app/        # application-core image
├── net_core_fw/   # network-core image
└── domains.yaml   # lists every domain for west flash
```

## Adding a custom network-core image

For Nordic's stock network-core firmware, Sysbuild selects it with `SB_CONFIG_NETCORE_*`
options in `sysbuild.conf` (for example `SB_CONFIG_NETCORE_HCI_IPC` for the Bluetooth
controller, or `SB_CONFIG_NETCORE_EMPTY`). To build *your own* network-core firmware,
register it as an extra image from the application's `sysbuild.cmake`:

```cmake
ExternalZephyrProject_Add(
  APPLICATION net_core_fw
  SOURCE_DIR  ${APP_DIR}/net_core_fw
  BOARD       nrf5340dk/nrf5340/cpunet
)
```

`net_core_fw/` is an ordinary standalone Zephyr application; it is simply built for the
`cpunet` board target.

## Releasing the network core

The network core is held in reset until the application core starts it. Set this in the
**application-core** `prj.conf`:

```kconfig
CONFIG_NRF53_BOOT_NETWORK_CORE_ON_STARTUP=y
```

Without it the netcore image is flashed but never runs.

## Flashing

`west flash` reads `domains.yaml` and programs every core in order:

```bash
west flash                      # both cores
west flash --domain net_core_fw # one core only
west flash --recover            # erase + flash a fresh, AP-protected part
```

## Notes

- `SB_CONFIG_NETCORE_*` symbols come from the nRF Connect SDK Sysbuild integration; on
  plain upstream Zephyr there is no auto-added netcore image, so just register yours with
  `ExternalZephyrProject_Add`.
- Per-image Kconfig fragments are passed with an image-name prefix, e.g.
  `-Dnet_core_fw_EXTRA_CONF_FILE=debug.conf`.
- This is distinct from SMP (one kernel across identical cores) and from OpenAMP/RPMsg
  (the runtime message transport between the running images).
