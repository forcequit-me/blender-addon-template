---
name: blender-api-patterns
description: Core bpy patterns for Blender 5.0+ - context versus data, operator structure (poll, invoke, execute, report, UNDO), properties and update callbacks, context overrides, saving and restoring selection, removing data, and the API traps that crash or misbehave. Use when writing or reviewing any bpy code.
---

# Blender API patterns (5.0+)

Reference: https://docs.blender.org/api/current/ and the gotchas page https://docs.blender.org/api/current/info_gotcha.html

## Context versus data

- `context` is what the user is looking at: `context.scene`, `context.view_layer`, `context.active_object`, `context.selected_objects`, `context.mode`. Take it from the `context` argument, not `bpy.context`, inside operators, panels and callbacks.
- `bpy.data` is everything in the file. `bpy.data.objects.get(name)` returns `None`; `bpy.data.objects[name]` raises `KeyError`.
- Prefer direct data access over `bpy.ops`. Operators depend on context, selection and mode, add undo steps and are slow in loops. `obj.modifiers.new("Subdivision", 'SUBSURF')`, not `bpy.ops.object.modifier_add`.
- Use `bpy.ops` when Blender's operator does real work you would otherwise re-implement (for example `object.parent_set` and its parent types). Save and restore the selection around it.

## Operator

```python
class ADDON_NAME_OT_delete_empties(bpy.types.Operator):
    """Delete every empty of the ticked types in the whole file, skipping the exclude list"""
    bl_idname = "addon_name.delete_empties"
    bl_label = "Delete Empties"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def execute(self, context):
        props = context.scene.addon_name
        doomed = [o for o in bpy.data.objects if o.type == 'EMPTY' and wanted(o, props)]
        if not doomed:
            self.report({'WARNING'}, "No empties of the ticked types")
            return {'CANCELLED'}
        bpy.data.batch_remove(doomed)
        self.report({'INFO'}, f"Removed {len(doomed)} empties")
        return {'FINISHED'}
```

- `{'UNDO'}` on every operator that changes file data. `'REGISTER'` adds it to the redo panel and the Info log. `'INTERNAL'` hides it from F3 search (for row buttons and menu entries).
- Return `{'CANCELLED'}` when nothing changed, so no empty undo step is pushed.
- `poll()` is cheap and never reports; it greys the button. Use it for mode and object type. Use a `WARNING` report in `execute` for "nothing to do".
- Row buttons pass which item via an `IntProperty` (`op.index = index`); keep that property out of saved presets with `options={'SKIP_SAVE'}` where it matters.
- Confirm dialogs and previews: `blender-ui-patterns`.
- `__init__` on an operator must take and pass arguments, or it fails in 5.0 with `TypeError: __init__() takes 1 positional argument but 2 were given` (checked). Usually you do not need one: set state in `invoke`.

```python
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._timer = None
```

## Properties

```python
class ADDON_NAME_Properties(bpy.types.PropertyGroup):
    show_settings: bpy.props.BoolProperty(name="Settings", default=False,
        description="Show the settings that change what Delete Empties removes")
    mode: bpy.props.EnumProperty(name="Mode", items=(
        ('SELECTED', "Selected", "Only the selected objects"),
        ('ALL', "All", "Every object in the scene"),
    ), default='SELECTED')
    target: bpy.props.PointerProperty(type=bpy.types.Object,
        poll=lambda self, obj: obj.type == 'EMPTY')
```

- References to objects, collections, materials: `PointerProperty`, never a name string (`addon-architecture`).
- Paths: `StringProperty(subtype='DIR_PATH')` or `'FILE_PATH'`; a render output path also takes `options={'OUTPUT_PATH'}` to behave like Blender's own output field.
- Dynamic enum `items=callback`: keep the returned strings alive in a module-level list, or Blender shows garbage labels.
- Get/set accessors let a scene value fall back to a preference default until the user sets it.

### Update callbacks

```python
_suppress = False

def _on_name_change(self, context):
    global _suppress
    if _suppress:
        return
    _suppress = True
    try:
        self.name = unique_name(self.name)   # writing back would re-enter without the guard
    finally:
        _suppress = False
```

- Update callbacks run on every change, including your own code setting the property. Guard with a module flag when code writes the value.
- They run outside the operator system: no undo step of their own. Keep them small.
- `context` can be incomplete; do not assume `context.area`.

## Context override

```python
with context.temp_override(area=area, region=region, space_data=area.spaces.active):
    bpy.ops.outliner.item_activate()
```

The old dict-as-first-argument override is gone. Reading Outliner selection (`context.selected_ids`) needs an override to an Outliner area.

## Save and restore selection around operators

```python
active = context.view_layer.objects.active
selected = list(context.selected_objects)
try:
    for o in context.selected_objects:
        o.select_set(False)
    ...                                        # bpy.ops call on a chosen selection
finally:
    for o in selected:
        if o.name in context.view_layer.objects:
            o.select_set(True)
    context.view_layer.objects.active = active
```

## Removing data

- `bpy.data.objects.remove(obj, do_unlink=True)` for one; `bpy.data.batch_remove(ids)` for many (much faster).
- After removal the Python object is dead. Touching it raises `ReferenceError`. Read `obj.name` first if you need it for the report.
- Never remove while iterating the same collection: collect first, then remove.
- `bpy.data.orphans_purge(do_local_ids=, do_linked_ids=, do_recursive=)` removes unused data blocks, the same as File > Clean Up.
- `ID.users` counts add-on `PointerProperty` references too.

## Traps

- **Stored Python references go stale** after undo, redo, file load, and adding to some collections (e.g. `mesh.vertices.add`, `collection.add()` can reallocate). Store names or pointers in properties, look objects up again, and catch `ReferenceError`.
- **Never write data in `draw()`** or in a `poll()`.
- **Nodes: find by type, never by name.** Names are translated on non-English UIs. `next(n for n in tree.nodes if n.type == 'BSDF_PRINCIPLED')`.
- **Socket names change between releases.** Look sockets up by identifier or check with `describe_node_type` (MCP) before indexing.
- **`Material.use_nodes` is deprecated** in 5.0 (warning says removal in 6.0). New materials already have a node tree; do not set it.
- **Colours on materials** go on the shader node inputs. `material.diffuse_color` is viewport display only.
- **Enum identifiers:** read them from `bl_rna`, do not hardcode (`blender-version-targeting`).
- **Mode:** mesh data read in Edit Mode is stale until `obj.update_from_editmode()`; many data edits require Object Mode. Check `context.mode` in `poll`.
- **Linked data** is read-only. Check `id.library` (and `id.override_library`) before editing.
- **BMesh:** always `bm.free()` in a `finally`.
- **Paths:** `bpy.path.abspath()` for `//` relative paths; an unsaved file has no `//` base. Never hardcode a user folder: use `bpy.utils.user_resource()` or, for an extension, `bpy.utils.extension_path_user(__package__, create=True)`, which an extension should use instead of writing into its own folder.

## Registration of loose properties

```python
bpy.types.Scene.addon_name = bpy.props.PointerProperty(type=ADDON_NAME_Properties)
...
del bpy.types.Scene.addon_name
```

Full register and unregister order: `addon-architecture`.
