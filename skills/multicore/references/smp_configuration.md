# SMP Configuration

Zephyr supports **Symmetric Multiprocessing (SMP)**, allowing multiple physical CPU cores to run the same Zephyr image and its threads concurrently.

## Core Concepts
- **Symmetric Architecture**: All CPUs have access to the same memory and peripherals.
- **Spinlocks**: The primary synchronization primitive for SMP. Unlike semaphores, spinlocks busy-wait and are safe for use in ISRs.
- **Thread Affinity**: The ability to pin a specific thread to a specific CPU core.

## Basic Configuration
To enable SMP for a multi-core SoC (e.g., ESP32, STM32H7), add to `prj.conf`:

```kconfig
CONFIG_SMP=y
CONFIG_MP_NUM_CPUS=2  # Specify the number of cores
```

## Synchronization with Spinlocks
In an SMP environment, `irq_lock()` only prevents interrupts on the local core. To protect shared data across cores, use `k_spinlock`.

```c
#include <zephyr/sys/spinlock.h>

static struct k_spinlock my_lock;
static uint32_t shared_data;

void update_shared_data(uint32_t val) {
    k_spinlock_key_t key = k_spin_lock(&my_lock);
    
    shared_data = val; // Critical section
    
    k_spin_unlock(&my_lock, key);
}
```

## Thread Affinity
By default, the Zephyr scheduler moves threads between cores. Pin a thread if it handles core-specific interrupts or real-time tasks.

```c
#include <zephyr/kernel.h>

void pin_my_thread(k_tid_t tid) {
    // Pin thread to CPU 1 only
    k_thread_cpu_pin(tid, 1);
}
```

## Best Practices
- **Minimize Spinlock Hold Time**: Spinlocks block other CPUs from progressing. Keep critical sections as short as possible.
- **Cache Coherency**: Be aware of cache coherency issues if the hardware does not provide automatic cache management between cores.
- **IRQs**: Remember that an ISR on Core A can still be interrupted by an ISR on Core B if they have different priorities.
