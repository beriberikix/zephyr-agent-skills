# Native Simulation (native_sim)

`native_sim` is a Zephyr board that compiles and runs as a native executable on your host OS (Linux, macOS, or Windows via WSL).

## Why use native_sim?
- **Speed**: Build and cycles are much faster than hardware or full system emulators like QEMU.
- **Tooling**: Use standard host debuggers (GDB), memory checkers (Valgrind), and profilers (gprof).
- **Automation**: Perfect for CI/CD and unit testing (Ztest).
- **No Hardware Needed**: Develop application logic before boards are ready.

## Building and Running
```bash
west build -b native_sim samples/hello_world
./build/zephyr/zephyr.exe
```

## Configuration
- `CONFIG_NATIVE_APPLICATION=y`: Main switch for native targets.
- `CONFIG_NATIVE_UART_0_ON_STDINOUT=y`: Maps the first UART to the host's terminal.

## Key Differences from Hardware
- **Timer Frequency**: native_sim tries to match host time or can be accelerated.
- **Interrupts**: Simulated via host signals; not as deterministic as hardware.
- **Peripherals**: Limited to simulated ones (GPIO, I2C emulator, etc.) or host-bridged ones.
