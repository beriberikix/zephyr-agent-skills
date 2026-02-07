# **Zephyr RTOS Agent Skills**

**Comprehensive Skill List for Embedded Development**

* **Version:** 1.8  
* **Last Updated:** February 7, 2026  
* **Target Platform:** Zephyr RTOS 4.3.0+

## **Overview**

This document provides a complete catalog of Agent Skills for Zephyr RTOS development.

## **Tier 0: Embedded Foundations (Zephyr Context)**

**Universal Skills Mapped to Zephyr APIs**

*These skills apply implicitly when executing Zephyr tasks.*

**0.1. Embedded C & Zephyr Macros**

* **Bit Manipulation:** Using Zephyr's BIT(), sys\_set\_bit(), and GENMASK() macros instead of raw shifting.  
* **Container Macros:** Mastering CONTAINER\_OF() for driver and linked-list structures.  
* **Types:** Strict usage of \<zephyr/types.h\> and \<stdint.h\> (e.g., uint32\_t, k\_timeout\_t).  
* **Memory Attributes:** Using \_\_aligned(), \_\_packed, and \_\_noinit for linker control.

**0.2. Real-Time Concurrency in Zephyr**

* **Race Conditions:** Protecting shared data using k\_spinlock or k\_mutex.  
* **Priority Inversion:** Understanding how k\_mutex handles priority inheritance vs. k\_sem which does not.  
* **Atomicity:** Using the atomic\_t API (atomic\_set, atomic\_cas) for lock-free state.  
* **Reentrancy:** Writing ISR-safe code (avoiding k\_mutex or blocking calls inside interrupts).

**0.3. Hardware Literacy for Devicetree**

* **Datasheet to DTS:** Translating datasheet register maps and base addresses into Devicetree nodes.  
* **Schematic to Pinctrl:** Reading schematics to configure pinctrl nodes (pull-ups, drive strength).  
* **Bus Protocols:** Configuring SPI CPOL/CPHA and I2C flags (I2C\_MSG\_READ, I2C\_MSG\_STOP) correctly in drivers.  
* **Interrupts:** Mapping hardware IRQ lines and priorities to Devicetree interrupts properties.

**0.4. Defensive Programming & Safety**

* **Asserts:** Using Zephyr's \_\_ASSERT macro (guarded by CONFIG\_ASSERT) to catch logic errors during development.  
* **Error Handling:** Returning standard negative error codes (e.g., \-EINVAL, \-ENOMEM, \-ETIMEDOUT) from \<errno.h\>.  
* **Input Validation:** Checking bounds on data from external buses before processing.  
* **Buffer Safety:** Using net\_buf or sys\_slist APIs instead of raw pointer arithmetic where possible.

## **Tier 1: Essential Zephyr Workflows**

**Core Skills \- High Value, Frequent Use**

These skills serve 80% of Zephyr developers in their daily work.

### **Build System & Tooling**

**1\. West Workspace Setup and Management**

* Initialize west workspaces  
* Configure manifest files for multi-repo projects  
* Manage modules and dependencies  
* **Apply West Snippets for common configurations**
* Handle manifest imports and projects

**2\. Sysbuild (System Build) Configuration**

* Configure sysbuild.conf for multi-image builds  
* Manage dependency between images (e.g., MCUboot \+ App)  
* Configure image signing within the build system  
* Overlay configuration for specific images

**3\. Kconfig Navigation and Optimization**

* Configure build options efficiently  
* Use menuconfig and guiconfig  
* Create defconfig and fragment files  
* Understand Kconfig dependencies and symbols  
* Debug configuration issues

**4\. CMake Integration for Applications**

* Create custom build targets  
* Configure out-of-tree builds  
* Integrate external libraries  
* Set up module CMakeLists.txt  
* Manage application-specific build flags

**5\. Devicetree Creation and Debugging**

* Write devicetree source files (.dts, .dtsi)  
* Create and use overlays  
* **Validate against YAML bindings** (dts/bindings)  
* Debug devicetree compilation errors  
* Use devicetree macros in C code

**6\. Native Simulator Workflow (native\_sim)**

* Run code immediately without hardware (POSIX/Host)  
* Self-verify logic and unit tests  
* Debug segfaults using host tools (Valgrind/GDB)  
* Integrate with CI pipelines

### **Core Development**

**7\. New Board Bringup Workflow (HWMv2)**

* **Implement Hardware Model v2:** Use modern boards/ structure, board.yml, and SoC separation.  
* Directory structure and file organization  
* Hardware configuration and validation  
* Documentation and testing

**8\. Zephyr Module Creation**

* Structure out-of-tree drivers and subsystems  
* Configure module.yml  
* Integrate with west workspace  
* Version and distribute modules

**9\. Thread Management and Scheduling**

* Create and configure kernel threads  
* Set thread priorities and options  
* Use synchronization primitives (mutex, semaphore, condvar)  
* Implement thread communication patterns

**10\. Logging Subsystem Setup**

