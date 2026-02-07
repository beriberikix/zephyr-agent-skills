# BLE Power Optimization

Optimizing BLE consumption involves managing the balance between responsiveness (latency) and battery life.

## Advertising Optimization
Advertising is the most power-hungry phase before a connection is established.

### 1. Intervals
- **Fast Advertising**: High responsiveness, high power (e.g., 20ms - 100ms).
- **Slow Advertising**: Low power, slow connection time (e.g., 1s - 10s).

```c
struct bt_le_adv_param param = BT_LE_ADV_PARAM_INIT(
    BT_LE_ADV_OPT_CONNECTABLE,
    BT_GAP_ADV_SLOW_INT_MIN,
    BT_GAP_ADV_SLOW_INT_MAX,
    NULL
);
```

### 2. Directed Advertising
If the peer's address is known, use directed advertising to reduce scanning time by the central.

## Connection Parameters
Once connected, parameters determine how often the devices sync.

- **Connection Interval**: Frequency of radio sync (e.g., 7.5ms to 4s).
- **Peripheral Latency**: Number of intervals the peripheral can skip if it has no data.
- **Supervision Timeout**: Time before the link is considered lost.

```c
struct bt_le_conn_param update_param = {
    .interval_min = 800, // 1 second
    .interval_max = 1600, // 2 seconds
    .latency = 5,
    .timeout = 1000, // 10 seconds
};
bt_conn_le_param_update(conn, &update_param);
```

## System-Level Strategies
- **Data Buffering**: Use "Send-When-Idle" to stay in low power longer.
- **Lower PHY**: Using 2M PHY (if supported) can reduce radio on-time for large transfers.
- **Power Measurement**: Always validate with a Power Profiler to see the "spikes" during radio events.

## Kconfig for Low Power
```kconfig
CONFIG_BT_CTLR_TX_PWR_DYNAMIC=y
CONFIG_BT_CTLR_TX_PWR_0=y # 0 dBm (Standard)
```
Lowering TX power can save significant current if the range requirement allows it.
