---
description: Live test using Blender MCP connection
---

Execute and test addon code in a running Blender instance via MCP.

**Prerequisites:**
- Blender MCP server must be running
- Blender instance must be connected

**Process:**

1. **Connect to Blender:**
   - Verify MCP connection is active
   - Get current Blender version
   - Check current scene state

2. **Test operator registration:**
   ```python
   # Execute via MCP
   import bpy

   # Check if operator is registered
   operator_id = "addon.example_operator"
   if hasattr(bpy.ops.addon, "example_operator"):
       print(f"✓ Operator '{operator_id}' is registered")
   else:
       print(f"✗ Operator '{operator_id}' NOT found")

   # List all addon operators
   addon_prefix = "addon."
   addon_ops = [op for op in dir(bpy.ops.addon) if not op.startswith('_')]
   print(f"Registered operators: {addon_ops}")
   ```

3. **Execute operator and capture result:**
   ```python
   # Execute via MCP
   import bpy

   # Set up test context
   if bpy.context.active_object is None:
       bpy.ops.mesh.primitive_cube_add()

   # Run operator
   try:
       result = bpy.ops.addon.example_operator()
       print(f"Operator result: {result}")
   except Exception as e:
       print(f"Operator error: {e}")

   # Check for console errors
   # (MCP should capture Blender console output)
   ```

4. **Verify operator effects:**
   ```python
   # Execute via MCP - check what changed
   import bpy

   obj = bpy.context.active_object
   print(f"Active object: {obj.name if obj else 'None'}")
   print(f"Selected objects: {[o.name for o in bpy.context.selected_objects]}")
   print(f"Object count: {len(bpy.data.objects)}")
   ```

5. **Test panel rendering:**
   ```python
   # Execute via MCP
   import bpy

   # Check panel registration
   panel_id = "VIEW3D_PT_addon_panel"
   if panel_id in dir(bpy.types):
       print(f"✓ Panel '{panel_id}' is registered")

       # Get panel info
       panel = getattr(bpy.types, panel_id)
       print(f"  Label: {panel.bl_label}")
       print(f"  Category: {panel.bl_category}")
       print(f"  Space: {panel.bl_space_type}")
   else:
       print(f"✗ Panel '{panel_id}' NOT found")
   ```

6. **Monitor console output:**
   - Capture any print statements
   - Watch for warnings
   - Report errors with tracebacks

**Test workflow:**

```
┌─────────────────────────────────────────┐
│  1. Verify MCP Connection               │
│     └─> Get Blender version             │
├─────────────────────────────────────────┤
│  2. Check Addon Registration            │
│     └─> List operators, panels          │
├─────────────────────────────────────────┤
│  3. Set Up Test Context                 │
│     └─> Create test objects if needed   │
├─────────────────────────────────────────┤
│  4. Execute Operator                    │
│     └─> Capture result and errors       │
├─────────────────────────────────────────┤
│  5. Verify Results                      │
│     └─> Check scene changes             │
├─────────────────────────────────────────┤
│  6. Report                              │
│     └─> Success/failure with details    │
└─────────────────────────────────────────┘
```

**Error handling:**
- Connection errors: Prompt to start MCP server
- Operator errors: Show full traceback
- Context errors: Suggest poll() fixes

**Output:**
- Connection status
- Operator registration status
- Execution result
- Any console output/errors
- Scene state changes
