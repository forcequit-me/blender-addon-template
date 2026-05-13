# Blender 4.2+ Extension Migration Guide

Blender 4.2 introduced the **Extensions Platform** as the long-term replacement for legacy `bl_info`-based addons. This template ships in **dual-mode**: the same source tree can be packaged as a legacy addon (3.6–4.1) AND as a 4.2+ extension.

## TL;DR

| Target Blender | Install path | Manifest | Install UI |
|----------------|--------------|----------|------------|
| 3.6 LTS – 4.1 | Edit → Preferences → Add-ons → Install | `bl_info` in `__init__.py` | Add-ons |
| 4.2+ | Edit → Preferences → Get Extensions → Install from Disk | `blender_manifest.toml` | Extensions |

Both zips have the same Python tree. Only the metadata differs.

## How dual-mode works

- `addon_name/__init__.py` keeps `bl_info` — Blender 3.6–4.1 reads this.
- `addon_name/blender_manifest.toml` is the 4.2+ manifest — Blender ignores `bl_info` when this file is present and treats the package as an extension.
- Blender 4.2 still loads legacy addons (without manifest) via its built-in compatibility layer, so a legacy zip works there too.

## Keeping `bl_info` and `blender_manifest.toml` in sync

When you change one, change the other. Fields that must match:

| `bl_info` | `blender_manifest.toml` |
|-----------|-------------------------|
| `name` | `name` |
| `version` tuple `(1,0,0)` | `version = "1.0.0"` string |
| `blender` minimum tuple | `blender_version_min` string |
| `description` | `tagline` |
| `author` | `maintainer` |

`build.py package --extension` validates this mapping before zipping.

## Permissions (extension-only)

Extensions must declare permissions in the manifest. Legacy addons have no equivalent. Add only what you use:

```toml
[permissions]
files = "Read/write user-selected files"
network = "Fetch remote textures"
clipboard = "Read clipboard for paste operator"
camera = "Capture from webcam"
microphone = "Record audio"
```

Omitted permissions become hard-denied in 4.2+.

## License (extension-only, required)

`license` is mandatory and must be an SPDX identifier:

```toml
license = ["SPDX:GPL-3.0-or-later"]
```

Legacy `bl_info` has no license field; the project README/LICENSE serves that role.

## Building both packages

```bash
python build.py package              # legacy zip (bl_info)
python build.py package --extension  # extension zip (manifest only)
python build.py package --both       # both, side by side in build/
```

## When to use which

- **Legacy zip only**: targeting 3.6 LTS or 4.0/4.1 users primarily.
- **Extension only**: targeting 4.2+ exclusively and submitting to extensions.blender.org.
- **Both**: distributing on GitHub releases or your own site with broad Blender support — recommended default.

## Submitting to extensions.blender.org

1. Build extension zip: `python build.py package --extension`
2. Test install: Edit → Preferences → Get Extensions → Install from Disk
3. Validate with Blender's `extension validate` CLI (Blender 4.2+):
   ```
   blender --command extension validate build/addon_name-v1.0.0-extension.zip
   ```
4. Submit at https://extensions.blender.org/

## References

- Extension specification: https://docs.blender.org/manual/en/latest/advanced/extensions/getting_started.html
- Manifest reference: https://docs.blender.org/manual/en/latest/advanced/extensions/addons.html
- Migrating legacy addons: https://developer.blender.org/docs/release_notes/4.2/python_api/
