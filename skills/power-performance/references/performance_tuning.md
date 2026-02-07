# Performance Tuning & Relocation

Optimize your Zephyr application for speed and memory efficiency.

## Code & Data Relocation
Place critical functions in faster memory (like ITCM or RAM) instead of Flash to eliminate wait-states.

### 1. Relocating a Single Function
```c
void __attribute__((section(".ramfunc"))) critical_fn(void) {
    // Fast execution
}
```
**Note**: The `.ramfunc` section must be defined in your linker script. Some boards use `__ramfunc` as a pre-defined macro. Check your board's linker script in `boards/<arch>/<vendor>/<board>/`.

### 2. Using the Relocation Script
Define relocation rules in a `relocation.conf` file.
```
# Place everything from this file into RAM
my_critical_math.c:SRAM
```

## Stack Analysis
Avoid overflows and reclaim wasted memory.
```kconfig
CONFIG_THREAD_STACK_INFO=y
CONFIG_THREAD_ANALYZER=y
CONFIG_THREAD_ANALYZER_AUTO=y
```
Inspect logs to see peak stack usage for every thread.

## Timing & Latency
- **Direct ISRs**: Use for lowest-latency interrupt handling (bypasses Zephyr OS overhead).
- **Execution Profiling**: Use `CONFIG_TRACING=y` or vendor-specific trace features (like ITM) to measure function durations.

## Compiler Optimizations
Tune the build for your specific goals.
- `CONFIG_SPEED_OPTIMIZATIONS=y`: `-O2`
- `CONFIG_SIZE_OPTIMIZATIONS=y`: `-Os`
- `CONFIG_NO_OPTIMIZATIONS=y`: `-O0` (Debugging only)

## Professional Tip: Linker Map
Always inspect the `zephyr.map` file in your build directory to understand exactly how your memory is being used and what functions are taking up the most space.
