---
name: blender-version-targeting
description: How this template targets one minimum Blender version (5.0 by default) with no compat layer, and how it ships both as a legacy zip and on extensions.blender.org. Use when setting bl_info "blender" or the manifest's blender_version_min, when unsure whether an API exists in the minimum version, when tempted to add a version check or compat.py, when testing on BLENDER_MIN and BLENDER_LATEST, or when a question comes up about legacy install versus the extensions platform.
---

# Blender version targeting

One minimum, no branches. The template targets **Blender 5.0 and newer** by default. To pick another minimum, change bl_info `"blender"`, the manifest `blender_version_min`, the guard in `register()` and `BLENDER_MIN` in `CLAUDE.md` together.

`<BLENDER_MIN>` and `<BLENDER_LATEST>` below are the two paths in the "Blender installs" section of `CLAUDE.md`: the oldest Blender you support and the newest you test on.

## Rules

- `bl_info["blender"]` is the true minimum: `(5, 0, 0)`. `blender_version_min` in `blender_manifest.toml` says the same (`"5.0.0"`).
- No `compat.py` of version branches, no `IS_BLENDER_4_x` flags, no `if bpy.app.version < ...` paths. Any branch for a version below the minimum is dead code; delete it.
- A helper module named for an API shape is fine (for example one that wraps the 5.0 compositor, `scene.compositing_node_group` and `NodeGroupOutput`, with no version checks). The line is branching on version, not having helpers.
- The one allowed check is refusing to enable below the minimum. Blender enables a legacy add-on with a newer `bl_info["blender"]` anyway and only shows a warning ("This script was written for Blender version 5.0.0 and might not function", checked in `bl_operators/userpref.py`). So put this at the top of `register()`:

```python
def register():
    if bpy.app.version < (5, 0, 0):
        raise RuntimeError(
            f"Addon Name requires Blender 5.0 or newer (found {bpy.app.version_string})."
        )
    ...
```

  An extensions install checks `blender_version_min` itself and refuses older Blenders; the guard costs nothing there. If the guard reads the minimum from `bl_info`, use `globals().get("bl_info", {})`, because Blender deletes `bl_info` from an extension's module.

- When a newer Blender adds something you want, check for it with feature detection (below), not a version number, and only if the feature is optional. If the add-on needs it, raise the minimum instead.

## Check an API exists before you use it

Run it headless in the oldest supported Blender:

```text
"<BLENDER_MIN>" --background --factory-startup --python-expr "import bpy; print('compositing_node_group' in bpy.types.Scene.bl_rna.properties)"
```

Do the check on `bl_rna`, not with `hasattr` on the class. Verified on 5.0 and 5.2: `hasattr(bpy.types.Object, "location")` is **False**, because RNA properties and functions live on instances. Use:

```python
"location" in bpy.types.Object.bl_rna.properties        # property
"select_set" in bpy.types.Object.bl_rna.functions       # method
[p.identifier for p in bpy.types.WindowManager.bl_rna.functions["invoke_confirm"].parameters]
hasattr(obj, "select_set")                               # on an instance, fine
```

`hasattr(bpy.types.Scene, "my_prop")` does work for properties your add-on registered in Python.

With the Blender MCP connected, `bpy_api_lookup` ("WindowManager.invoke_confirm", "bpy.ops.object.parent_set") and `describe_node_type` answer the same questions against the live build.

## Read enum items, never hardcode them

Enum identifiers change between releases. `file_format` gained `AVIF` in 5.2 and 5.0 does not have it. Read the list:

```python
items = bpy.types.ImageFormatSettings.bl_rna.properties["file_format"].enum_items
formats = [i.identifier for i in items]
```

`scene.render.engine` is the exception: RNA only lists `BLENDER_EEVEE` even though Cycles and Workbench are valid. Read the current value, which is always valid. To switch engines, assign inside `try/except TypeError`; the error lists every accepted identifier. In 5.x EEVEE is `BLENDER_EEVEE` (the 4.2 to 4.5 `BLENDER_EEVEE_NEXT` name is gone).

