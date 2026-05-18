# Sysbuild & CMake Integration

## Sysbuild (Multi-image Builds)
Sysbuild allows building multiple images (e.g., MCUboot + Application) with a single command.

### Using Sysbuild
- `west build --sysbuild`: Enable sysbuild for the current build.
- `SB_CONFIG_BOOTLOADER_MCUBOOT=y`: Enable MCUboot integration in `sysbuild.conf`.

### Configuration
- `sysbuild.conf`: Global sysbuild configuration.
- `boards/`: Board-specific sysbuild configuration inside the application directory.

### Flash Partition Layout (MCUboot prerequisite)
Setting `SB_CONFIG_BOOTLOADER_MCUBOOT=y` is not sufficient on its own. MCUboot also
requires the application's Devicetree to define a `fixed-partitions` flash layout — a
bootloader slot plus two equal-size image slots — and to choose the code partition:

```dts
&flash0 {
    partitions {
        compatible = "fixed-partitions";
        #address-cells = <1>;
        #size-cells = <1>;

        boot_partition:  partition@0     { reg = <0x00000 0x0c000>; };
        slot0_partition: partition@c000  { reg = <0x0c000 0x37000>; };
        slot1_partition: partition@43000 { reg = <0x43000 0x37000>; };
    };
};

/ { chosen { zephyr,code-partition = &slot0_partition; }; };
```

`slot0_partition` (running image) and `slot1_partition` (update image) must be the same
size. Most upstream boards already define this layout; custom boards do not. A build that
fails with a missing `slot0_partition` or `boot_partition` almost always means this layout
is absent — add it in the board `.dts` or an overlay. The security-updates skill covers
image signing, DFU, and rollback in depth.

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
