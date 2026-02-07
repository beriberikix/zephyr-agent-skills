/*
 * Template Zephyr Driver
 * Demonstrates: CONTAINER_OF, Mutex, Error Handling, DT Macros
 */

#define DT_DRV_COMPAT my_company_template_driver

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/logging/log.h>
#include <zephyr/drivers/gpio.h>

LOG_MODULE_REGISTER(template_driver, CONFIG_TEMPLATE_DRIVER_LOG_LEVEL);

struct template_config {
    struct gpio_dt_spec alert_gpio;
};

struct template_data {
    struct k_mutex lock;
    uint32_t value;
};

static int template_init(const struct device *dev)
{
    const struct template_config *config = dev->config;
    struct template_data *data = dev->data;

    k_mutex_init(&data->lock);

    if (!device_is_ready(config->alert_gpio.port)) {
        LOG_ERR("Alert GPIO device not ready");
        return -ENODEV;
    }

    LOG_INF("Template driver initialized");
    return 0;
}

// Public API (should be declared in include/my_company/template_driver.h)
int template_get_value(const struct device *dev, uint32_t *val)
{
    struct template_data *data = dev->data;

    k_mutex_lock(&data->lock, K_FOREVER);
    *val = data->value;
    k_mutex_unlock(&data->lock);

    return 0;
}

#define TEMPLATE_INST(inst)                                             \
    static const struct template_config template_config_##inst = {      \
        .alert_gpio = GPIO_DT_SPEC_INST_GET(inst, alert_gpios),         \
    };                                                                  \
                                                                        \
    static struct template_data template_data_##inst;                   \
                                                                        \
    DEVICE_DT_INST_DEFINE(inst,                                         \
                         template_init,                                 \
                         NULL,                                          \
                         &template_data_##inst,                         \
                         &template_config_##inst,                       \
                         POST_KERNEL,                                   \
                         CONFIG_TEMPLATE_DRIVER_INIT_PRIORITY,          \
                         NULL);

DT_INST_FOREACH_STATUS_OKAY(TEMPLATE_INST)
