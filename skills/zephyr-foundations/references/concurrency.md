# Real-Time Concurrency

Zephyr provides a rich set of primitives for thread synchronization and interrupt safety.

## Mutexes (`k_mutex`)
- **Use**: Blocking synchronization between threads.
- **Rules**: Cannot be used in ISRs. Supports priority inheritance.
- **API**: `k_mutex_init`, `k_mutex_lock`, `k_mutex_unlock`.

## Semaphores (`k_sem`)
- **Use**: Signaling and resource counting.
- **Rules**: Can be given from ISRs, but not taken with wait.
- **API**: `k_sem_init`, `k_sem_give`, `k_sem_take`.

## Spinlocks (`k_spinlock`)
- **Use**: Ultra-fast, non-blocking protection.
- **Rules**: Held for as short a time as possible. Disables interrupts locally.
- **API**: `K_SPINLOCK_DEFINE`, `k_spin_lock`, `k_spin_unlock`.

## Atomic Operations (`atomic_t`)
- **Use**: Lock-free manipulation of 32-bit values.
- **Rules**: Safe for ISR-to-thread communication.
- **API**: `atomic_set`, `atomic_add`, `atomic_cas` (Compare-And-Swap).
- **Note**: Atomics provide atomicity but NOT memory ordering guarantees. Use memory barriers if ordering is critical.

## ISR Safety
- **CRITICAL**: Never call an API that might sleep or block from an ISR (Interrupt Service Routine).
- Use `k_is_in_isr()` to check context if a function is shared.
- Use Semaphores or Work Queues to "defer" heavy processing from an ISR to a thread.

## Polling (`k_poll`)
- **Use**: Wait for multiple events (semaphores, FIFOs, etc.) simultaneously.
