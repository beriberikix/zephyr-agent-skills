# Power Management (PM)

Zephyr provides a comprehensive power management subsystem to reduce power consumption through system states and peripheral management.

## System Power States
States are defined in Devicetree and managed by the PM subsystem.
- **Active**: Normal operation.
- **Idle**: CPU stops executing instructions, but remains powered.
- **Suspend / Deep Sleep**: Core and some peripherals are powered down. RAM is typically retained.
- **Off**: Complete power down. Requires a wake-up source or reset.

## Residency & States
Define states in your board's Devicetree.
```dts
/ {
    cpus {
        cpu0: cpu@0 {
            cpu-power-states = <&state0 &state1>;
        };
    };

    power-states {
        state0: state0 {
            compatible = "zephyr,power-state";
            power-state-name = "suspend-to-idle";
            min-residency-us = <1000>;
        };
    };
};
```

## Device Power Management
Peripherals can be transitioned to low-power states independently.
```c
#include <zephyr/pm/device.h>

const struct device *dev = DEVICE_DT_GET(DT_NODELABEL(uart0));

void enter_low_power(void) {
    pm_device_action_run(dev, PM_DEVICE_ACTION_SUSPEND);
}
```

## PM Hooks (Application Level)
Use the `pm_state_set` hook to perform custom actions (like turning off external chips) when the system enters a power state.

```c
#include <zephyr/pm/pm.h>

void pm_state_set(struct pm_state_info info) {
    if (info.state == PM_STATE_SOFT_OFF) {
        // Prepare hardware for off
    }
}
```

## Professional Patterns
- **Trigger via Zbus**: Notify all modules to prepare for sleep via a shared Zbus channel.
- **Hardware-Informed Sleep**: Use `GPIO_INT_EDGE_BOTH` to wake up the SoC on external events.
- **Measure Actual Current**: Always validate your PM logic with a power analyzer (e.g., Power Profiler Kit).
