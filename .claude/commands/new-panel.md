---
description: Create a new Blender UI panel
---

Create a new UI panel with proper registration and layout examples.

**Ask user:**
1. What is the panel name? (e.g., "custom_tools", "modifier_helper")
2. Where should the panel appear?
   - VIEW_3D sidebar (N-panel)
   - VIEW_3D tools (T-panel)
   - Properties Editor (which tab?)
   - Node Editor sidebar
   - Other
3. What tab/category name? (e.g., "My Tools", "Custom")
4. Should it have a poll condition? (e.g., only show for mesh objects)
5. Should it start collapsed? (yes/no)

**Process:**

1. Generate panel class with:
   - Proper `bl_idname` format: `{SPACE}_PT_{panel_name}`
   - `bl_space_type` and `bl_region_type` based on location
   - `bl_category` for sidebar tab name
   - `bl_options` if starting collapsed

2. Include:
   - `poll()` classmethod if conditional display
   - `draw_header()` if icon needed
   - `draw()` with layout examples

3. Add to panels.py file

4. Register in __init__.py classes list

**Panel Locations Reference:**

| Location | bl_space_type | bl_region_type |
|----------|---------------|----------------|
| 3D View Sidebar | VIEW_3D | UI |
| 3D View Tools | VIEW_3D | TOOLS |
| Properties > Object | PROPERTIES | WINDOW |
| Properties > Modifier | PROPERTIES | WINDOW |
| Node Editor | NODE_EDITOR | UI |
| Image Editor | IMAGE_EDITOR | UI |

**Template:**

```python
class {SPACE}_PT_{panel_name}(bpy.types.Panel):
    bl_label = "{Panel Label}"
    bl_idname = "{SPACE}_PT_{panel_name}"
    bl_space_type = '{space_type}'
    bl_region_type = '{region_type}'
    bl_category = "{Tab Name}"
    bl_options = {{'DEFAULT_CLOSED'}}  # Remove if should start open

    @classmethod
    def poll(cls, context):
        # Modify or remove based on requirements
        return context.active_object is not None

    def draw_header(self, context):
        layout = self.layout
        layout.label(icon='TOOL_SETTINGS')

    def draw(self, context):
        layout = self.layout
        obj = context.active_object

        # Column layout example
        col = layout.column(align=True)
        col.label(text="Section Title:")
        col.operator("object.your_operator")

        # Row layout example
        row = layout.row(align=True)
        row.prop(obj, "name")

        # Box example
        box = layout.box()
        box.label(text="Boxed Section")

        # Split example
        split = layout.split(factor=0.4)
        split.label(text="Label:")
        split.prop(obj, "location", text="")
```

**Layout Tips:**
- Use `align=True` for tighter spacing
- Use `box()` to group related controls
- Use `split()` for label-property pairs
- Use `separator()` for visual spacing
