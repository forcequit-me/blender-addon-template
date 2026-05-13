---
name: blender-api-patterns
description: Core Blender Python API (bpy) patterns — context access, data manipulation, operators, panels, properties, update callbacks, modal operators. Use when writing or reviewing any bpy code, especially when avoiding common API pitfalls.
---

# Blender Python API Patterns

Expert knowledge for working with the Blender Python API (bpy).

## When to Use This Skill
- Accessing Blender data and context
- Creating operators, panels, and properties
- Working with update callbacks
- Using modal operators for interaction
- Avoiding common API pitfalls

## Context Access Patterns

### bpy.context - Current State
```python
import bpy

# Active/selected objects
active = bpy.context.active_object
selected = bpy.context.selected_objects

# Current mode
mode = bpy.context.mode  # 'OBJECT', 'EDIT_MESH', etc.

# Current scene and view layer
scene = bpy.context.scene
view_layer = bpy.context.view_layer

# Preferences
prefs = bpy.context.preferences

# Window/screen (for UI operations)
window = bpy.context.window
screen = bpy.context.screen
area = bpy.context.area
```

### bpy.data - All Blend File Data
```python
import bpy

# Access all data of specific type
objects = bpy.data.objects
meshes = bpy.data.meshes
materials = bpy.data.materials
images = bpy.data.images
node_groups = bpy.data.node_groups

# Get specific item by name
obj = bpy.data.objects.get("Cube")  # Returns None if not found
obj = bpy.data.objects["Cube"]  # Raises KeyError if not found

# Create new data
mesh = bpy.data.meshes.new("NewMesh")
material = bpy.data.materials.new("NewMaterial")

# Remove data
bpy.data.objects.remove(obj)
bpy.data.meshes.remove(mesh)
```

### Context Override (Temporary Context)
```python
import bpy

# Override context for specific operations
override = bpy.context.copy()
override['selected_objects'] = [obj1, obj2]
override['active_object'] = obj1

# Blender 3.2+
with bpy.context.temp_override(**override):
    bpy.ops.object.duplicate()

# Legacy (pre-3.2)
# bpy.ops.object.duplicate(override)
```

## Operator Design Patterns

### Standard Operator
```python
class OBJECT_OT_my_operator(bpy.types.Operator):
    """Tooltip shown on hover"""
    bl_idname = "object.my_operator"
    bl_label = "My Operator"
    bl_description = "Detailed description"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        # Main logic
        return {'FINISHED'}
```

### Operator with Properties
```python
class OBJECT_OT_parameterized(bpy.types.Operator):
    bl_idname = "object.parameterized"
    bl_label = "Parameterized Operator"
    bl_options = {'REGISTER', 'UNDO'}

    # Properties shown in operator panel/popup
    amount: bpy.props.FloatProperty(
        name="Amount",
        default=1.0,
        min=0.0,
        max=10.0,
    )

    axis: bpy.props.EnumProperty(
        name="Axis",
        items=[
            ('X', "X", "X axis"),
            ('Y', "Y", "Y axis"),
            ('Z', "Z", "Z axis"),
        ],
        default='Z',
    )

    def invoke(self, context, event):
        # Show properties dialog before executing
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "amount")
        layout.prop(self, "axis")

    def execute(self, context):
        obj = context.active_object
        axis_index = {'X': 0, 'Y': 1, 'Z': 2}[self.axis]
        obj.location[axis_index] += self.amount
        return {'FINISHED'}
```

### Modal Operator
```python
class OBJECT_OT_modal_move(bpy.types.Operator):
    bl_idname = "object.modal_move"
    bl_label = "Modal Move"
    bl_options = {'REGISTER', 'UNDO'}

    def __init__(self):
        self.initial_location = None
        self.initial_mouse = None

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':
            delta = event.mouse_x - self.initial_mouse[0]
            context.active_object.location.x = self.initial_location[0] + delta * 0.01
            return {'RUNNING_MODAL'}

        elif event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            return {'FINISHED'}

        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            context.active_object.location = self.initial_location
            return {'CANCELLED'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        if context.active_object:
            self.initial_location = context.active_object.location.copy()
            self.initial_mouse = (event.mouse_x, event.mouse_y)
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        return {'CANCELLED'}
```

## Property Definition Patterns

### Basic Properties
```python
from bpy.props import (
    IntProperty, FloatProperty, BoolProperty,
    StringProperty, EnumProperty,
    FloatVectorProperty, IntVectorProperty,
    PointerProperty, CollectionProperty,
)

class MyProperties(bpy.types.PropertyGroup):
    # Numeric
    count: IntProperty(name="Count", default=1, min=0, max=100)
    value: FloatProperty(name="Value", default=0.0, precision=3)

    # Boolean
    enabled: BoolProperty(name="Enabled", default=True)

    # String
    name: StringProperty(name="Name", default="", maxlen=64)
    path: StringProperty(name="Path", subtype='FILE_PATH')

    # Enum
    mode: EnumProperty(
        name="Mode",
        items=[
            ('MODE_A', "Mode A", "First mode", 'MESH_CUBE', 0),
            ('MODE_B', "Mode B", "Second mode", 'MESH_UVSPHERE', 1),
        ],
    )

    # Vectors
    location: FloatVectorProperty(name="Location", size=3)
    color: FloatVectorProperty(name="Color", subtype='COLOR', size=4, min=0, max=1)
```

