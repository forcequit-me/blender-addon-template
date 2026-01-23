# API Documentation

This document describes the public API of the addon.

## Operators

### ADDON_OT_example_operator

Moves the active object on the Z axis.

**bl_idname:** `addon.example_operator`

**Location:** Search menu (F3), Panel button

**Properties:**

| Property | Type | Default | Range | Description |
|----------|------|---------|-------|-------------|
| `offset` | Float | 1.0 | -10 to 10 | Amount to move on Z axis |

**Poll:** Requires an active object.

**Usage:**
```python
import bpy

# Basic usage
bpy.ops.addon.example_operator()

# With custom offset
bpy.ops.addon.example_operator(offset=2.5)
```

**Returns:**
- `{'FINISHED'}` - Operation completed successfully
- `{'CANCELLED'}` - Operation failed (no active object or error)

---

## Panels

### VIEW3D_PT_addon_panel

Main addon panel in the 3D View sidebar.

**Location:** View3D > Sidebar (N) > Addon Tab

**Sections:**
- **Settings:** Addon property controls
- **Actions:** Operator buttons
- **Active Object:** Info about selected object

**Poll:** Always visible in 3D View.

---

## Properties

### AddonProperties

Main property group registered on `bpy.types.Scene`.

**Access:**
```python
props = bpy.context.scene.addon_props
```

**Properties:**

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `example_float` | Float | 1.0 | General float value (0-10) |
| `example_int` | Int | 5 | General integer value (0-100) |
| `example_bool` | Bool | False | Toggle feature |
| `example_string` | String | "" | Text input (max 256 chars) |
| `example_enum` | Enum | 'OPTION_A' | Mode selection |
| `example_color` | FloatVector[4] | (1,1,1,1) | RGBA color |
| `example_vector` | FloatVector[3] | (0,0,0) | 3D vector |

**Enum Values for `example_enum`:**
- `'OPTION_A'` - First option
- `'OPTION_B'` - Second option
- `'OPTION_C'` - Third option

---

## Utility Functions

### utils.get_selected_objects(context, obj_type=None)

Get selected objects, optionally filtered by type.

**Parameters:**
- `context` - Blender context
- `obj_type` (optional) - Filter by type ('MESH', 'CURVE', etc.)

**Returns:** List of selected objects

**Example:**
```python
from addon_name.utils import get_selected_objects

# All selected
objects = get_selected_objects(context)

# Only meshes
meshes = get_selected_objects(context, 'MESH')
```

---

### utils.get_active_mesh(context)

Get the active object's mesh data.

**Parameters:**
- `context` - Blender context

**Returns:** Mesh data or None

---

### utils.create_bmesh_from_object(obj, apply_modifiers=False)

Create a BMesh from an object.

**Parameters:**
- `obj` - Blender object
- `apply_modifiers` - Whether to apply modifiers first

**Returns:** BMesh instance

**Important:** Caller must call `bm.free()` when done.

**Example:**
```python
from addon_name.utils import create_bmesh_from_object, apply_bmesh_to_object

bm = create_bmesh_from_object(obj, apply_modifiers=True)
try:
    # Edit mesh...
    bmesh.ops.subdivide_edges(bm, edges=bm.edges, cuts=2)
    apply_bmesh_to_object(bm, obj)
finally:
    bm.free()
```

---

### utils.calculate_bounds(obj)

Calculate the world-space bounding box of an object.

**Parameters:**
- `obj` - Blender object

**Returns:** Tuple of (min_point, max_point, dimensions)

---

## Compatibility Functions

### compat.create_node_socket(node_tree, name, socket_type, in_out='INPUT')

Create a socket on a node tree, compatible across Blender versions.

**Parameters:**
- `node_tree` - The node tree
- `name` - Socket name
- `socket_type` - Type ('NodeSocketFloat', 'NodeSocketVector', etc.)
- `in_out` - 'INPUT' or 'OUTPUT'

**Returns:** The created socket

**Example:**
```python
from addon_name.compat import create_node_socket

socket = create_node_socket(
    node_tree,
    name="Value",
    socket_type="NodeSocketFloat",
    in_out='INPUT'
)
```

---

### compat.set_auto_smooth(obj, enable=True, angle=30.0)

Enable auto smooth on a mesh, compatible across versions.

**Parameters:**
- `obj` - Mesh object
- `enable` - Whether to enable
- `angle` - Angle in degrees

---

### compat.get_principled_socket_name(socket_name)

Get the correct Principled BSDF socket name for current version.

**Parameters:**
- `socket_name` - Generic socket name

**Returns:** Version-appropriate socket name

**Example:**
```python
from addon_name.compat import get_principled_socket_name

# Returns "Specular" in 3.x, "Specular IOR Level" in 4.0+
name = get_principled_socket_name("Specular")
```
