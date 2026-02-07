# DFU Protocols & MCUmgr

Device Firmware Update (DFU) requires a protocol to transport the signed image to the device. Zephyr's primary tool for this is **MCUmgr**.

## MCUmgr Overview
MCUmgr is an 8-bit oriented management protocol used for DFU, file management, and log/stats access.

### Features
- **SMP (Simple Management Protocol)**: The underlying framing protocol.
- **Transports**: Works over UART, BLE, UDP, and USB.
- **Client Tools**: `mcumgr` CLI, mobile apps (nRF Connect Device Manager).

## Configuration
To enable MCUmgr DFU over BLE, add the following to `prj.conf`:

```kconfig
# Enable MCUmgr and SMP
CONFIG_MCUMGR=y
CONFIG_MCUMGR_TRANSPORT_BT=y

# Enable Image Management (DFU)
CONFIG_MCUMGR_GRP_IMG=y
CONFIG_MCUMGR_IMG_DIRECT_UPLOAD=y

# Dependencies
CONFIG_BT=y
CONFIG_BT_PERIPHERAL=y
```

> [!NOTE]
> For detailed BLE configuration and advertising patterns, see **[connectivity-ble](../../connectivity-ble/SKILL.md)**.

## MCUmgr CLI Usage

### 1. Identify the device
```bash
mcumgr --conntype ble --connstring "name=MyDevice" echo hello
```

### 2. Upload a new image
```bash
mcumgr --conntype ble --connstring "name=MyDevice" image upload signed_zephyr.bin
```

### 3. List and test the image
```bash
mcumgr --conntype ble --connstring "name=MyDevice" image list
mcumgr --conntype ble --connstring "name=MyDevice" image test <hash_of_new_image>
```

## Professional Pattern: Golioth Cloud OTA
For remote updates, Golioth utilizes the same DFU backend but automates the transport.
- **Release Management**: Bundle artifacts into a single release package in the Golioth Console.
- **Cohort Deployment**: Deploy updates to specific groups of devices (e.g., "staging" vs. "production").
- **Delta Updates**: Golioth can send only the changes between firmware versions, dramatically reducing data usage for cellular devices.
