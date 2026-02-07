# Error Handling & Defensive Programming

Zephyr uses standard POSIX-like error codes. Correct error handling is vital for robust embedded systems.

## Error Code Return Pattern
Functions should return `0` on success and a negative `errno` code on failure.

```c
int my_function(void) {
    if (error_condition) {
        return -EINVAL;
    }
    return 0;
}
```

## Defensive Programming Patterns

### 1. Build-Time Assertions
Catch configuration errors early.
```c
BUILD_ASSERT(CONFIG_MY_BUFFER_SIZE > 128, "Buffer too small!");
```

### 2. Parameter Validation
Check inputs at the start of functions, especially in public APIs.
```c
if (!dev) return -EINVAL;
if (!data) return -EFAULT;
```

### 3. Return Code Checking
Always check the return value of kernel and driver APIs.
```c
int ret = gpio_pin_configure_dt(spec, GPIO_OUTPUT);
if (ret < 0) {
    LOG_ERR("Failed to configure GPIO (err %d)", ret);
    return ret;
}
```

### 4. Pointer Safety
Use `NULL` checks before dereferencing, or use `CONTAINER_OF` to reach parent contexts safely.

### 5. Initialization Safety
Ensure drivers are initialized at the correct level (`PRE_KERNEL_1`, `POST_KERNEL`, etc.) using `DEVICE_DT_INST_DEFINE` or similar macros.
