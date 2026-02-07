# Zephyr Shell

The shell provides a powerful interactive command-line interface for your device.

## Enabling the Shell
```kconfig
CONFIG_SHELL=y
CONFIG_SHELL_BACKEND_UART=y
```

## Adding Commands
Use `SHELL_CMD_REGISTER` to add a new top-level command.

```c
#include <zephyr/shell/shell.h>

static int cmd_version(const struct shell *sh, size_t argc, char **argv)
{
    shell_print(sh, "App Version: 1.0.0");
    return 0;
}

SHELL_CMD_REGISTER(version, NULL, "Print app version", cmd_version);
```

## Subcommands
Organize complex CLI interfaces using subcommand sets.

```c
SHELL_STATIC_SUBCMD_SET_CREATE(sub_led,
    SHELL_CMD(on, NULL, "Turn LED on", cmd_led_on),
    SHELL_CMD(off, NULL, "Turn LED off", cmd_led_off),
    SHELL_SUBCMD_SET_END
);
SHELL_CMD_REGISTER(led, &sub_led, "LED control commands", NULL);
```

## Benefits of the Shell
- Real-time hardware inspection.
- Calling functions without recompiling.
- Debugging connectivity (e.g., `net connectivity`).