* Configure logging backends (UART, RTT, filesystem)  
* Set up log levels and filtering  
* Use structured logging (LOG\_INF, LOG\_ERR)  
* Optimize logging for production (dictionary/deferred logging)

**11\. Shell Subsystem Integration**

* Add custom shell commands  
* Implement command autocompletion and subcommands  
* Use shell for runtime debugging  
* Configure shell backends (UART, USB, RTT)

## **Tier 2: Common Zephyr Features**

**Important Skills \- Regular Use, Significant Value**

### **Kernel & Services**

**12\. Zbus (Zephyr Bus) Integration** *(Modern Event Architecture)*

* Define Zbus channels and messages  
* Implement listeners and subscribers  
* Decouple subsystems using event-driven patterns  
* Debug Zbus observers and data flow

**13\. State Machine Framework (SMF)**

* Implement hierarchical state machines  
* Define states, entries, runs, and exits  
* Manage state transitions  
* Replace ad-hoc switch-case logic with SMF

**14\. Memory Management Patterns**

* Configure heap and stack sizes  
* Use k\_malloc/k\_free and memory slabs  
* Implement memory domains  
* Configure MPU/MMU regions

**15\. Work Queues and Timers**

* Use k\_work API for deferred processing  
* Configure system and user work queues  
* Implement delayable work  
* Use k\_timer for scheduled tasks

**16\. Interrupt Handling and IRQ**

* Use IRQ\_CONNECT macro  
* Configure interrupt priorities  
* Implement ISR best practices (short, non-blocking)  
* Use direct interrupts and zero-latency interrupts

**17\. Settings Subsystem (Persistence)**

* Implement persistent configuration storage  
* Integrate with NVS (Non-Volatile Storage) backend  
* Define settings handlers (settings\_register)  
* Migrate settings between firmware versions

**18\. Event and Notification Patterns**

* Use k\_poll for multi-object waiting  
* Implement k\_event for bit-flag signaling  
* Use k\_msgq for simple message passing (vs Zbus)

### **Hardware Integration**

**19\. Pin Configuration (pinctrl)**

* Configure pin muxing in devicetree  
* Use pinctrl devicetree bindings  
* Handle pin state transitions (sleep vs active)  
* Support multiple pin states

**20\. Input Subsystem**

* Configure input devices (Buttons, Touch, Encoders) in Devicetree  
* Implement input event listeners (INPUT\_CALLBACK\_DEFINE)  
* Map input codes to application actions  
* Decouple hardware drivers from UI logic

**21\. Sensor Subsystem Usage**

* Use sensor API for standardized access  
* Configure sensor triggers and attributes  
* Handle sensor channels and data scaling  
* Process sensor data efficiently

**22\. GPIO and Interrupt Callbacks**

* Configure GPIO pins  
* Set up edge and level interrupts  
* Implement GPIO callbacks  
* Use GPIO flags (active low/high)

**23\. DMA Configuration**

* Configure DMA controllers in Devicetree  
* Set up DMA channels and requests  
* Use DMA for peripheral transfers (SPI/I2C/UART)  
* Handle DMA completion callbacks

**24\. ADC/DAC Patterns**

* Configure ADC channels and sequences  
* Implement sampling strategies  
* Handle calibration and reference voltages  
* Use buffered acquisition

### **Power & Performance**

**25\. Power Management (PM)**

* Configure system PM states  
* Implement device PM (suspend/resume)  
* Use low-power modes (tickless idle)  
* Measure and optimize power consumption

**26\. Real-time Performance Tuning**

* Optimize thread priorities  
* Analyze stack usage  
* Measure timing and latency  
* Configure tick rates

**27\. Code/Data Relocation**

* Configure XIP (Execute in Place)  
* Use ITCM/DTCM regions (Tightly Coupled Memory)  
* Create custom linker sections (zephyr\_linker\_section)  
* Optimize memory layout

## **Tier 3: Advanced Features**

**Specialized Skills \- Situational, High-Impact Use**

### **Connectivity Stacks**

**28\. Bluetooth LE Peripheral/Central**

* Configure GAP and GATT  
* Implement services and characteristics  
* Handle connections, pairing, and bonding  
* Use advertising and scanning extensions

**29\. Network Stack Configuration**

* Set up IPv4/IPv6 networking  
* Configure sockets API (BSD-like)  
* Use net\_mgmt for event monitoring  
* Implement network services (DNS, DHCP, SNTP)

**30\. LwM2M Client Implementation**

* Configure OMA LwM2M client  
* Register resources and IPSO objects  
* Handle server communication (Bootstrap/Registration)  
* Implement FOTA via LwM2M

**31\. CoAP Client/Server**

* Set up CoAP endpoints  
* Implement resources and handlers  
* Use observe functionality  
* Configure block transfer

**32\. MQTT Client Patterns**

* Configure MQTT client  
* Implement publish/subscribe  
* Handle QoS levels and keep-alive  
* Integrate TLS/DTLS credentials

**33\. USB Device Classes**

* Implement CDC-ACM serial  
* Configure HID devices (Mouse/Keyboard)  
* Set up mass storage (MSC)  
* Handle USB device events

