# Sysbuild & CMake Integration

## Sysbuild (Multi-image Builds)
Sysbuild allows building multiple images (e.g., MCUboot + Application) with a single command.

### Using Sysbuild
- `west build --sysbuild`: Enable sysbuild for the current build.
- `SB_CONFIG_BOOTLOADER_MCUBOOT=y`: Enable MCUboot integration in `sysbuild.conf`.

### Configuration
- `sysbuild.conf`: Global sysbuild configuration.
- `boards/`: Board-specific sysbuild configuration inside the application directory.

---

## CMake Integration
Zephyr uses CMake as its primary build system.

### Application `CMakeLists.txt`
```cmake
cmake_minimum_required(VERSION 3.20.0)
find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
project(my_app)

target_sources(app PRIVATE src/main.c)
```

### Key Variables
- `ZEPHYR_BASE`: Path to the Zephyr repository.
- `BOARD`: The target board name.
- `CONF_FILE`: Path to the configuration file (defaults to `prj.conf`).

### Adding External Libraries
Use `zephyr_library()` and `zephyr_library_sources()` within a module or application to integrate custom code into the Zephyr build graph.
