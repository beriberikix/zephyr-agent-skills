# BLE Fundamentals

Zephyr provides a highly configurable and feature-rich Bluetooth Low Energy (BLE) stack.

## Core Concepts
- **GAP (Generic Access Profile)**: Defines advertising, scanning, and connection management.
- **GATT (Generic Attribute Profile)**: Defines how data is organized into Services and Characteristics.
- **Host vs Controller**: Zephyr can run both or just one (e.g., using an external controller via HCI).

## Advertising
The most common way to make a device discoverable.

```c
#include <zephyr/bluetooth/bluetooth.h>
#include <zephyr/bluetooth/gap.h>

static const struct bt_data ad[] = {
    BT_DATA_BYTES(BT_DATA_FLAGS, (BT_LE_AD_GENERAL | BT_LE_AD_NO_BREDR)),
    BT_DATA(BT_DATA_NAME_COMPLETE, "Zephyr Device", 13),
};

void start_adv(void) {
    bt_enable(NULL);
    bt_le_adv_start(BT_LE_ADV_CONN_NAME, ad, ARRAY_SIZE(ad), NULL, 0);
}
```

## Services & Characteristics
GATT data hierarchy.

```c
#include <zephyr/bluetooth/gatt.h>

BT_GATT_SERVICE_DEFINE(my_service,
    BT_GATT_PRIMARY_SERVICE(BT_UUID_DECLARE_16(0x1234)),
    BT_GATT_CHARACTERISTIC(BT_UUID_DECLARE_16(0x5678),
                           BT_GATT_CHRC_READ | BT_GATT_CHRC_NOTIFY,
                           BT_GATT_PERM_READ,
                           read_fn, NULL, &val),
    BT_GATT_CCC(ccc_cfg_changed, BT_GATT_PERM_READ | BT_GATT_PERM_WRITE),
);
```

## Connection Management
Register callbacks to handle connection and disconnection.

```c
static void connected(struct bt_conn *conn, uint8_t err) { /* ... */ }
static void disconnected(struct bt_conn *conn, uint8_t reason) { /* ... */ }

BT_CONN_CB_DEFINE(conn_callbacks) = {
    .connected = connected,
    .disconnected = disconnected,
};
```

## Security (Pairing & Bonding)
Register authentication callbacks to handle pairing requests.

```c
static void auth_passkey_display(struct bt_conn *conn, unsigned int passkey) {
    printk("Passkey: %06u\n", passkey);
}

static void auth_cancel(struct bt_conn *conn) {
    printk("Pairing cancelled\n");
}

static const struct bt_conn_auth_cb auth_callbacks = {
    .passkey_display = auth_passkey_display,
    .cancel = auth_cancel,
};

void init_security(void) {
    bt_conn_auth_cb_register(&auth_callbacks);
}
```

## Best Practices
- **UUID Selection**: Use standard 16-bit UUIDs for adopted services, and 128-bit random UUIDs for custom services.
- **Payload Minimization**: Keep advertising names short to fit in the 31-byte limit.
- **Security by Design**: Implement pairing and bonding if data privacy or integrity is required.

## Enabling the BLE Stack
```kconfig
CONFIG_BT=y
CONFIG_BT_PERIPHERAL=y
CONFIG_BT_DEVICE_NAME="Zephyr Device"
CONFIG_BT_MAX_CONN=1
```
