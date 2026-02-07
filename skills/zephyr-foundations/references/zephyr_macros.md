# Zephyr Essential Macros & C Patterns

Zephyr heavily utilizes preprocessor macros for hardware abstraction, safety, and conciseness.

## Bit Manipulation
- `BIT(n)`: Returns a value with the `n`-th bit set.
- `BIT_MASK(n)`: Returns a bit mask of `n` bits (e.g., `BIT_MASK(3)` is `0x7`).
- `GENMASK(high, low)`: Returns a bit mask with bits from `low` to `high` set.
- `sys_get_bit(addr, bit)`: Safely check a bit at a memory address.
- `sys_set_bit(addr, bit)`: Safely set a bit at a memory address.

## Container & Pointer Logic
- `CONTAINER_OF(ptr, type, field)`: Returns a pointer to the parent structure of a field. Crucial for driver callbacks.
- `ARRAY_SIZE(array)`: Returns the number of elements in a static array.

## Compile-Time Checks
- `BUILD_ASSERT(cond, msg)`: Fails the build if `cond` is false.
- `__ASSERT(cond, msg)`: Runtime assertion (enabled via `CONFIG_ASSERT`).

## Error Codes
Always include `<zephyr/posix/errno.h>` for standard error codes:
- `-EINVAL`: Invalid argument.
- `-ENOTSUP`: Command or feature not supported.
- `-EIO`: Input/output error.
- `-EBUSY`: Device or resource busy.
- `-ENODEV`: No such device.
- `-EAGAIN`: Try again (e.g., non-blocking I/O).

## Naming Conventions
- Kernel APIs: `k_` prefix (e.g., `k_thread_create`).
- System/Utility: `sys_` prefix.
- Architecture-specific: `arch_` prefix.
- Driver APIs: Subsystem name prefix (e.g., `gpio_pin_set`).
