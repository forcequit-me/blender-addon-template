---
description: Upgrade addon to a newer Blender version
argument-hint: "[target-version]"
allowed-tools: Read, Edit, Grep, Glob
---

Upgrade addon code to support a newer Blender version by replacing deprecated APIs.

**Ask user:**
1. What is the target Blender version? (e.g., 4.0, 4.1, 4.2)
2. Should we maintain backward compatibility? (yes/no)
3. What is the minimum version to support after upgrade?

**Process:**

1. **Run compatibility check first**
   - Identify all deprecated API usage
   - List breaking changes for target version

2. **Apply automatic replacements:**

   **For Blender 4.0:**
   ```python
   # Before (3.x)
   node_tree.inputs.new('NodeSocketFloat', "Value")
   node_tree.outputs.new('NodeSocketGeometry', "Geometry")

   # After (4.0+)
   node_tree.interface.new_socket(
       name="Value",
       socket_type='NodeSocketFloat',
       in_out='INPUT'
   )
   node_tree.interface.new_socket(
       name="Geometry",
       socket_type='NodeSocketGeometry',
       in_out='OUTPUT'
   )
   ```

   **For Blender 4.1:**
   ```python
   # Before (4.0)
   mesh.use_auto_smooth = True
   mesh.auto_smooth_angle = 0.523599

   # After (4.1+)
   mod = obj.modifiers.new(name="Smooth by Angle", type='SMOOTH_BY_ANGLE')
   mod.angle = 0.523599
   ```

3. **If maintaining backward compatibility:**
   - Add version detection code
   - Create compatibility wrappers in compat.py
   - Use conditional execution

   ```python
   # compat.py addition
   import bpy

   BLENDER_VERSION = bpy.app.version

   def set_auto_smooth(obj, angle):
       """Set auto smooth - compatible with 4.0 and 4.1+"""
       if BLENDER_VERSION >= (4, 1, 0):
           # Check for existing modifier
           mod = None
           for m in obj.modifiers:
               if m.type == 'SMOOTH_BY_ANGLE':
                   mod = m
                   break
           if mod is None:
               mod = obj.modifiers.new("Smooth by Angle", 'SMOOTH_BY_ANGLE')
           mod.angle = angle
       else:
           obj.data.use_auto_smooth = True
           obj.data.auto_smooth_angle = angle
   ```

4. **Update bl_info:**
   ```python
   # Update minimum version
   bl_info = {
       "blender": (4, 1, 0),  # Updated minimum
       # ...
   }
   ```

5. **Create upgrade notes:**
   ```markdown
   # Upgrade Notes: v1.0 → v2.0

   ## Breaking Changes
   - Minimum Blender version changed from 3.6 to 4.1
   - Auto-smooth now uses modifier instead of mesh property

   ## Migration Steps
   1. Update Blender to 4.1 or later
   2. Re-enable the addon
   3. Objects with auto-smooth will need modifier applied manually
      or use the new operator

   ## API Changes
   - `set_smooth()` function now adds modifier in 4.1+
   - Node socket creation uses new interface API
   ```

6. **Test upgraded code:**
   - Generate test script for new version
   - Verify all operators work
   - Check panel rendering
   - Test edge cases

**Major Version Changes Reference:**

| Version | Key Changes |
|---------|-------------|
| 2.80 | Collection system, select_set(), preferences |
| 3.0 | Asset browser, geometry nodes improvements |
| 3.2 | Asset system changes |
| 4.0 | Node socket interface API, extension system |
| 4.1 | Auto-smooth removed, Smooth by Angle modifier |

**Output:**
- List all changes made
- Show before/after code comparisons
- Update bl_info version
- Generate UPGRADE_NOTES.md
- Confirm test requirements
