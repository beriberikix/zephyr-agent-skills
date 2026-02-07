# Matter-over-Thread Devices

Matter is an industry-standard unified application layer protocol that allows devices to work across different smart home ecosystems (Apple, Google, Amazon).

## Architecture
Matter runs on top of IPv6. In constrained environments, **Thread** is the preferred transport, while **BLE** is used for the initial "Commissioning" (pairing) process.

## Commissioning Flow
1. **Discovery**: Device advertises via BLE.
2. **PAKE (Password Authenticated Key Exchange)**: Securely exchange credentials using a setup code/QR code.
3. **Operational Discovery**: Device joins the Thread network using credentials received over BLE.
4. **Interaction**: Device is now controllable via Matter clusters.

## Implementation Patterns

### 1. Clusters & Attributes
Matter defines "Clusters" (e.g., On/Off, Level Control, Temperature) that contain "Attributes".

```c
// Example: Handling an On/Off command
void matter_on_off_callback(uint16_t endpoint, bool on) {
    if (on) {
        led_on();
    } else {
        led_off();
    }
}
```

### 2. ZAP (Zigbee/Matter Alliance Processor)
Matter projects often use `.zap` or `.zap.template` files to generate the boilerplate code for clusters and endpoints.

### 3. nRF Connect SDK Integration
While Zephyr has basic Matter support, the **nRF Connect SDK (NCS)** provides the most mature implementation for Zephyr-based SoCs.

## Kconfig Configuration
```kconfig
CONFIG_CHIP=y                  # Enable Matter (Project CHIP)
CONFIG_CHIP_PROJECT_CONFIG="..."
CONFIG_CHIP_OPENTHREAD_TRANSPORT=y
```

## Professional Strategies
- **Multi-Admin**: Matter devices can be controlled by multiple controllers (e.g., both an Apple HomePod and a Google Nest Hub) simultaneously.
- **OTA Updates**: Always integrate Matter with a secure update mechanism like **MCUboot** (see **security-updates** skill).
- **Safety**: Implement "Software Component Isolation" if your device performs critical safety functions.
