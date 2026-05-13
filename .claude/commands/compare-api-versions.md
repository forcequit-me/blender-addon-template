---
description: Compare Blender API across versions
argument-hint: "<version-a> <version-b>"
allowed-tools: WebFetch, Read, Grep
---

Compare API between two Blender versions to identify changes, renames, and migration paths.

**Ask user:**
1. Which Blender versions to compare? (e.g., "3.6 vs 4.1")
2. What API feature to compare? (e.g., "geometry node sockets", "mesh operators", "all changes")

**Documentation URLs:**
- Version-specific API: https://docs.blender.org/api/{version}/
- Examples: /api/4.1/, /api/4.0/, /api/3.6/, /api/3.3/, /api/2.93/

**Process:**

1. **Parse version numbers**
2. **Fetch documentation from both versions**
3. **Compare and identify:**
   - Renamed items (operators, properties, nodes)
   - Removed features
   - Added features
   - Changed parameters
   - Changed default values
4. **Generate compatibility code**
5. **Provide migration guide**

**Example Output: Geometry Node Sockets (3.6 vs 4.0)**

```
═══════════════════════════════════════
Comparing Blender 3.6 vs 4.0
Feature: Geometry Node Sockets
═══════════════════════════════════════

API CHANGES
───────────────────────────────────────
Socket Creation (MAJOR CHANGE):

Blender 3.6:
  inputs.new('NodeSocketGeometry', "Geometry")
  inputs.new('NodeSocketFloat', "Value")

Blender 4.0:
  interface.new_socket(name="Geometry",
                      socket_type='NodeSocketGeometry',
                      in_out='INPUT')
  interface.new_socket(name="Value",
                      socket_type='NodeSocketFloat',
                      in_out='INPUT')

Socket Access:
  node.inputs["Geometry"]  # Still works in both


COMPATIBILITY CODE
───────────────────────────────────────
import bpy

def create_geometry_socket(node_tree, name, socket_type, in_out):
    """Create socket compatible with 3.6 and 4.0+"""
    if bpy.app.version >= (4, 0, 0):
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


MIGRATION GUIDE
───────────────────────────────────────
Upgrading from 3.6 to 4.0:

1. Replace all node_tree.inputs.new():
   OLD: node_tree.inputs.new('NodeSocketFloat', "Value")
   NEW: node_tree.interface.new_socket(name="Value",
                                       socket_type='NodeSocketFloat',
                                       in_out='INPUT')

2. Replace all node_tree.outputs.new():
   OLD: node_tree.outputs.new('NodeSocketGeometry', "Geo")
   NEW: node_tree.interface.new_socket(name="Geo",
                                       socket_type='NodeSocketGeometry',
                                       in_out='OUTPUT')

Documentation:
  3.6: https://docs.blender.org/api/3.6/bpy.types.NodeTree.html
  4.0: https://docs.blender.org/api/4.0/bpy.types.NodeTree.html
═══════════════════════════════════════
```

**Example Output: Mesh Auto-Smooth (4.0 vs 4.1)**

```
═══════════════════════════════════════
Comparing Blender 4.0 vs 4.1
Feature: Mesh Auto-Smooth
═══════════════════════════════════════

REMOVED PROPERTIES
───────────────────────────────────────
⚠️  BREAKING CHANGE

mesh.use_auto_smooth
  4.0: ✓ Available (bool property)
  4.1: ✗ REMOVED

mesh.auto_smooth_angle
  4.0: ✓ Available (float property)
  4.1: ✗ REMOVED


REPLACEMENT
───────────────────────────────────────
Use Smooth by Angle modifier instead

Blender 4.0:
  mesh.use_auto_smooth = True
  mesh.auto_smooth_angle = 0.523599  # 30 degrees

Blender 4.1:
  mod = obj.modifiers.new("Smooth", 'SMOOTH_BY_ANGLE')
  mod.angle = 0.523599


COMPATIBILITY CODE
───────────────────────────────────────
import bpy
import math

def set_smooth_shading(obj, angle_degrees=30):
    """Set smooth shading - compatible with 4.0 and 4.1"""
    angle_radians = math.radians(angle_degrees)

    if bpy.app.version >= (4, 1, 0):
        # Check for existing modifier
        smooth_mod = None
        for mod in obj.modifiers:
            if mod.type == 'SMOOTH_BY_ANGLE':
                smooth_mod = mod
                break

        if smooth_mod is None:
            smooth_mod = obj.modifiers.new(
                name="Smooth by Angle",
                type='SMOOTH_BY_ANGLE'
            )
        smooth_mod.angle = angle_radians
    else:
        if hasattr(obj.data, 'use_auto_smooth'):
            obj.data.use_auto_smooth = True
            obj.data.auto_smooth_angle = angle_radians


Documentation:
  4.0: https://docs.blender.org/api/4.0/bpy.types.Mesh.html
  4.1: https://docs.blender.org/api/4.1/bpy.types.Mesh.html
═══════════════════════════════════════
```

**Common Version Changes:**

| From | To | Major Changes |
|------|-----|---------------|
| 2.79 | 2.80 | Collections, select_set(), preferences |
| 2.93 | 3.0 | Python 3.10, library overrides |
| 3.6 | 4.0 | Node socket interface API |
| 4.0 | 4.1 | Auto-smooth removed |

**Output:**
- Detailed comparison report
- Renamed/removed/added items
- Working compatibility code
- Migration steps
- Documentation links
