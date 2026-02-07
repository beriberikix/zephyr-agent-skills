# Pinctrl & GPIO

Managing pins and basic input/output is the foundation of any hardware interface in Zephyr.

## Pinctrl (Pin Control)
Pinctrl handles the multiplexing and electrical configuration (pull-up, pull-down, drive strength) of pins. It is almost entirely configured in Devicetree.

### 1. Defining Pin States
Typically defined in the board's `.dts` or an overlay.
```dts
&pinctrl {
    uart0_default: uart0_default {
        group1 {
            psels = <NRF_PSEL(UART_TX, 0, 6)>,
                    <NRF_PSEL(UART_RX, 0, 8)>;
            bias-pull-up;
        }
    };
};
```

### 2. Assigning to Peripherals
```dts
&uart0 {
    pinctrl-0 = <&uart0_default>;
    pinctrl-names = "default";
    status = "okay";
};
```

## GPIO (General Purpose I/O)
Used for simple signals like buttons, LEDs, and chip-selects.

### 1. Devicetree Configuration
```dts
/ {
    leds {
        compatible = "gpio-leds";
        led0: led_0 {
            gpios = <&gpio0 13 GPIO_ACTIVE_LOW>;
        };
    };
};
```

### 2. Runtime API
```c
#include <zephyr/drivers/gpio.h>

const struct gpio_dt_spec led = GPIO_DT_SPEC_GET(DT_ALIAS(led0), gpios);

void setup(void) {
    gpio_pin_configure_dt(&led, GPIO_OUTPUT_ACTIVE);
}

void toggle(void) {
    gpio_pin_toggle_dt(&led);
}
```

### 3. GPIO Interrupts
```c
static struct gpio_callback button_cb;

void button_pressed(const struct device *dev, struct gpio_callback *cb, uint32_t pins) {
    // Handle button press
}

void setup_button(void) {
    const struct gpio_dt_spec button = GPIO_DT_SPEC_GET(DT_ALIAS(sw0), gpios);
    
    gpio_pin_configure_dt(&button, GPIO_INPUT);
    gpio_pin_interrupt_configure_dt(&button, GPIO_INT_EDGE_TO_ACTIVE);
    
    gpio_init_callback(&button_cb, button_pressed, BIT(button.pin));
    gpio_add_callback(button.port, &button_cb);
}
```

## Tips for Success
- **Use `dt_spec`**: The `_dt` variants of the GPIO functions are much safer and handle polarity automatically based on Devicetree bits.
- **Check Schematics**: Always verify `GPIO_ACTIVE_LOW` vs `GPIO_ACTIVE_HIGH` against your hardware design.
- **Inspect Pinmux**: Use `west build -t rom_report` or vendor-specific tools to verify your pin multiplexing.
