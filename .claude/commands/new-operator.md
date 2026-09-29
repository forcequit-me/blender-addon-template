---
description: Add an operator to the add-on using the house patterns
argument-hint: "<what the operator does>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

Add an operator to the add-on. From `$ARGUMENTS` or by asking, get: what the button does, and where it goes in the panel.

Read the package's `__init__.py`, `operators.py` and `panels.py` first and copy their style: the class prefix (`ADDON_NAME_` in the bare template), the idname prefix (the package name), and how existing operators poll and report. If the template's `example` operator is still there and this is the first real feature, ask whether to replace it.

## Pattern

```python
class <PREFIX>_OT_<name>(bpy.types.Operator):
    bl_idname = "wm.<package>_<name>"  # wm. so right-click > Assign Shortcut shows up
    bl_label = "<Short Verb Phrase>"
    bl_description = "<One line: what happens when you click>"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def execute(self, context):
        targets = [o for o in context.selected_objects if o.type == 'MESH']
        if not targets:
            self.report({'WARNING'}, "No mesh objects selected")
            return {'CANCELLED'}
        for obj in targets:
            ...
        self.report({'INFO'}, f"Did X to {len(targets)} objects")
        return {'FINISHED'}
```

- `{'REGISTER', 'UNDO'}` when it changes scene data. Leave `UNDO` off when it does not (opening a URL or folder, toggling UI state).
- Report what it did, with a count. Nothing to do: `WARNING` plus `{'CANCELLED'}`.
- Add `invoke` with `context.window_manager.invoke_confirm(self, event)` only if the action cannot be undone.
- Use the data API, not `bpy.ops`, inside loops. No broad try/except around the body.
- `bl_description` follows `docs/README Spec.md`: plain, second person, no em dashes, true to the code.

## Wire it up

1. Add the class to `operators.py` (or the module the add-on uses for operators).
2. Add it to the `classes` tuple in `__init__.py`.
3. Add the button to the panel where it belongs, above the links sub-panel. Rarely used? Put it in the Settings section (see `/new-panel`).
4. Add the idname to `OPERATORS` in `tests/test_blender_smoke.py`.
5. Add the button to the README's "How to use" (`README.md`, or `ADDON_README.md` before `/setup-addon`), in panel order, with the exact label.
6. Run the smoke test on `BLENDER_MIN` and `BLENDER_LATEST` (`/test-addon`).

Remind the user to check Ctrl+Z on it in a real Blender window.