## Known removals that still show up in old code

| Old | 5.0+ |
| --- | --- |
| `import bgl` | gone, use `gpu` and `gpu_extras` |
| `mesh.use_auto_smooth`, `auto_smooth_angle` | gone, use `mesh.set_sharp_from_angle()` or a Smooth by Angle modifier |
| `node_tree.inputs.new(...)` on groups | `node_tree.interface.new_socket(name=, in_out=, socket_type=)` |
| `scene.node_tree` (compositor) | `scene.compositing_node_group`, output is `NodeGroupOutput` |
| `bpy.ops.x(override_dict, ...)` | `with context.temp_override(...):` |
| `CompositorNodeMixRGB` | not in 5.0 or 5.2; check `hasattr(bpy.types, "CompositorNodeX")` before `nodes.new` |
| `BLENDER_EEVEE_NEXT` (4.2 to 4.5) | `BLENDER_EEVEE` |

For each release, read the Python API notes: https://developer.blender.org/docs/release_notes/5.0/python_api/ (swap 5.1, 5.2).

## Test on BLENDER_MIN and BLENDER_LATEST

The two bracket the supported range. From the repo root:

```text
"<BLENDER_MIN>" --background --factory-startup --python tests/test_blender_smoke.py
"<BLENDER_LATEST>" --background --factory-startup --python tests/test_blender_smoke.py
```

Both must print `SMOKE OK`. `--factory-startup` stops a copy of the add-on installed in your own Blender from shadowing the repo copy. Undo and anything drawn in a window cannot be tested headless.

## Legacy zip and extensions platform

The template builds both:

| | Legacy zip | Extensions platform |
| --- | --- | --- |
| Build | `python build.py package --clean` | `python build.py package --extension --clean` (runs `blender --command extension build`) |
| Install | Edit > Preferences > Add-ons > arrow menu > Install from Disk | Edit > Preferences > Get Extensions, or drag the zip into Blender |
| Metadata Blender reads | `bl_info` | `blender_manifest.toml` (bl_info is ignored and removed from the module) |
| Module name | `addon_name` | `bl_ext.<repo>.addon_name` |
| Links footer | allowed | not allowed (rule 6.1) |

Both read the same package, so keep `bl_info` and the manifest in step: `name`, `version`, and `blender` against `blender_version_min`. The smoke test asserts it, and `python build.py version X.Y.Z` sets both versions. Check a manifest with `"<BLENDER_LATEST>" --command extension validate addon_name` (it rejects, for example, a `tagline` over 64 characters or one ending in punctuation; checked on 5.0).

Rules of extensions.blender.org that shape the code (terms: https://extensions.blender.org/terms-of-service/):

- **6.1, no advertising in the UI.** No links to commercial or funding sites, donation buttons or anything prompting a purchase inside Blender. The links footer has to go from an extensions build (`blender-ui-patterns`). The website and bug report link can go in the manifest (`website`) and the listing page instead.
- **3.9, no tampering.** Do not modify the operating system, third-party software, other extensions or add-ons, or Blender's internal modules. That rules out, for example, registering file associations, reordering other add-ons' header buttons, or patching Blender's own classes.

Other extension requirements worth knowing before you choose:

- Relative imports only (`from . import x`): the package lives under `bl_ext.<repo>`.
- Look the add-on up with `__package__`, never a hardcoded `"addon_name"` (preferences, `extension_path_user`).
- Write user data to `bpy.utils.extension_path_user(__package__, create=True)`, not into the add-on's own folder.
- Declare what it needs in the manifest `[permissions]` (`files`, `network`, `clipboard`, `camera`, `microphone`) with a short reason each, and check `bpy.app.online_access` before any network access.
- Third-party Python packages ship as bundled wheels listed in the manifest; never `pip install` at run time.

If you ship only the legacy zip, none of the platform rules bind you. Keep the package name fixed either way: installed copies keep their preferences under it.
