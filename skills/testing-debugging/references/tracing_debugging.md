# Tracing & Debugging

Beyond simple logging, Zephyr provides advanced tools for analyzing system behavior, timing, and resource utilization.

## Tracing Subsystem
The tracing subsystem allows you to capture events (thread switches, ISRs, kernel object usage) with microsecond precision.

### 1. Enabling Tracing
```kconfig
CONFIG_TRACING=y
CONFIG_TRACING_CORE=y
CONFIG_TRACING_SYSCALL=y
```

### 2. Backends
- **Segger SystemView**: Real-time visual analysis of thread execution.
- **CTF (Common Trace Format)**: Standard format for offline analysis with tools like TraceCompass.
- **User Tracing**: Add custom trace points in your application code.

## Thread & Stack Analysis
Memory issues (stack overflows) are common in RTOS development.

### 1. Stack Sentinel
Detects stack overflows at runtime by checking a "magic" value at the end of the stack.
```kconfig
CONFIG_STACK_SENTINEL=y
```

### 2. Thread Analyzer
Periodically prints statistics about thread stack usage.
```kconfig
CONFIG_THREAD_ANALYZER=y
CONFIG_THREAD_ANALYZER_AUTO=y
```

## Debugging Workflow
1. **Shell Inspection**: Use the `devmem`, `kernel`, and `device` shell commands to inspect state at runtime.
2. **GDB Integration**: Use `west debug` with advanced probes (J-Link, ST-Link) for step-through debugging.
3. **Core Dumps**: Enable `CONFIG_KOBJECT_TEXT_AREA` to allow Zephyr to generate core dumps on fatal errors, which can be analyzed later in GDB.

## Professional Tip: Latency Analysis
Use the `TRACING_ISR_ENTER` and `TRACING_ISR_EXIT` hooks to measure interrupt latency. This is critical for high-performance motor control or time-sensitive wireless applications.
