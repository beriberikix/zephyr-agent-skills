/* Sensor polling template */

#include <zephyr/device.h>
#include <zephyr/drivers/sensor.h>

static const struct device *sensor = DEVICE_DT_GET(DT_ALIAS(ambient_temp0));

int read_sensor_once(struct sensor_value *out)
{
    if (!device_is_ready(sensor)) {
        return -ENODEV;
    }

    if (sensor_sample_fetch(sensor) < 0) {
        return -EIO;
    }

    if (sensor_channel_get(sensor, SENSOR_CHAN_AMBIENT_TEMP, out) < 0) {
        return -EIO;
    }

    return 0;
}
