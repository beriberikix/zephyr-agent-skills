# Debugging & Profiling on Host

One of the greatest strengths of `native_sim` is the ability to use mature host-side tools.

## Debugging with GDB
Since the output is a standard executable, you can use GDB directly.
```bash
gdb ./build/zephyr/zephyr.exe
(gdb) run
```
You can also use `west debug`, which will automatically find the executable and launch GDB.

## Memory Checking with Valgrind
Catch memory leaks and invalid accesses effortlessly.
```bash
valgrind ./build/zephyr/zephyr.exe
```
*Note: Ensure `CONFIG_NATIVE_SIM_NATIVE_NOT_OPTIMIZED=y` for better stack traces.*

## Profiling with Gprof
Identify bottlenecks in your application logic.
1. Enable `CONFIG_GPROF=y`.
2. Build and run the app.
3. Analyze `gmon.out` using `gprof`.

## PCAP Tracing
If using networking, you can capture simulated packets directly to a PCAP file.
```bash
./build/zephyr/zephyr.exe --pcap=capture.pcap
```
Then open `capture.pcap` in Wireshark.
