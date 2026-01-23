# Blender Addon Development Standards

## Project Overview
This project is a Blender addon developed using Python and the Blender Python API (bpy).

## Blender Python API Conventions

### Context and Data Access
- Use `bpy.context` for current state (active object, selected objects, mode)
- Use `bpy.data` for accessing all data in the blend file
- Always check context validity before operations
- Prefer direct data access over operators when possible for performance

```python
# Good: Direct access
obj = bpy.context.active_object
obj.location.x = 5.0

# Avoid when possible: Operator calls (slower)
bpy.ops.transform.translate(value=(5, 0, 0))
```

### Naming Conventions
- **Addon folder**: `lowercase_with_underscores`
- **Operator IDs**: `CATEGORY_OT_operation_name` (e.g., `MESH_OT_custom_subdivide`)
- **Panel IDs**: `CATEGORY_PT_panel_name` (e.g., `VIEW3D_PT_custom_tools`)
- **Property Group IDs**: `CATEGORY_PG_group_name`
- **Menu IDs**: `CATEGORY_MT_menu_name`
- **UIList IDs**: `CATEGORY_UL_list_name`
- Use descriptive names with type hints for properties
- Use `snake_case` for Python functions and variables
- Use `SCREAMING_SNAKE_CASE` for constants

### bl_info Dictionary
Every addon must have a properly formatted `bl_info` dictionary:

```python
bl_info = {
    "name": "Addon Name",
    "author": "Your Name",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),  # Minimum Blender version
    "location": "View3D > Sidebar > Tab Name",
    "description": "Brief description of addon functionality",
    "warning": "",  # Optional warning text
    "doc_url": "",  # Documentation URL
    "category": "Object",  # Choose appropriate category
}
```

## Addon Structure Requirements

### Required Files
```
addon_name/
├── __init__.py          # Main addon file with bl_info and registration
├── operators.py         # Operator classes
├── panels.py            # UI panel classes
├── properties.py        # Property definitions
├── utils.py             # Utility functions
└── compat.py            # Version compatibility wrappers
```

### Registration Pattern
```python
# In __init__.py
classes = [
    MyOperator,
    MyPanel,
    MyPropertyGroup,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    # Register properties after classes
    bpy.types.Scene.my_props = bpy.props.PointerProperty(type=MyPropertyGroup)

def unregister():
    # Unregister properties before classes
    del bpy.types.Scene.my_props
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
```

## Operator Design Patterns

### Basic Operator Structure
```python
class CATEGORY_OT_operator_name(bpy.types.Operator):
    """Tooltip description shown on hover"""
    bl_idname = "category.operator_name"
    bl_label = "Operator Label"
    bl_description = "Detailed description"
    bl_options = {'REGISTER', 'UNDO'}

    # Properties
    my_prop: bpy.props.FloatProperty(
        name="Property Name",
        description="Property description",
        default=1.0,
        min=0.0,
        max=10.0,
    )

    @classmethod
    def poll(cls, context):
        """Check if operator can run in current context"""
        return context.active_object is not None

    def invoke(self, context, event):
        """Called when operator is invoked (optional)"""
        # For user interaction before execute
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        """Main operator logic"""
        try:
            # Your code here
            self.report({'INFO'}, "Operation completed")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}

    def draw(self, context):
        """Draw operator properties in popup (optional)"""
        layout = self.layout
        layout.prop(self, "my_prop")
```

### Return Values
- `{'FINISHED'}` - Operator completed successfully
- `{'CANCELLED'}` - Operator was cancelled or failed
- `{'RUNNING_MODAL'}` - Operator is running in modal mode
- `{'PASS_THROUGH'}` - Pass event to other operators

### Modal Operators
For continuous interaction (drag, draw, etc.):
```python
class CATEGORY_OT_modal_operator(bpy.types.Operator):
    bl_idname = "category.modal_operator"
    bl_label = "Modal Operator"

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':
            # Handle mouse movement
            return {'RUNNING_MODAL'}
        elif event.type == 'LEFTMOUSE':
            # Confirm operation
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            # Cancel operation
            return {'CANCELLED'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
```

