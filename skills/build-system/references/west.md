# West Workspace & Manifests

`west` is Zephyr's meta-tool for managing multiple repositories and the build process.

## Essential Workspace Commands
- `west init -m <url> <dir>`: Initialize a new workspace from a manifest repository.
- `west update`: Clone/update all repositories listed in the manifest.
- `west topdir`: Print the absolute path to the workspace root.
- `west manifest --path`: Show the path to the current manifest file.

## Advanced Configuration (from Golioth)
- `west flash --context`: Displays supported runners and the default runner for the built board.
- `west sdk -i`: Interactive SDK and toolchain installation/update.
- `west config manifest.file <filename>`: Switch between multiple manifest files (e.g., `west-zephyr.yml` vs `west-ncs.yml`).
- `west manifest --resolve`: Resolve and print the combined manifest from all imports.
- `west manifest --freeze`: Lock all project revisions to their current commit hashes.

## Manifest Allow-Lists
Use `name-allowlist` to filter modules imported from an upstream manifest (like Zephyr's).

```yaml
manifest:
  projects:
    - name: zephyr
      url: https://github.com/zephyrproject-rtos/zephyr
      revision: v3.7.0
      import:
        name-allowlist:
          - cmsis
          - mbedtls
          - hal_nordic
```

## Custom West Commands
You can define custom west commands in a `scripts/west-commands.yml` file within your repository or a module.
