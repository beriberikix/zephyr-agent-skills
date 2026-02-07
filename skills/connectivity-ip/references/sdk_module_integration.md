# SDK & Module Integration

IoT applications often rely on external libraries and cloud SDKs (e.g., Golioth, Memfault, AWS IoT). These should be integrated as Zephyr modules.

## West Manifest (`west.yml`)
The manifest defines all repositories required by your project.

### 1. Adding a Remote Module
```yaml
manifest:
  remotes:
    - name: golioth
      url-base: https://github.com/golioth
  projects:
    - name: golioth-firmware-sdk
      remote: golioth
      revision: main
      path: modules/lib/golioth-sdk
```

### 2. Using an Allow-List
Large projects (like the nRF Connect SDK) include many modules. Use an `allow-list` to only fetch what you need.
```yaml
manifest:
  projects:
    - name: nrf
      url: https://github.com/nrfconnect/sdk-nrf
      revision: v2.5.0
      import:
        name-allowlist:
          - zephyr
          - cmsis
          - nrfxlib
```

## Integrating into CMake
Once added via West, Zephyr automatically detects the module if it contains a `zephyr/module.yml` file.

If it is a "non-Zephyr" library, you can manually add it to your `CMakeLists.txt`:
```cmake
list(APPEND ZEPHYR_EXTRA_MODULES ${CMAKE_CURRENT_SOURCE_DIR}/external/my_lib)
```

## Pro Tip: Module Isolation
Try to keep module-specific configuration in its own Kconfig/Devicetree files and include them from your main project to keep the root clean.

## Common Issue: Revison Mismatch
Always pin your modules to specific tags or SHAs in production manifests to ensure reproducible builds.