## UI/UX Patterns

### Panel Structure
```python
class VIEW3D_PT_my_panel(bpy.types.Panel):
    bl_label = "Panel Label"
    bl_idname = "VIEW3D_PT_my_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "My Tab"
    bl_options = {'DEFAULT_CLOSED'}  # Optional

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def draw_header(self, context):
        layout = self.layout
        layout.label(icon='MODIFIER')

    def draw(self, context):
        layout = self.layout
        obj = context.active_object

        # Column layout
        col = layout.column(align=True)
        col.prop(obj, "location")

        # Row layout
        row = layout.row(align=True)
        row.operator("category.operator_name")

        # Box
        box = layout.box()
        box.label(text="Section Title")

        # Split
        split = layout.split(factor=0.3)
        split.label(text="Label:")
        split.prop(obj, "name", text="")
```

### Common Panel Locations
- `VIEW_3D` + `UI` = 3D View Sidebar (N-panel)
- `VIEW_3D` + `TOOLS` = 3D View Tool Shelf (T-panel)
- `PROPERTIES` + `WINDOW` = Properties Editor
- `NODE_EDITOR` + `UI` = Node Editor Sidebar

### Translation
Always use translation functions for user-visible text:
```python
from bpy.app.translations import pgettext as _

layout.label(text=_("Translatable Text"))
```

## Property Definitions

### Property Types
```python
class MyPropertyGroup(bpy.types.PropertyGroup):
    # Basic types
    my_int: bpy.props.IntProperty(name="Integer", default=0, min=0, max=100)
    my_float: bpy.props.FloatProperty(name="Float", default=0.0, precision=3)
    my_bool: bpy.props.BoolProperty(name="Boolean", default=False)
    my_string: bpy.props.StringProperty(name="String", default="", maxlen=256)

    # Enum (dropdown)
    my_enum: bpy.props.EnumProperty(
        name="Enum",
        items=[
            ('OPTION_A', "Option A", "Description for A"),
            ('OPTION_B', "Option B", "Description for B"),
        ],
        default='OPTION_A',
    )

    # Vectors
    my_vector: bpy.props.FloatVectorProperty(name="Vector", size=3, default=(0, 0, 0))
    my_color: bpy.props.FloatVectorProperty(name="Color", subtype='COLOR', size=4, default=(1, 1, 1, 1))

    # Collections
    my_collection: bpy.props.CollectionProperty(type=MyItemPropertyGroup)
    my_index: bpy.props.IntProperty(name="Active Index", default=0)

    # Pointer
    my_object: bpy.props.PointerProperty(name="Object", type=bpy.types.Object)
```

### Update Callbacks
```python
def update_callback(self, context):
    """Called when property value changes"""
    print(f"Value changed to: {self.my_prop}")

my_prop: bpy.props.FloatProperty(
    name="My Property",
    update=update_callback,
)
```

## Performance Considerations

### Viewport Updates
- Minimize calls to `bpy.context.view_layer.update()`
- Batch property changes before triggering updates
- Use `depsgraph.update()` only when necessary

### Efficient Operations
```python
# Good: Batch operations
for obj in objects:
    obj.location.x += 1.0
# Single update at end

# Bad: Individual updates
for obj in objects:
    obj.location.x += 1.0
    bpy.context.view_layer.update()  # Expensive!
```

### BMesh for Mesh Operations
Use BMesh for complex mesh editing instead of operators:
```python
import bmesh

bm = bmesh.new()
bm.from_mesh(obj.data)

# Edit mesh...
bmesh.ops.subdivide_edges(bm, edges=bm.edges, cuts=2)

bm.to_mesh(obj.data)
bm.free()
```

## Version Compatibility

