# IoT Protocol Selection

Choosing the right application-layer protocol is critical for balancing power, bandwidth, and device management requirements.

## Comparison Table

| Feature | LwM2M | CoAP | MQTT |
| :--- | :--- | :--- | :--- |
| **Transport** | UDP (typically) | UDP (typically) | TCP |
| **Overhead** | Very Low | Low | Moderate |
| **Model** | Object-based | Request/Response | Pub/Sub |
| **Device Mgmt** | Built-in | None (manual) | None (manual) |
| **Power Efficiency**| High | High | Moderate |

## Quick Decision Guide
- **Need device management (FOTA, config)?** → LwM2M
- **RESTful API over constrained network?** → CoAP
- **Simple pub/sub with cloud provider?** → MQTT

## 1. LwM2M (Lightweight M2M)
Best for: Professional IoT fleets requiring standardized device management (FOTA, configuration, monitoring).
- **Pros**: Standardized data model, excellent for low-power (UDP), built-in security (DTLS).
- **Cons**: Higher complexity to implement custom objects.

## 2. CoAP (Constrained Application Protocol)
Best for: Direct resource access in restricted environments where RESTful patterns are preferred.
- **Pros**: Extremely lightweight, maps directly to HTTP patterns, low RAM footprint.
- **Cons**: Requires manual implementation of device management features.

## 3. MQTT (Message Queuing Telemetry Transport)
Best for: Applications requiring a simple publish-subscribe model and reliable delivery over stable connections.
- **Pros**: Very easy to implement, widely supported by cloud providers.
- **Cons**: TCP overhead can be high for low-power/cellular; persistent connections consume battery.

## Knowledge from Golioth
Golioth primarily uses **CoAP** as the underlying transport for its efficiency, but provides a high-level SDK that handles device management features similar to LwM2M.

## Kconfig Selection
Select the appropriate subsystem in your `prj.conf`:
```kconfig
CONFIG_LWM2M=y        # Enable LwM2M
CONFIG_COAP=y         # Enable CoAP
CONFIG_MQTT_LIB=y     # Enable MQTT Library
```
