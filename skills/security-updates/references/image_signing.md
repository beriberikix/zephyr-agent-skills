# Image Signing & Key Management

MCUboot ensures that only authorized firmware runs on your device by verifying a digital signature on the image header.

## Digital Signatures
MCUboot supports several signature algorithms:
- **RSA**: Standard but requires more memory and processing.
- **ECDSA-P256**: Modern, efficient, and recommended for most microcontrollers.
- **Ed25519**: Extremely efficient, but less widely supported in hardware accelerators.

## Key Management

> [!CAUTION] 
> **NEVER use the default sample keys** (`root-rsa-2048.pem`, etc.) provided in the MCUboot repository for production. These keys are public and provide zero security.

### Generating a Production Key
Use the `imgtool.py` script provided with MCUboot:

```bash
# Generate a NIST P-256 key
imgtool keygen -k my_production_key.pem -t ecdsa-p256
```

### Configuring MCUboot to use your key
When building MCUboot, point it to your private key file:
```kconfig
CONFIG_BOOT_SIGNATURE_TYPE_ECDSA_P256=y
CONFIG_BOOT_SIGNATURE_KEY_FILE="my_production_key.pem"
```

## Signing the Application
Your application binary (`zephyr.bin`) must be signed before it can be booted by MCUboot.

```bash
imgtool sign \
    --key my_production_key.pem \
    --header-size 0x200 \
    --align 8 \
    --version 1.2.3+0 \
    --slot-size <size_of_slot0> \
    zephyr.bin signed_zephyr.bin
```

## Professional Pattern: Version Monotonicity
Enable **Version Monotonicity** in MCUboot to prevent "downgrade attacks" where an attacker flashes an older, verified version of your firmware that contains a known vulnerability.

```kconfig
CONFIG_BOOT_UPGRADE_ONLY=y
```