**34\. CAN and CAN-FD Setup**

* Configure CAN controller  
* Implement ISO-TP protocol  
* Set up filters and callbacks  
* Use CAN-FD features (Bitrate switching)

### **Storage & Filesystems**

**35\. Flash Storage (NVS, FCB, LittleFS)**

* Use NVS for key-value storage  
* Implement FCB for circular logs  
* Configure LittleFS filesystem  
* Handle wear leveling

**36\. File System Mounting**

* Mount FAT and LittleFS  
* Use SD card and external flash  
* Implement file operations (fs\_open, fs\_write)

**37\. Flash Map and Partitions**

* Define flash partitions in Devicetree (fixed-partitions)  
* Use partition manager  
* Access flash areas (flash\_area\_read)

**38\. Stream Flash API**

* Implement efficient flash writing  
* Use stream flash buffering  
* Handle page boundaries

**39\. Retained Memory (Retained Mem)**

* Configure retained memory regions in Devicetree  
* Store critical state across reboots without flash wear  
* Handle checksums and validation

### **Testing & Debugging**

**40\. Twister & Ztest Framework**

* Write unit tests using Ztest  
* **Invoke Twister** for test running and reporting  
* Implement mocking  
* Filter test suites via testcase.yaml

**41\. Thread Analyzer**

* Analyze stack usage at runtime  
* Measure thread CPU utilization  
* Identify stack overflows

**42\. Tracing Subsystem**

* Configure CTF (Common Trace Format)  
* Use SystemView integration for visualization  
* Implement Segger RTT tracing

**43\. GDB & Core Dump Debugging**

* Set breakpoints and watchpoints  
* **Configure and analyze Zephyr Core Dumps**  
* Debug multi-core systems  
* Analyze crashes and faults

## **Tier 4: Production & Advanced**

**Domain-Specific Skills \- Specialized, Niche Applications**

### **Security & Updates**

**44\. MCUboot Integration**

* Configure secure bootloader  
* Implement image signing  
* Handle rollback protection  
* Set up dual-bank updates (Swap scratch vs move)

**45\. TF-M (Trusted Firmware-M)**

* Configure PSA Crypto  
* Use secure services  
* Implement secure partitions  
* Handle secure/non-secure boundaries

**46\. DFU and FOTA**

* Implement over-the-air updates  
* Configure image management (img\_mgmt)  
* Handle update verification

**47\. mbedTLS Configuration**

* Set up TLS/DTLS  
* Configure cipher suites  
* Manage certificates and keys  
* Optimize crypto performance (RAM usage)

**48\. Crypto API Usage**

* Use hardware crypto acceleration  
* Implement secure random generation  
* Configure crypto algorithms

### **Mesh & IoT Protocols**

**49\. OpenThread Mesh Networking**

* Configure Thread protocol stack  
* Implement border router  
* Handle commissioning

**50\. Golioth Platform Integration**

* Configure Golioth SDK module  
* Implement device provisioning and authentication  
* Use LightDB State and Stream services  
* Handle OTA updates via Golioth  
* Use Remote Procedure Calls (RPC)

**51\. LoRaWAN Stack Integration**

* Configure Class A/B/C devices  
* Implement OTAA and ABP activation  
* Optimize power for LoRa

**52\. Matter (CHIP) Integration**

* *Note: Matter uses Zephyr as an OS but requires the external Matter SDK.*  
* Configure Matter build options  
* Implement device types and endpoints  
* Handle commissioning (BLE/WiFi/Thread)

### **Multi-core & Advanced Architecture**

**53\. SMP (Symmetric Multiprocessing)**

* Configure multi-core RTOS  
* Set CPU affinity  
* Handle SMP synchronization (Spinlocks)

**54\. LLEXT (Linkable Loadable Extensions)**

* Configure LLEXT subsystem  
* Build and sign loadable ELF modules  
* Load and execute code segments at runtime  
* Manage symbol tables for extensions

**55\. AMP and IPC**

* Configure OpenAMP  
* Use RPMsg for inter-core communication  
* Handle resource tables

**56\. Userspace and Memory Domains**

* Configure process isolation  
* Implement system calls (Z\_SYSCALL)  
* Use memory domains for permission control

**57\. Custom SoC Porting**

* Port to new architecture or SoC  
* Implement HAL integration  
* Configure clock trees and PLLs

### **Industrial & Automotive**

**58\. Modbus RTU/TCP**

* Implement Modbus protocol (Client/Server)  
* Configure RTU and TCP modes  
* Handle register mapping

**59\. CANopen Stack**

* Configure CANopen protocol  
* Implement object dictionary  
* Handle SDO/PDO

### **Ultra-Specialized**

**60\. Audio Subsystem**

* Configure I2S interface  
* Implement codec drivers  
* Use audio processing (DMIC)

**61\. Display Subsystem**

* Integrate LVGL graphics library  
* Configure framebuffer and display drivers  
* Handle touch input devices

**62\. Fault Injection and Safety**

* Implement fault handling hooks  
* Configure watchdog timers  
* Validate safety requirements (MISRA-C compliance)