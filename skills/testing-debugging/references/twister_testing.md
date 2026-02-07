# Twister Test Runner

Twister is the automation tool that scans for tests, builds them for multiple platforms, and executes them (either in simulation or on real hardware).

## Core Concepts
- **`testcase.yaml`**: Defines how Twister should discover and build your tests.
- **Scenarios**: Specific configurations of a test (e.g., building with different Kconfigs).
- **HIL (Hardware-In-The-Loop)**: Running tests on physical boards connected to the host.

## Basic Usage
Run Twister from the root of your Zephyr workspace:

```bash
./scripts/twister -p native_sim -s samples/basic/blinky
```

## Test Metadata (`testcase.yaml`)
Each test directory requires a `.yaml` file to describe it to Twister.

```yaml
tests:
  my_feature.logic:
    tags: kernel drivers
    platform_allow: native_sim reel_board
    harness: ztest
  my_feature.performance:
    extra_configs:
      - CONFIG_SPEED_OPTIMIZED=y
```

## Advanced Twister Patterns

### 1. Filtering
Run only specific tags or platforms to save time.
```bash
twister -p native_sim -t drivers
```

### 2. HIL Testing
Twister can flash physical boards if they are connected and defined in a hardware map.
```bash
twister --device-testing --hardware-map device_map.yaml
```

### 3. Reporting
Twister generates comprehensive reports in XML and JSON formats, ideal for CI/CD integration.
- `twister-out/twister.json`: Summary of all tests.
- `twister-out/testplan.json`: Detailed report of build/run status.

### 4. CI/CD Integration (GitHub Actions)
```yaml
- name: Run Twister Tests
  run: |
    ./scripts/twister -p native_sim --inline-logs
    
- name: Upload Test Results
  uses: actions/upload-artifact@v3
  with:
    name: twister-results
    path: twister-out/twister.json
```

## Professional Insight
Use the **test quarantine** feature for flaky tests in large repositories. Mark unstable tests in a `quarantine.yaml` file to prevent them from breaking the entire CI pipeline while they are being investigated.
