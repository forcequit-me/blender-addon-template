---
description: Test the addon in Blender
---

Test the addon by reloading scripts and checking for errors.

**Process:**

1. **Validate addon structure:**
   - Check `__init__.py` exists and has `bl_info`
   - Verify all imported modules exist
   - Check registration functions are defined

2. **Check for common issues:**
   - Missing `bl_idname` in operators/panels
   - Incorrect ID naming conventions
   - Missing `poll()` methods where needed
   - Circular imports
   - Undefined references

3. **Generate reload script:**
   ```python
   # Run this in Blender's Python console or Text Editor
   import bpy
   import importlib
   import sys

   addon_name = "addon_name"  # Replace with actual addon name

   # Remove cached modules
   modules_to_remove = [key for key in sys.modules.keys()
                        if addon_name in key]
   for module in modules_to_remove:
       del sys.modules[module]

   # Disable and re-enable addon
   try:
       bpy.ops.preferences.addon_disable(module=addon_name)
   except:
       pass

   bpy.ops.preferences.addon_enable(module=addon_name)
   print(f"Addon '{addon_name}' reloaded successfully")
   ```

4. **Verification checklist:**
   - [ ] Addon appears in Preferences > Add-ons
   - [ ] No errors in console on enable
   - [ ] Operators appear in F3 search
   - [ ] Panels appear in correct locations
   - [ ] Properties are accessible
   - [ ] Operators execute without errors
   - [ ] Undo/redo works correctly

5. **Test edge cases:**
   - Run operators with no selection
   - Run operators in different modes (Object, Edit, etc.)
   - Test with different object types
   - Check behavior with multiple objects selected

**Common Error Solutions:**

| Error | Cause | Solution |
|-------|-------|----------|
| `AttributeError: module has no attribute` | Import issue | Check module imports and file names |
| `RuntimeError: register_class(...): already registered` | Double registration | Check classes list for duplicates |
| `ReferenceError: StructRNA removed` | Accessing deleted data | Refresh references after operations |
| `poll() failed, context incorrect` | Wrong context | Add proper poll() check |

**Report results:**
- List any errors found
- Confirm successful tests
- Suggest fixes for issues
