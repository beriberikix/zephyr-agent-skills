/* Template health-bit map for watchdog supervised tasks. */

#ifndef APP_WDT_HEALTH_MAP_H_
#define APP_WDT_HEALTH_MAP_H_

#define HEALTH_BIT_SENSOR      (1u << 0)
#define HEALTH_BIT_COMMS       (1u << 1)
#define HEALTH_BIT_STORAGE     (1u << 2)
#define HEALTH_BIT_UI          (1u << 3)

#define HEALTH_ALL_REQUIRED (HEALTH_BIT_SENSOR | HEALTH_BIT_COMMS | HEALTH_BIT_STORAGE | HEALTH_BIT_UI)

#endif /* APP_WDT_HEALTH_MAP_H_ */
