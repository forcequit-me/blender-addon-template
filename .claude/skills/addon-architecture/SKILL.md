---
name: addon-architecture
description: This template's layout and lifecycle for a Blender add-on - package files, bl_info and blender_manifest.toml, class tuple and registration order, AddonPreferences, the links footer sub-panel, handlers, keymaps, deferring bpy.data work out of register(), and storing references as PointerProperty with a migration for old name-only data. Use when adding a module, touching register()/unregister(), storing settings or object references, or debugging enable/disable errors.
---

# Add-on architecture

## Folder

```text
<repo>/
├── addon_name/             the package that gets installed; never rename it once shipped
│   ├── __init__.py         bl_info, class tuple, register(), unregister(). Nothing else
│   ├── blender_manifest.toml   extensions metadata; mirrors bl_info
│   ├── operators.py
│   ├── panels.py           main panel, UIList, links sub-panel, WEBSITE_URL, BUG_REPORT_URL
│   ├── properties.py       PropertyGroups and their registration on Scene / WindowManager
│   ├── preferences.py      AddonPreferences, pref() helper
│   ├── constants.py        enum item lists, defaults      (when needed)
│   ├── utils.py            shared logic, no bpy.types classes (when needed)
│   ├── handlers.py         app handlers and timers        (when needed)
│   └── keymaps.py          keymap items                   (when needed)
├── build.py                python build.py package [--extension] [--clean]
├── README.md
├── docs/README Spec.md
└── tests/test_blender_smoke.py
```

Never rename a shipped package: installed copies keep their preferences under it. No `compat.py` of version branches (see `blender-version-targeting`). When one file grows past a few hundred lines, turn it into a package (`operators/presets.py`, `operators/render.py`, `operators/__init__.py` exporting `classes`).

## bl_info and the manifest

```python
bl_info = {
    "name": "Addon Name",
    "author": "Your Name",
    "version": (0, 1, 0),
    "blender": (5, 0, 0),
    "location": "View3D > Sidebar > Addon Name",
    "description": "One sentence saying what the add-on does for you",
    "category": "Object",
}
```

A legacy install reads `bl_info`; an extensions install reads `blender_manifest.toml` and ignores `bl_info`. Keep them in step: manifest `name`, `version` and `blender_version_min` match bl_info `name`, `version` and `blender`. The smoke test asserts this. The manifest `tagline` is the short form of `description`: at most 64 characters and no punctuation at the end (the validator rejects both, checked on 5.0). `python build.py version X.Y.Z` sets both versions at once.

Blender deletes `bl_info` from an extension's module when it loads it (checked on 5.0: `hasattr(module, "bl_info")` is False). Code that reads it at run time, such as the version guard in `register()`, must use `globals().get("bl_info", {})`, never `bl_info[...]` directly.

The legacy zip name is built from `name` and `version`. `description` is one user-facing sentence (`addon-writing`).

## Registration

One explicit tuple, in dependency order. Blender resolves `PointerProperty(type=X)` and `CollectionProperty(type=X)` at register time, so X must already be registered.

```python
import bpy

from . import handlers, operators, panels, preferences, properties

classes = (
    properties.ADDON_NAME_ExcludeItem,     # item types before the groups that hold them
    properties.ADDON_NAME_Properties,
    preferences.ADDON_NAME_AddonPreferences,
    *operators.classes,
    panels.ADDON_NAME_UL_exclude_list,
    panels.ADDON_NAME_PT_panel,            # parent panel before its sub-panels
    panels.ADDON_NAME_PT_links,
)


def register():
    minimum = globals().get("bl_info", {}).get("blender", (0, 0, 0))
    if bpy.app.version < minimum:
        raise RuntimeError(f"Addon Name requires Blender {minimum} or newer (found {bpy.app.version_string}).")
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.addon_name = bpy.props.PointerProperty(type=properties.ADDON_NAME_Properties)
    handlers.register_handlers()           # handlers, header/menu appends, keymaps, timers last


def unregister():
    handlers.unregister_handlers()         # exact reverse
    del bpy.types.Scene.addon_name
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
```

Rules:

- Class names follow `PREFIX_OT_name`, `PREFIX_PT_name`, `PREFIX_UL_name`, `PREFIX_MT_name`. `bl_idname` of an operator is `prefix.name`, lower case.
- Prefer one `PointerProperty` to a PropertyGroup (`scene.addon_name.x`) over many loose `Scene.addon_name_x` properties. If a shipped add-on already uses loose ones, do not rewrite them: saved files hold those names.
- `unregister()` must not raise before `unregister_class` runs, or the add-on cannot be re-enabled without restarting Blender. Guard every removal (`if fn in list`, `if bpy.app.timers.is_registered(fn)`, `try: header.remove(fn) except ValueError`).
- Module globals survive disable and enable because the module stays in `sys.modules`. Reset caches and flags in `unregister()`.
- Stop anything that can call back into the module first: running timers, modal batches, handlers.
- Use relative imports (`from . import x`) only. An extensions install imports the package as `bl_ext.<repo>.addon_name`, so an absolute `import addon_name` breaks there.

## Never touch bpy.data or the scene inside register()

