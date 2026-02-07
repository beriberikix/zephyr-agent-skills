# LVGL GUI Development

LVGL (Light and Versatile Graphics Library) is the primary graphics stack for Zephyr, enabling sophisticated GUIs on microcontrollers with limited memory.

## Core Concepts
- **Widgets**: Basic building blocks (Buttons, Labels, Sliders, Charts).
- **Styles**: Custom CSS-like properties for coloring, padding, and borders.
- **Events**: Callbacks triggered by user interaction or system changes.
- **Input Devices**: Pointers (touch), Keypads, Encoders, or Buttons.

## Configuration
Zephyr includes LVGL as a module. Enable it in `prj.conf`:

```kconfig
CONFIG_LVGL=y
CONFIG_LV_Z_MEM_POOL_SIZE=16384 # Reserved RAM for LVGL objects
CONFIG_LV_Z_VDB_SIZE=100        # Display buffer size (percentage of screen)

# Input Device Support
CONFIG_LV_Z_POINTER_KSCAN=y    # Use keyboard scan for touch
```

## Basic Implementation

### 1. Creating a Label
```c
#include <zephyr/device.h>
#include <lvgl.h>

void create_ui(void) {
    lv_obj_t *label = lv_label_create(lv_scr_act());
    lv_label_set_text(label, "Hello Zephyr!");
    lv_obj_align(label, LV_ALIGN_CENTER, 0, 0);
}
```

### 2. Handling a Button Click
```c
static void btn_event_cb(lv_event_t *e) {
    lv_event_code_t code = lv_event_get_code(e);
    if (code == LV_EVENT_CLICKED) {
        printk("Button clicked!\n");
    }
}

void add_button(void) {
    lv_obj_t *btn = lv_btn_create(lv_scr_act());
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_ALL, NULL);
}
```

## Performance Optimization
- **Double Buffering**: Use `CONFIG_LV_Z_DOUBLE_VDB=y` for smooth, flicker-free animations.
- **DPI Adjustment**: Set `CONFIG_LV_DPI_DEF` according to your physical display size.
- **Flush Thread**: Enable `CONFIG_LV_Z_FLUSH_THREAD=y` to perform display data flushing in a separate thread, freeing the main GUI thread for rendering.

## Professional Patterns
- **Asset Management**: Use the LVGL Image Converter to convert PNG/JPG to C arrays for inclusion in the binary.
- **Theming**: Create a custom theme to ensure a consistent look and feel across all screens.
- **Simulator**: Use the `native_sim` board with the SDL display driver to develop your UI on your PC before deploying to hardware.
