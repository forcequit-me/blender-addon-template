---
description: Add a panel or sub-panel to the add-on using the house layout
argument-hint: "<what the panel holds>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

Add a panel to the add-on. From `$ARGUMENTS` or by asking, get: what goes in it, and whether it is a new section of the existing sidebar panel (usual) or a new top-level panel (rare).

Read `panels.py` and `__init__.py` first and match the existing names and style.

## House rules

- `bl_category` is the add-on's existing plain tab name (`"Addon Name"` in the bare template). Panel labels are plain too.
- Class and idname: `<PREFIX>_PT_<name>`.
- Sections of the main panel are sub-panels: `bl_parent_id = "<PREFIX>_PT_panel"` (use the real main panel idname).
- The links footer `<PREFIX>_PT_links`, when the build has one, must stay last. It has `bl_order = 100`; give new sub-panels a lower `bl_order`.
- Advanced or rarely used options go in a closed Settings section: `bl_options = {'DEFAULT_CLOSED'}`, or the hand-drawn disclosure row in the `blender-ui-patterns` skill.
- Show state as a status label in the panel, not in a tooltip.
- `draw()` only reads. No data writes, no slow scene-wide loops.

## Pattern

```python
class <PREFIX>_PT_settings(bpy.types.Panel):
    bl_label = "Settings"
    bl_idname = "<PREFIX>_PT_settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "<Addon Name>"
    bl_parent_id = "<PREFIX>_PT_panel"
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 10

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.prop(context.scene, "<prop>")
```

## Wire it up

1. Add the class to `panels.py`.
2. Add it to `classes` in `__init__.py`, after its parent.
3. Update the README's "How to use" (`README.md`, or `ADDON_README.md` before `/setup-addon`) so it lists every control in the order the user meets it, with exact labels.
4. Run the smoke test on `BLENDER_MIN` and `BLENDER_LATEST` (`/test-addon`).

Consider asking the `ui-designer` agent to review the result.
