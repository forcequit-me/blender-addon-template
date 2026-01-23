# Blender UI/UX Patterns

Expert knowledge for creating effective Blender user interfaces.

## When to Use This Skill
- Creating panels for the sidebar
- Designing operator interfaces
- Building custom property editors
- Implementing UILists
- Following Blender UI conventions

## Layout Types

### Column Layout
```python
def draw(self, context):
    layout = self.layout

    # Basic column
    col = layout.column()
    col.prop(obj, "location")
    col.prop(obj, "rotation_euler")

    # Aligned column (tighter spacing)
    col = layout.column(align=True)
    col.prop(obj, "scale", index=0, text="X")
    col.prop(obj, "scale", index=1, text="Y")
    col.prop(obj, "scale", index=2, text="Z")
```

### Row Layout
```python
def draw(self, context):
    layout = self.layout

    # Basic row
    row = layout.row()
    row.prop(obj, "hide_viewport")
    row.prop(obj, "hide_render")

    # Aligned row (buttons touching)
    row = layout.row(align=True)
    row.operator("object.select_all", text="All").action = 'SELECT'
    row.operator("object.select_all", text="None").action = 'DESELECT'
    row.operator("object.select_all", text="Invert").action = 'INVERT'
```

### Box Layout
```python
def draw(self, context):
    layout = self.layout

    # Framed section
    box = layout.box()
    box.label(text="Transform", icon='OBJECT_ORIGIN')

    col = box.column(align=True)
    col.prop(obj, "location")
    col.prop(obj, "rotation_euler")
    col.prop(obj, "scale")
```

### Split Layout
```python
def draw(self, context):
    layout = self.layout

    # Proportional split
    split = layout.split(factor=0.3)
    split.label(text="Name:")
    split.prop(obj, "name", text="")

    # Multiple columns
    split = layout.split(factor=0.5)
    col1 = split.column()
    col2 = split.column()
    col1.prop(obj, "location")
    col2.prop(obj, "scale")
```

### Grid Flow
```python
def draw(self, context):
    layout = self.layout

    # Even grid
    grid = layout.grid_flow(columns=3, even_columns=True, align=True)
    for i in range(9):
        grid.operator("mesh.primitive_cube_add", text=str(i+1))

    # Auto columns based on width
    grid = layout.grid_flow(columns=0, even_columns=True)
    # Blender determines column count
```

## Property Widgets

### Standard Properties
```python
def draw(self, context):
    layout = self.layout
    props = context.scene.my_props

    # Label + widget
    layout.prop(props, "my_float")

    # No label
    layout.prop(props, "my_float", text="")

    # Custom label
    layout.prop(props, "my_float", text="Custom Label")

    # With icon
    layout.prop(props, "my_bool", icon='CHECKBOX_HLT')

    # Icon only (for toggles)
    layout.prop(props, "my_bool", icon_only=True)
```

### Enum Properties
```python
def draw(self, context):
    layout = self.layout
    props = context.scene.my_props

    # Dropdown
    layout.prop(props, "my_enum")

    # Expanded (radio buttons)
    layout.prop(props, "my_enum", expand=True)

    # Icon menu
    layout.prop_menu_enum(props, "my_enum")
```

### Vector Properties
```python
def draw(self, context):
    layout = self.layout
    obj = context.active_object

    # Full vector
    layout.prop(obj, "location")

    # Single component
    layout.prop(obj, "location", index=0, text="X")

    # As slider
    layout.prop(obj, "scale", slider=True)
```

### Search/Pointer Properties
```python
def draw(self, context):
    layout = self.layout
    props = context.scene.my_props

    # Object search
    layout.prop_search(props, "target_object", bpy.data, "objects")

    # Material search
    layout.prop_search(props, "target_material", bpy.data, "materials")

    # Collection search
    layout.prop_search(props, "target_collection", bpy.data, "collections")

    # Vertex group search (on active object)
    if context.active_object:
        layout.prop_search(props, "vertex_group",
                          context.active_object, "vertex_groups")
```

## Icons

### Using Icons
```python
def draw(self, context):
    layout = self.layout

    # Label with icon
    layout.label(text="My Label", icon='MESH_CUBE')

    # Operator with icon
    layout.operator("mesh.primitive_cube_add", icon='MESH_CUBE')

    # Icon button only
    layout.operator("mesh.primitive_cube_add", text="", icon='MESH_CUBE')

    # Row of icon buttons
    row = layout.row(align=True)
    row.operator("object.select_all", text="", icon='CHECKBOX_HLT').action = 'SELECT'
    row.operator("object.select_all", text="", icon='CHECKBOX_DEHLT').action = 'DESELECT'
```

### Common Icons
```
Object types: MESH_CUBE, MESH_UVSPHERE, MESH_CYLINDER, CURVE_DATA, EMPTY_DATA
UI: ADD, REMOVE, TRIA_DOWN, TRIA_RIGHT, CHECKBOX_HLT, CHECKBOX_DEHLT
Actions: PLAY, PAUSE, REW, FF, PREVIEW_RANGE
File: FILE, FILE_FOLDER, FILE_NEW, FILE_BLEND
Tools: TOOL_SETTINGS, MODIFIER, CONSTRAINT, SHADERFX
Status: ERROR, INFO, QUESTION, CANCEL, CHECKMARK
```