### Collection Properties
```python
class MyItem(bpy.types.PropertyGroup):
    name: StringProperty(name="Name")
    value: FloatProperty(name="Value")

class MySettings(bpy.types.PropertyGroup):
    items: CollectionProperty(type=MyItem)
    active_index: IntProperty()

# Usage
settings = context.scene.my_settings
item = settings.items.add()
item.name = "New Item"
item.value = 1.0

# Remove item
settings.items.remove(settings.active_index)
```

### Update Callbacks
```python
def on_value_changed(self, context):
    """Called when property changes"""
    print(f"Value changed to: {self.my_value}")
    # Trigger viewport update if needed
    context.area.tag_redraw()

class MyProperties(bpy.types.PropertyGroup):
    my_value: FloatProperty(
        name="Value",
        update=on_value_changed,
    )
```

### Pointer Properties
```python
class MyProperties(bpy.types.PropertyGroup):
    target_object: PointerProperty(
        name="Target",
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == 'MESH',  # Filter
    )

    target_material: PointerProperty(
        name="Material",
        type=bpy.types.Material,
    )
```

## Draw Functions and UI Layouts

### Layout Types
```python
def draw(self, context):
    layout = self.layout

    # Column - vertical stack
    col = layout.column(align=True)
    col.prop(obj, "location")
    col.prop(obj, "rotation_euler")

    # Row - horizontal stack
    row = layout.row(align=True)
    row.operator("object.select_all").action = 'SELECT'
    row.operator("object.select_all").action = 'DESELECT'

    # Box - framed section
    box = layout.box()
    box.label(text="Section Title")
    box.prop(obj, "name")

    # Split - proportional columns
    split = layout.split(factor=0.3)
    split.label(text="Label:")
    split.prop(obj, "name", text="")

    # Grid flow
    grid = layout.grid_flow(columns=3, even_columns=True)
    for i in range(9):
        grid.operator("mesh.primitive_cube_add", text=str(i))
```

### Property Widgets
```python
def draw(self, context):
    layout = self.layout
    obj = context.active_object

    # Standard property
    layout.prop(obj, "name")

    # Without label
    layout.prop(obj, "name", text="")

    # Expand enum
    layout.prop(obj, "display_type", expand=True)

    # Slider
    layout.prop(obj, "scale", slider=True)

    # Icon only
    layout.prop(obj, "hide_viewport", icon_only=True)

    # Search (for pointers)
    layout.prop_search(props, "target_object", bpy.data, "objects")

    # Template list
    layout.template_list("UI_UL_list", "", props, "items", props, "active_index")
```

## Common Pitfalls and Solutions

### Pitfall: Accessing Invalid Context
```python
# BAD - context may be None in some situations
def execute(self, context):
    obj = context.active_object  # Could be None!
    obj.location.z = 1.0  # AttributeError!

# GOOD - always check
def execute(self, context):
    obj = context.active_object
    if obj is None:
        self.report({'WARNING'}, "No active object")
        return {'CANCELLED'}
    obj.location.z = 1.0
    return {'FINISHED'}
```

### Pitfall: Data Access After Deletion
```python
# BAD - accessing removed object
obj = bpy.context.active_object
bpy.data.objects.remove(obj)
print(obj.name)  # ReferenceError!

# GOOD - don't access after removal
obj_name = obj.name
bpy.data.objects.remove(obj)
print(f"Removed: {obj_name}")
```

### Pitfall: Modifying Data in Draw
```python
# BAD - modifying data in draw causes infinite loop
def draw(self, context):
    context.scene.my_value = 5  # WRONG!

# GOOD - only read data in draw
def draw(self, context):
    layout = self.layout
    layout.label(text=str(context.scene.my_value))
```

### Pitfall: Missing BMesh Free
```python
# BAD - memory leak
bm = bmesh.new()
bm.from_mesh(mesh)
# ... operations ...
bm.to_mesh(mesh)
# Forgot bm.free()!

# GOOD - always free
bm = bmesh.new()
try:
    bm.from_mesh(mesh)
    # ... operations ...
    bm.to_mesh(mesh)
finally:
    bm.free()
```

### Pitfall: Circular Imports
```python
# BAD - __init__.py
from .operators import *  # Imports everything
from .panels import *     # panels.py imports from operators

# GOOD - explicit imports
from .operators import MY_OT_operator
from .panels import MY_PT_panel
```

## Registration Patterns

### Standard Registration
```python
classes = [
    MyPropertyGroup,
    MY_OT_operator,
    MY_PT_panel,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.my_props = PointerProperty(type=MyPropertyGroup)

def unregister():
    del bpy.types.Scene.my_props
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
```

### Conditional Registration
```python
def register():
    for cls in classes:
        try:
            bpy.utils.register_class(cls)
        except ValueError:
            # Already registered
            pass

def unregister():
    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            # Not registered
            pass
```

## Resources
- API Reference: https://docs.blender.org/api/current/
- Best Practices: https://docs.blender.org/api/current/info_best_practice.html
- Tips & Tricks: https://docs.blender.org/api/current/info_tips_and_tricks.html
