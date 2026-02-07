# State Machine Framework (SMF)

The Zephyr State Machine Framework (SMF) provides a standard way to implement finite state machines (FSM) and hierarchical state machines (HSM).

## Core Concepts
- **States**: Defined by an entry, run, and exit function.
- **Object**: The user-defined structure that holds the state context and the `struct smf_ctx`.
- **Transitions**: Moving from one state to another using `smf_set_state`.

## Implementation Pattern

### 1. Define the Context
```c
#include <zephyr/smf.h>

struct my_app_obj {
    struct smf_ctx ctx;
    // App-specific data
    int value;
};
```

### 2. Define the States
```c
enum my_states { STATE_INIT, STATE_IDLE, STATE_ACTIVE };

static void state_init_entry(void *obj) { /* Entry logic */ }
static void state_init_run(void *obj) {
    struct my_app_obj *app = obj;
    smf_set_state(SMF_CTX(app), &states[STATE_IDLE]);
}

static const struct smf_state states[] = {
    [STATE_INIT] = SMF_CREATE_STATE(state_init_entry, state_init_run, NULL),
    [STATE_IDLE] = SMF_CREATE_STATE(NULL, state_idle_run, NULL),
    // ...
};
```

### 3. Execution Loop
```c
void thread_fn(void) {
    struct my_app_obj app;
    smf_set_initial(SMF_CTX(&app), &states[STATE_INIT]);

    while (1) {
        smf_run_state(SMF_CTX(&app));
        k_msleep(100);
    }
}
```

## Hierarchical State Machines (HSM)
HSMs allow you to define parent states, reducing duplication for common behaviors (like error handling or power management).

```c
static const struct smf_state states[] = {
    [PARENT_STATE] = SMF_CREATE_STATE(entry_fn, run_fn, exit_fn, NULL),
    [CHILD_STATE] = SMF_CREATE_STATE(entry_fn, run_fn, exit_fn, &states[PARENT_STATE]),
};
```
The parent state is specified as the 4th parameter.

## Professional Patterns (from Golioth)
- **Combine with Zbus**: Trigger state transitions based on Zbus events.
- **Modularization**: Each major feature (Network, Cloud, FOTA) often gets its own SMF-based module.
- **Clean Transitions**: Always use entry/exit functions to manage hardware state or memory instead of putting cleanup in the run function.

## Enabling SMF
```kconfig
CONFIG_SMF=y
CONFIG_SMF_ANCESTOR_SUPPORT=y  # For hierarchical state machines
```
