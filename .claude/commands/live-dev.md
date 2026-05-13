---
description: Interactive development mode via MCP
allowed-tools: Bash, Read, Edit
---

Enable interactive development mode with live code execution and monitoring via MCP.

**Prerequisites:**
- Blender MCP server must be running
- Blender instance must be connected

**Process:**

1. **Establish MCP connection:**
   - Verify connection to Blender
   - Get Blender version and scene info
   - Confirm addon is loaded

2. **Set up development environment:**
   ```python
   # Execute via MCP - Development helpers
   import bpy
   import sys
   import importlib

   # Add addon path to sys.path if needed
   addon_path = r"path/to/addon"
   if addon_path not in sys.path:
       sys.path.insert(0, addon_path)

   # Helper function for quick reload
   def reload_addon(addon_name):
       """Reload addon modules"""
       # Remove cached modules
       modules_to_remove = [
           key for key in sys.modules.keys()
           if addon_name in key
       ]
       for module in modules_to_remove:
           del sys.modules[module]

       # Disable and re-enable
       try:
           bpy.ops.preferences.addon_disable(module=addon_name)
       except:
           pass
       bpy.ops.preferences.addon_enable(module=addon_name)
       print(f"Reloaded: {addon_name}")

   print("Development helpers loaded")
   print("  reload_addon(name) - Reload addon")
   ```

3. **Code execution workflow:**
   ```
   ┌─────────────────────────────────────────┐
   │  Edit code locally                      │
   │         ↓                               │
   │  Send code snippet via MCP              │
   │         ↓                               │
   │  Execute in Blender                     │
   │         ↓                               │
   │  Capture output/errors                  │
   │         ↓                               │
   │  Display results                        │
   │         ↓                               │
   │  Iterate                                │
   └─────────────────────────────────────────┘
   ```

4. **Quick test patterns:**

   **Test operator logic:**
   ```python
   # Execute via MCP
   import bpy

   # Test your operator logic directly
   obj = bpy.context.active_object
   if obj:
       # Your execute() logic here
       obj.location.z += 1.0
       print(f"Moved {obj.name} up")
   ```

   **Test property access:**
   ```python
   # Execute via MCP
   import bpy

   scene = bpy.context.scene
   if hasattr(scene, 'addon_props'):
       props = scene.addon_props
       print(f"Current value: {props.example_property}")
       props.example_property = 5.0
       print(f"New value: {props.example_property}")
   ```

   **Test UI drawing:**
   ```python
   # Execute via MCP - Force panel redraw
   import bpy

   for area in bpy.context.screen.areas:
       if area.type == 'VIEW_3D':
           area.tag_redraw()
   print("Forced viewport redraw")
   ```

5. **Monitor console output:**
   - Capture print statements
   - Watch for warnings
   - Report errors with full tracebacks
   - Show operator reports

6. **Auto-reload on change:**
   ```python
   # Concept - would need file watcher integration
   # When file changes detected:
   #   1. Reload specific module
   #   2. Re-register classes
   #   3. Report status
   ```

7. **Debug helpers:**
   ```python
   # Execute via MCP
   import bpy

   # Inspect registered operators
   def list_addon_operators(prefix):
       ops = []
       for category in dir(bpy.ops):
           cat = getattr(bpy.ops, category)
           for op in dir(cat):
               if prefix in op:
                   ops.append(f"{category}.{op}")
       return ops

   # Check class registration
   def is_class_registered(class_name):
       return class_name in dir(bpy.types)

   # Get property values
   def dump_props(obj):
       for prop in obj.bl_rna.properties:
           if not prop.is_readonly:
               print(f"  {prop.identifier}: {getattr(obj, prop.identifier)}")
   ```

**Interactive commands:**

| Command | Action |
|---------|--------|
| `exec <code>` | Execute Python code in Blender |
| `reload` | Reload addon modules |
| `status` | Show addon status |
| `console` | Show recent console output |
| `clear` | Clear test objects |
| `exit` | Exit live dev mode |

**Error handling:**
- Syntax errors: Show line number and suggestion
- Runtime errors: Full traceback with context
- Context errors: Explain required context

**Output:**
- Real-time execution results
- Console output streaming
- Error reports with solutions
- Reload confirmations
