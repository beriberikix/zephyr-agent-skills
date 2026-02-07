# LoRaWAN Basics

LoRa (Long Range) is a low-power wide-area network (LPWAN) technology. Zephyr provides a standardized LoRa driver API that supports multiple radio chips (e.g., Semtech SX12xx).

## Core Concepts
- **LoRa (PHY)**: The physical radio modulation.
- **LoRaWAN (MAC)**: The networking protocol providing security, addressing, and regional regulatory compliance.
- **Classes**:
  - **Class A**: Lowest power, device initiates all communication.
  - **Class B**: Periodic receive windows synced to a beacon.
  - **Class C**: Radio always on, lowest latency.

## Basic Configuration
```kconfig
CONFIG_LORA=y
CONFIG_HAS_SEMTECH_LORAMAC=y  # LoRaWAN stack
```

## Implementation (LoRa PHY)
Sending a raw packet:

```c
#include <zephyr/drivers/lora.h>

void send_lora(void) {
    const struct device *lora_dev = DEVICE_DT_GET(DT_ALIAS(lora0));
    struct lora_modem_config config = {
        .frequency = 868100000,
        .bandwidth = LORA_BW_125_KHZ,
        .datarate = LORA_DR_SF7,
        .coding_rate = LORA_CR_4_5,
        .preamble_len = 8,
        .tx_power = 4,
    };
    
    lora_config(lora_dev, &config);
    lora_send(lora_dev, "Hello", 5);
}
```

## LoRaWAN Integration
Most developers use a library like **Semtech's LoRaMac-node**, integrated as a Zephyr module, to handle joining and packet fragmentation.

## Best Practices
- **Regional Parameters**: Always ensure your frequency and TX power comply with local regulations (e.g., EU868, US915).
- **Duty Cycle**: LoRaWAN often enforces a 1% duty cycle limit. Implement appropriate backoff logic in your application.
- **Adaptive Data Rate (ADR)**: Enable ADR to allow the network to optimize your device's battery usage and range automatically.
