# Threads & Scheduling

Zephyr is a multi-threaded RTOS where even the simplest application typically involves multiple threads.

## Thread Types
- **Main Thread**: Runs the `main()` function. Automatically created with a default priority.
- **Idle Thread**: Runs when no other thread is ready.
- **System Threads**: Threads created by the kernel (e.g., logging, shell, networking).
- **User Threads**: Threads created by your application.

## Priority
- **Preemptive (0 to N)**: Can be interrupted by higher-priority threads.
- **Cooperative (-N to -1)**: Runs until it blocks or yields. Ideal for non-deterministic tasks.

## Thread Creation
### 1. Static Creation (Recommended)
```c
K_THREAD_DEFINE(my_thread_id, STACK_SIZE, my_thread_fn, NULL, NULL, NULL, PRIORITY, 0, 0);
```

### 2. Dynamic Creation
```c
k_tid_t tid = k_thread_create(&my_thread_data, my_stack_area, K_THREAD_STACK_SIZEOF(my_stack_area),
                              my_thread_fn, NULL, NULL, NULL, PRIORITY, 0, K_NO_WAIT);
```

## Common Operations
- `k_sleep(K_MSEC(100))`: Yield the CPU for a duration.
- `k_yield()`: Yield to threads of the same priority.
- `k_thread_priority_set(tid, new_prio)`: Change a thread's priority at runtime.

## Stack Sizing Guidelines
Choosing the right stack size prevents crashes and wastes less RAM.
- **Minimum**: 512 bytes (very simple threads with no function calls)
- **Typical**: 1024-2048 bytes (most application threads)
- **With Logging**: Add 512-1024 bytes for log buffer overhead
- **Best Practice**: Use `CONFIG_THREAD_ANALYZER=y` and `CONFIG_THREAD_STACK_INFO=y` to measure actual usage at runtime

