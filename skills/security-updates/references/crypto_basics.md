# Crypto Basics & Secure Storage

Zephyr utilizes **mbedTLS** as its primary cryptographic library and provides standard APIs for accessing hardware security modules (HSM) or Trusted Execution Environments (TEE) like **TF-M**.

## mbedTLS Integration
To enable basic crypto operations, add the following to `prj.conf`:

```kconfig
CONFIG_MBEDTLS=y
CONFIG_MBEDTLS_BUILTIN=y
CONFIG_MBEDTLS_ENABLE_ALL_256_CURVES=y
```

### Example: Random Number Generation
```c
#include <zephyr/crypto/crypto.h>

void get_random(uint8_t *output, size_t len) {
    const struct device *dev = DEVICE_DT_GET(DT_CHOSEN(zephyr_crypto_controller));
    if (device_is_ready(dev)) {
        crypto_get_entropy(dev, output, len);
    }
}
```

## TF-M (Trusted Firmware-M)
For high-security applications (ARM PSA certified), Zephyr can run on top of TF-M.
- **Isolation**: Critical keys and crypto operations run in a "Secure World" isolated from the main application.
- **Secure Storage**: Provides a protected area for storing private keys that cannot be read by the main "Non-Secure" application.

## Best Practices
- **Hardware Acceleration**: Always enable hardware-specific Kconfigs (e.g., `CONFIG_CRYPTO_STM32`) to utilize the SoC's crypto engine instead of software emulation.
- **Key Storage**: Never hardcode private keys in the binary. Use NVS or TF-M Secure Storage to store keys provisioned during manufacturing.
- **Entropy Source**: Ensure `CONFIG_ENTROPY_GENERATOR` is enabled to provide cryptographically secure random numbers.
