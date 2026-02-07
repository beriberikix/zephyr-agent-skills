# Ztest Framework

Ztest is the primary testing framework used by Zephyr. It provides a C-based syntax for writing unit and integration tests that can run on native simulation or real hardware.

## Core Concepts
- **Test Suite**: A grouping of related test cases.
- **Test Case**: A single function that validates a specific behavior.
- **Expectations**: Macros like `zassert_equal` or `zassert_not_null` used to verify results.

## Basic Test Structure
A typical test file in `tests/` directory:

```c
#include <zephyr/ztest.h>

ZTEST_SUITE(my_feature_tests, NULL, NULL, NULL, NULL, NULL);

ZTEST(my_feature_tests, test_addition) {
    uint32_t a = 5;
    uint32_t b = 10;
    zassert_equal(a + b, 15, "Addition failed!");
}
```

## Advanced Features

### 1. Setup and Teardown
Define functions to run before and after the suite or individual tests.
```c
static void* my_suite_setup(void) {
    // Allocation or peripheral init
    return NULL;
}

ZTEST_SUITE(my_suite, NULL, my_suite_setup, NULL, NULL, NULL);
```

### 2. Mocking
While Ztest doesn't have a built-in heavy mocking framework, developers often use function pointers or the `fake_function_framework` (fff) integrated as a module.

### 3. Thread Safety
Ztest handles running test cases in their own threads, but be careful when testing multi-threaded code. Use `k_sleep` or kernel objects (semaphores) to synchronize with background tasks.

## Best Practices
- **Atomic Tests**: Each test case should be independent and not rely on the state of previous tests.
- **Descriptive Failures**: Always include a helpful error message in your `zassert` calls.
- **Native Execution**: Run your logic-only tests on `native_sim` first for rapid iteration before moving to hardware.