### Version Detection
```python
import bpy

BLENDER_VERSION = bpy.app.version

if BLENDER_VERSION >= (4, 0, 0):
    # Blender 4.0+ code
    pass
elif BLENDER_VERSION >= (3, 0, 0):
    # Blender 3.x code
    pass
else:
    # Older versions
    pass
```

### bl_info Version Range
```python
bl_info = {
    "blender": (3, 6, 0),  # Minimum version required
    # ...
}
```

### Compatibility Wrappers
Create `compat.py` for version-specific code:
```python
# compat.py
import bpy

BLENDER_VERSION = bpy.app.version

def create_node_socket(node_tree, name, socket_type, in_out):
    """Create socket compatible across versions"""
    if BLENDER_VERSION >= (4, 0, 0):
        return node_tree.interface.new_socket(
            name=name,
            socket_type=socket_type,
            in_out=in_out
        )
    else:
        if in_out == 'INPUT':
            return node_tree.inputs.new(socket_type, name)
        else:
            return node_tree.outputs.new(socket_type, name)
```

## Error Handling

### Operator Error Handling
```python
def execute(self, context):
    try:
        # Main logic
        result = self.do_operation(context)
        self.report({'INFO'}, f"Completed: {result}")
        return {'FINISHED'}
    except ValueError as e:
        self.report({'WARNING'}, f"Invalid value: {e}")
        return {'CANCELLED'}
    except Exception as e:
        self.report({'ERROR'}, f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return {'CANCELLED'}
```

### Context Validation
Always validate context in `poll()`:
```python
@classmethod
def poll(cls, context):
    return (
        context.active_object is not None
        and context.active_object.type == 'MESH'
        and context.mode == 'OBJECT'
    )
```

## Testing Approach

### Manual Testing Checklist
- [ ] Addon enables without errors
- [ ] Operators appear in search menu (F3)
- [ ] Panels appear in correct locations
- [ ] All properties work correctly
- [ ] Undo/redo works for operators
- [ ] No console errors during normal use
- [ ] Works with expected object types
- [ ] Handles edge cases gracefully

### Test Scene Setup
Create test scenes with:
- Various object types (mesh, curve, empty, etc.)
- Different selection states
- Multiple objects
- Edge cases (empty meshes, complex hierarchies)

## Documentation Standards

### Operator Documentation
- Set `bl_description` for detailed tooltip
- Use docstring for tooltip preview
- Document all properties with `description` parameter

### Code Comments
- Comment complex algorithms
- Explain version-specific workarounds
- Document performance considerations
- Note any limitations or known issues

## Code Organization

### Import Order
```python
# Standard library
import os
import math
from typing import Set, List

# Blender modules
import bpy
import bmesh
from bpy.types import Operator, Panel
from bpy.props import FloatProperty, IntProperty

# Local modules
from . import utils
from .compat import create_node_socket
```

### Module Structure
- `__init__.py` - Registration and bl_info only
- `operators.py` - All operator classes
- `panels.py` - All panel classes
- `properties.py` - Property groups and definitions
- `utils.py` - Shared utility functions
- `compat.py` - Version compatibility code
- `constants.py` - Constants and enums (if needed)

## Security Considerations

- Never execute arbitrary code from user input
- Validate file paths before file operations
- Sanitize string inputs used in expressions
- Be cautious with `exec()` or `eval()`

## Common Pitfalls to Avoid

1. **Accessing context in wrong thread** - bpy.context is only valid in main thread
2. **Missing poll() method** - Causes crashes in invalid contexts
3. **Not freeing BMesh** - Memory leaks with `bm.free()`
4. **Hardcoded paths** - Use `bpy.path` utilities
5. **Not handling missing data** - Always check if objects/data exist
6. **Circular imports** - Structure modules carefully
7. **Registering classes multiple times** - Track registration state
8. **Not reversing unregistration order** - Unregister in reverse order
