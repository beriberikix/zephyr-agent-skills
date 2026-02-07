# Fault Injection & Resilience

Resilience testing involves intentionally introducing faults to verify that the system handles them gracefully and recovers according to the design.

## Core Concepts
- **Fault Injection**: Forcing error conditions (e.g., network timeout, corrupt packet, CPU exception).
- **Chaos Engineering**: Randomly disabling components to test system stability.
- **Panic Handling**: Customizing how the kernel reacts to fatal errors.

## Implementation Patterns

### 1. Software-Triggered Oops
Use `k_oops()` or `k_panic()` to simulate a fatal software error.

```c
void test_fault_recovery(void) {
    printk("Simulating fatal error...\n");
    k_oops(); // Normal recovery logic should kick in
}
```

### 2. Network Faults
If using the IP stack, simulate packet loss or latency using the **Traffic Control (TC)** subsystem or external tools in `native_sim`.

### 3. Corruption Testing
Intentionally corrupting data in **NVS** or **Settings** backends to verify that the application detects the corruption and re-initializes to a safe default.

## Best Practices
- **Production Stripping**: Ensure that fault injection code is excluded from production builds using Kconfig (e.g., `ifdef CONFIG_TEST_FAULTS`).
- **Telemetry**: Report the cause of the previous reset (e.g., `NRF_POWER->RESETREAS` on Nordic) to the cloud so you can track field failures.
- **Simulators**: Use `native_sim` to perform automated chaos testing that would be difficult or destructive on real hardware.