### Find Icons
```python
# In Blender Python console:
import bpy.types
icons = [attr for attr in dir(bpy.types.UILayout.bl_rna)
         if attr.startswith('icon_')]

# Or use Edit > Preferences > Interface > Developer Extras
# Then access icon viewer in any icon field
```

## Panel Organization

### Subpanels
```python
class VIEW3D_PT_main_panel(bpy.types.Panel):
    bl_label = "Main Panel"
    bl_idname = "VIEW3D_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "My Tab"

    def draw(self, context):
        self.layout.label(text="Main content")

class VIEW3D_PT_sub_panel(bpy.types.Panel):
    bl_label = "Sub Panel"
    bl_idname = "VIEW3D_PT_sub_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "My Tab"
    bl_parent_id = "VIEW3D_PT_main_panel"  # Makes this a subpanel
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        self.layout.label(text="Sub content")
```

### Panel Header
```python
class VIEW3D_PT_with_header(bpy.types.Panel):
    bl_label = "My Panel"
    # ...

    def draw_header(self, context):
        layout = self.layout
        props = context.scene.my_props

        # Toggle in header
        layout.prop(props, "enabled", text="")

    def draw(self, context):
        layout = self.layout
        props = context.scene.my_props

        # Disable panel content based on toggle
        layout.enabled = props.enabled
        layout.prop(props, "my_value")
```

### Conditional Panels
```python
class VIEW3D_PT_conditional(bpy.types.Panel):
    bl_label = "Mesh Only Panel"
    # ...

    @classmethod
    def poll(cls, context):
        # Only show for mesh objects
        return (context.active_object is not None and
                context.active_object.type == 'MESH')

    def draw(self, context):
        # ...
```

## Operator Invocation from UI

### Basic Operator Button
```python
def draw(self, context):
    layout = self.layout

    # Simple button
    layout.operator("mesh.primitive_cube_add")

    # With custom text
    layout.operator("mesh.primitive_cube_add", text="Add Box")

    # With icon
    layout.operator("mesh.primitive_cube_add", text="Add Box", icon='MESH_CUBE')
```

### Operator with Properties
```python
def draw(self, context):
    layout = self.layout

    # Set operator properties
    op = layout.operator("transform.translate")
    op.value = (1, 0, 0)

    # Multiple properties
    op = layout.operator("mesh.primitive_cube_add")
    op.size = 2.0
    op.location = (0, 0, 1)
```

### Operator Menu
```python
def draw(self, context):
    layout = self.layout

    # Dropdown menu of operators
    layout.operator_menu_enum("object.modifier_add", "type")

    # Custom menu
    layout.menu("VIEW3D_MT_my_menu")
```

## Custom Property Drawing

### UIList
```python
class MY_UL_items(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            row.prop(item, "name", text="", emboss=False)
            row.prop(item, "enabled", text="")
        elif self.layout_type == 'GRID':
            layout.label(text=item.name, icon='OBJECT_DATA')

# Usage in panel
def draw(self, context):
    layout = self.layout
    props = context.scene.my_props

    row = layout.row()
    row.template_list("MY_UL_items", "", props, "items", props, "active_index")

    col = row.column(align=True)
    col.operator("my.add_item", icon='ADD', text="")
    col.operator("my.remove_item", icon='REMOVE', text="")
```

### Popover
```python
class MY_PT_popover(bpy.types.Panel):
    bl_label = "Popover Content"
    bl_idname = "MY_PT_popover"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'  # Important for popovers

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene.my_props, "my_value")

# Usage
def draw(self, context):
    layout = self.layout
    layout.popover("MY_PT_popover", text="Settings")
```

## Visual Hierarchy

### Separator and Spacing
```python
def draw(self, context):
    layout = self.layout

    layout.label(text="Section 1")
    layout.prop(obj, "location")

    layout.separator()  # Visual gap

    layout.label(text="Section 2")
    layout.prop(obj, "rotation_euler")

    layout.separator(factor=2.0)  # Larger gap
```

### Enabled/Active States
```python
def draw(self, context):
    layout = self.layout
    props = context.scene.my_props

    # Disable entire section
    col = layout.column()
    col.enabled = props.section_enabled
    col.prop(props, "value1")
    col.prop(props, "value2")

    # Gray out (but still clickable)
    row = layout.row()
    row.active = props.is_active
    row.prop(props, "value3")
```

### Alert State
```python
def draw(self, context):
    layout = self.layout

    # Warning/alert styling
    row = layout.row()
    row.alert = True
    row.label(text="Warning!", icon='ERROR')
```

## Best Practices

### Consistency with Blender UI
- Follow existing panel patterns in Blender
- Use standard icons for common actions
- Match layout density to similar panels
- Use familiar terminology

### User Experience
- Group related controls together
- Show only relevant options
- Provide sensible defaults
- Use appropriate widget for data type

### Performance
- Avoid heavy computation in draw()
- Don't modify data in draw()
- Cache expensive lookups

## Resources
- UI Layout: https://docs.blender.org/api/current/bpy.types.UILayout.html
- Panel: https://docs.blender.org/api/current/bpy.types.Panel.html
- UIList: https://docs.blender.org/api/current/bpy.types.UIList.html
