# Work Queues & Settings

Efficient background processing and persistent configuration storage are essential for robust IoT applications.

## Work Queues
Work queues (System and Custom) allow you to defer work from an ISR or high-priority thread to a lower-priority context.

### 1. System Work Queue
Convenient for simple, non-blocking tasks.
```c
struct k_work my_work;

void work_handler(struct k_work *work) {
    // Background task
}

void trigger_work(void) {
    k_work_init(&my_work, work_handler);
    k_work_submit(&my_work);
}
```

### 2. Custom Work Queues (Professional Pattern)
Prevent your tasks from being delayed by other system work. Essential for sensor sampling or slow I/O.
```kconfig
CONFIG_SYSTEM_WORKQUEUE_STACK_SIZE=2048
```
```c
struct k_work_q my_q;
K_THREAD_STACK_DEFINE(my_q_stack, 1024);

void setup_q(void) {
    k_work_queue_start(&my_q, my_q_stack, K_THREAD_STACK_SIZEOF(my_q_stack),
                       PRIORITY, NULL);
}
```

## Settings Subsystem
Store and retrieve persistent data across reboots.

### 1. Enabling Settings
```kconfig
CONFIG_SETTINGS=y
CONFIG_SETTINGS_NVS=y # Use Non-Volatile Storage backend
```

### 2. Registering a Handler
```c
#include <zephyr/settings/settings.h>

static int my_set(const char *name, size_t len, settings_read_cb read_cb, void *cb_arg) {
    // Load logic
    return 0;
}

SETTINGS_STATIC_HANDLER_DEFINE(my_mod, "app/config", NULL, my_set, NULL, NULL);

void init_settings(void) {
    settings_subsys_init();
    settings_load();
}
```

### 3. Saving Values
```c
settings_save_one("app/config/value", &data, sizeof(data));
```

## Pro Tip: Deferred Action
Use `k_work_delayable` to trigger an action after a timeout, perfect for debouncing or periodic polling.