During `register()`, `bpy.data` is a restricted stand-in: `bpy.data.scenes` raises `AttributeError` (`_RestrictData`), checked on 5.0 and 5.2. `bpy.context` is limited too. Defer first-time setup to the first event-loop tick:

```python
def _init_existing_scenes():
    for scene in bpy.data.scenes:
        init_scene(scene)
    return None                            # None = run once

def register_handlers():
    bpy.app.handlers.load_post.append(on_load)
    bpy.app.timers.register(_init_existing_scenes, first_interval=0)
```

The user keyconfig and add-on preferences may also be incomplete at start-up. Build a keymap that depends on preferences from a `first_interval=0` timer for that reason.

## Preferences

```python
class ADDON_NAME_AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__                # the package name, whichever way it was installed

    show_in_header: bpy.props.BoolProperty(
        name="Show in 3D View Header",
        description="Show the Addon Name button in the 3D Viewport header",
        default=True,
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "show_in_header")
        panels.draw_links(layout)          # the links row; draws nothing while the URLs are empty


def pref(name, default=None):
    """One preference value, or default when preferences are not available yet."""
    try:
        return getattr(bpy.context.preferences.addons[__package__].preferences, name)
    except (KeyError, AttributeError):
        return default
```

Always read preferences through a guarded helper keyed on `__package__`, never a hardcoded `"addon_name"`: an extensions install lives under `bl_ext.<repo>.addon_name`. `preferences.addons[__package__]` raises `KeyError` inside `register()` when the add-on is enabled from a script without `default_set=True` (checked), and during start-up ordering. This template gives every add-on an `AddonPreferences` class, even one with no settings, so the links row appears in its preferences.

Where state lives:

- `AddonPreferences`: global, per user. Defaults for new scenes, where the UI shows.
- `Scene` (through a PropertyGroup): saved in the .blend, per scene. The user's working choices.
- `WindowManager`: not saved, reset on file load. Session state such as a list mirrored from disk.

To start new scenes from preference defaults, copy the preferences into the scene once per scene (keyed on `scene.as_pointer()`) from `load_post`, from a `depsgraph_update_post` backstop (Blender has no scene-created handler), and from the first-tick timer.

## References: PointerProperty, not names

Store objects and collections as pointers so they survive renames:

```python
class ADDON_NAME_ExcludeItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()           # kept for old files and the "Missing:" label
    is_collection: bpy.props.BoolProperty()
    object: bpy.props.PointerProperty(type=bpy.types.Object)
    collection: bpy.props.PointerProperty(type=bpy.types.Collection)
```

Files saved before the pointer existed carry only `name`. Fill the pointer in on load, and fall back to the name until then:

```python
from bpy.app.handlers import persistent

def migrate_excludes(scene):
    for item in scene.addon_name.excludes:
        if item.is_collection and item.collection is None:
            item.collection = bpy.data.collections.get(item.name)
        elif not item.is_collection and item.object is None:
            item.object = bpy.data.objects.get(item.name)

@persistent
def on_load(_filepath):
    for scene in bpy.data.scenes:
        migrate_excludes(scene)
```

A pointer to a deleted ID reads `None`: draw it as `Missing: <name>` rather than dropping the row. A `PointerProperty` to an ID adds a user (checked: `users` goes 1 to 2), so a listed object never counts as orphan data. Keep that in mind in anything that counts users.

## Handlers

- Decorate with `@persistent` or Blender drops the handler on file load.
- Append only if not already present, remove only if present. `Script > Reload` and double `register()` otherwise stack duplicates.
- Handlers flag work; they do not do heavy work. `depsgraph_update_post` fires on every change.
- Never write to properties from `draw()`. Backfills and migrations go in `load_post`.

## Keymaps

```python
addon_keymaps = []

def register_keymaps():
    kc = bpy.context.window_manager.keyconfigs.addon
    if kc is None:                         # None in --background
        return
    km = kc.keymaps.new(name='Window', space_type='EMPTY')
    kmi = km.keymap_items.new("addon_name.example", type='E', value='PRESS', shift=True, alt=True)
    addon_keymaps.append((km, kmi))

def unregister_keymaps():
    for km, kmi in addon_keymaps:
        try:
            km.keymap_items.remove(kmi)
        except (ReferenceError, RuntimeError):
            pass                           # keyconfig already torn down
    addon_keymaps.clear()
```

Build it from scratch each time (call `unregister_keymaps()` first) when a preference toggles it. Read the user's own bindings from `keyconfigs.user` rather than assuming defaults such as F12.

## Menus and header

`bpy.types.VIEW3D_MT_object.append(draw_fn)` in `register`, `.remove(draw_fn)` in `unregister`. Header draw functions run in enable order. Do not remove and re-append other add-ons' draw functions to fix the order: that touches other add-ons, which the extensions platform forbids (rule 3.9).

## Every add-on also needs

- `tests/test_blender_smoke.py`: enables through `addon_utils.enable(MODULE, default_set=True)`, checks every operator with `bpy.ops.<cat>.<name>.get_rna_type()`, checks bl_info against the manifest, disables, enables again, prints `SMOKE OK`. Keep `OPERATORS` in step with every `bl_idname`.
- `ADDON_FOLDER` in `build.py` set to the package name.
- The links sub-panel and preferences row (`blender-ui-patterns`), for legacy builds only.
- README to the spec (`addon-writing`).
