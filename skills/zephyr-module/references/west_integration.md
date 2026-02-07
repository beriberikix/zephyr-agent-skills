# Integrating Modules with West

To use an out-of-tree module, you must add it to your project's `west.yml` manifest.

## Manifest Entry
```yaml
manifest:
  projects:
    - name: my-module
      url: https://github.com/my-org/my-module
      revision: main
      path: modules/lib/my-module # Suggested path
```

## `west update`
After adding the module to the manifest, run:
```bash
west update
```
Zephyr will automatically detect the `zephyr/module.yml` file and include the module in the next build.

## Checking Module Status
You can verify that your module is recognized by running:
```bash
west build -t list_modules
```
This will display all detected modules and their versions.
