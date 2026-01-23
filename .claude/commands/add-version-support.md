---
description: Add support for additional Blender versions
---

Add backward or forward compatibility for additional Blender versions.

**Ask user:**
1. Which version(s) to add support for? (e.g., "3.6", "4.0 and 4.1")
2. What is the current minimum version?
3. What is the current maximum tested version?

**Process:**

1. **Analyze current code:**
   - Find all version-specific API usage
   - Identify APIs that differ between versions
   - Check existing compatibility code

2. **Create version detection:**
   ```python
   # In compat.py
   import bpy

   BLENDER_VERSION = bpy.app.version
   BLENDER_VERSION_STRING = '.'.join(map(str, BLENDER_VERSION[:2]))

   # Version checks
   IS_BLENDER_4_1_PLUS = BLENDER_VERSION >= (4, 1, 0)
   IS_BLENDER_4_0_PLUS = BLENDER_VERSION >= (4, 0, 0)
   IS_BLENDER_3_6_PLUS = BLENDER_VERSION >= (3, 6, 0)
   IS_BLENDER_3_0_PLUS = BLENDER_VERSION >= (3, 0, 0)
   ```

3. **Add compatibility wrappers:**

   For each API difference, create a wrapper:

   ```python
   # compat.py

   def create_node_socket(node_tree, name, socket_type, in_out):
       """Create node socket - compatible with 3.x and 4.x"""
       if IS_BLENDER_4_0_PLUS:
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

   def set_auto_smooth(obj, enabled=True, angle=0.523599):
       """Set auto smooth - compatible with pre and post 4.1"""
       if IS_BLENDER_4_1_PLUS:
           if enabled:
               mod = obj.modifiers.get("Smooth by Angle")
               if mod is None:
                   mod = obj.modifiers.new("Smooth by Angle", 'SMOOTH_BY_ANGLE')
               mod.angle = angle
           else:
               # Remove modifier if exists
               mod = obj.modifiers.get("Smooth by Angle")
               if mod:
                   obj.modifiers.remove(mod)
       else:
           if hasattr(obj.data, 'use_auto_smooth'):
               obj.data.use_auto_smooth = enabled
               if enabled:
                   obj.data.auto_smooth_angle = angle

   def get_node_socket_by_name(node, name, fallback_names=None):
       """Get socket with fallback names for version differences"""
       if name in node.inputs:
           return node.inputs[name]
       if name in node.outputs:
           return node.outputs[name]

       if fallback_names:
           for fallback in fallback_names:
               if fallback in node.inputs:
                   return node.inputs[fallback]
               if fallback in node.outputs:
                   return node.outputs[fallback]

       return None
   ```

4. **Update addon code to use wrappers:**
   ```python
   # Before
   mesh.use_auto_smooth = True

   # After
   from .compat import set_auto_smooth
   set_auto_smooth(obj, enabled=True, angle=0.523599)
   ```

5. **Add conditional imports:**
   ```python
   # For modules that may not exist in all versions
   try:
       from bpy.types import SmoothByAngleModifier
       HAS_SMOOTH_BY_ANGLE = True
   except ImportError:
       HAS_SMOOTH_BY_ANGLE = False
   ```

6. **Update bl_info:**
   ```python
   bl_info = {
       "blender": (3, 6, 0),  # Minimum supported version
       # ...
   }
   ```

7. **Update documentation:**
   - Add version support table to README
   - Document any version-specific behavior
   - List known limitations per version

   ```markdown
   ## Supported Blender Versions

   | Version | Support Level | Notes |
   |---------|--------------|-------|
   | 4.1+ | Full | Native support |
   | 4.0 | Full | Uses auto_smooth property |
   | 3.6 | Full | Uses legacy socket API |
   | 3.3 | Partial | Some features unavailable |
   | < 3.3 | Unsupported | |
   ```

8. **Create version test matrix:**
   ```python
   # test_versions.py - run in each Blender version
   import bpy
   import sys

   def test_compatibility():
       print(f"Testing in Blender {bpy.app.version_string}")

       tests = [
           ("Import addon", test_import),
           ("Register classes", test_register),
           ("Create operator", test_operator),
           ("Check panel", test_panel),
       ]

       results = []
       for name, test_func in tests:
           try:
               test_func()
               results.append((name, "PASS"))
           except Exception as e:
               results.append((name, f"FAIL: {e}"))

       for name, result in results:
           print(f"  {name}: {result}")
   ```

**Output:**
- Updated compat.py with new wrappers
- Modified addon code to use wrappers
- Updated bl_info version range
- Version support documentation
- Test checklist for each version
