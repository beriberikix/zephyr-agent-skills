# Zephyr Module Definition

A Zephyr module is an external repository that integrates into the Zephyr build system. It is defined by the existence of a `zephyr/module.yml` file.

## Module Structure
```
my-module/
├── zephyr/
│   ├── module.yml        # Integration metadata
│   ├── Kconfig           # Module-specific configuration
│   └── CMakeLists.txt    # Module-specific build logic
├── include/
│   └── my_module.h       # Public headers
├── src/
│   └── my_module.c       # Source code
└── CMakeLists.txt         # Entry point for CMake
```

## `zephyr/module.yml`
This file tells Zephyr how to interact with the module.
```yaml
build:
  cmake: .                 # Path to the module's CMakeLists.txt
  kconfig: zephyr/Kconfig  # Path to the module's Kconfig
```

## The "Glue" Pattern
If you are wrapping an existing 3rd-party library, keep the original source clean and put all Zephyr-specific files in the `zephyr/` directory. Use the `zephyr/CMakeLists.txt` to add the library to the Zephyr build.
