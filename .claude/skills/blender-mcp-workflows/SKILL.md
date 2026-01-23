# Blender MCP Workflows

Expert knowledge for using Blender MCP (Model Context Protocol) for live development and testing.

## When to Use This Skill
- Live testing operators without reloading
- Inspecting scene state during development
- Interactive debugging
- Automated test scene creation
- Real-time performance profiling

## What is Blender MCP?

Blender MCP allows Claude Code to:
- Execute Python code directly in a running Blender instance
- Query scene data and object properties
- Test operators in real-time
- Monitor console output
- Inspect current context

## Live Testing Workflows

### Test Operator Without Reload
```python
# Execute via MCP
import bpy

# Check if operator is registered
if hasattr(bpy.ops.my_addon, 'my_operator'):
    # Run it
    result = bpy.ops.my_addon.my_operator()
    print(f"Result: {result}")
else:
    print("Operator not registered - reload addon first")
```

### Test Operator Logic Directly
```python
# Execute via MCP - test execute() logic without full operator
import bpy

obj = bpy.context.active_object
if obj:
    # Simulate what your execute() does
    obj.location.z += 1.0
    print(f"Moved {obj.name} to {obj.location}")
else:
    print("No active object")
```

### Verify Registration
```python
# Execute via MCP
import bpy

# Check operators
addon_ops = [op for op in dir(bpy.ops.my_addon) if not op.startswith('_')]
print(f"Registered operators: {addon_ops}")

# Check panels
panels = [p for p in dir(bpy.types) if 'MY_PT' in p]
print(f"Registered panels: {panels}")

# Check property groups
if hasattr(bpy.types.Scene, 'my_props'):
    print("Scene properties registered")
```

## Scene Inspection Patterns

### Get Current State
```python
# Execute via MCP
import bpy

ctx = bpy.context
print(f"Mode: {ctx.mode}")
print(f"Active: {ctx.active_object.name if ctx.active_object else 'None'}")
print(f"Selected: {[o.name for o in ctx.selected_objects]}")
print(f"Scene: {ctx.scene.name}")
print(f"Frame: {ctx.scene.frame_current}")
```

### Inspect Object Properties
```python
# Execute via MCP
import bpy

obj = bpy.context.active_object
if obj:
    print(f"Name: {obj.name}")
    print(f"Type: {obj.type}")
    print(f"Location: {tuple(obj.location)}")
    print(f"Scale: {tuple(obj.scale)}")
    print(f"Rotation: {tuple(obj.rotation_euler)}")

    if obj.type == 'MESH':
        mesh = obj.data
        print(f"Vertices: {len(mesh.vertices)}")
        print(f"Faces: {len(mesh.polygons)}")
        print(f"Materials: {len(obj.material_slots)}")
```

### Check Modifiers
```python
# Execute via MCP
import bpy

obj = bpy.context.active_object
if obj and obj.modifiers:
    print(f"Modifiers on {obj.name}:")
    for i, mod in enumerate(obj.modifiers):
        print(f"  {i+1}. {mod.name} ({mod.type})")
        # Print some properties
        for prop in mod.bl_rna.properties:
            if not prop.is_readonly and prop.identifier not in ['name', 'type']:
                try:
                    value = getattr(mod, prop.identifier)
                    print(f"      {prop.identifier}: {value}")
                except:
                    pass
```

### Inspect Materials
```python
# Execute via MCP
import bpy

obj = bpy.context.active_object
if obj and obj.material_slots:
    for slot in obj.material_slots:
        mat = slot.material
        if mat:
            print(f"Material: {mat.name}")
            if mat.use_nodes:
                print(f"  Nodes: {len(mat.node_tree.nodes)}")
                for node in mat.node_tree.nodes:
                    print(f"    - {node.name} ({node.type})")
```

## Interactive Debugging

### Debug Context Issues
```python
# Execute via MCP - Check why poll() might fail
import bpy

ctx = bpy.context
print("Context check:")
print(f"  active_object: {ctx.active_object}")
print(f"  mode: {ctx.mode}")
print(f"  area.type: {ctx.area.type if ctx.area else 'None'}")
print(f"  selected_objects: {len(ctx.selected_objects)}")

# Check specific poll condition
if ctx.active_object:
    print(f"  object.type: {ctx.active_object.type}")
    print(f"  object.mode: {ctx.active_object.mode}")
```

### Test Property Access
```python
# Execute via MCP
import bpy

scene = bpy.context.scene

# Check if addon properties exist
if hasattr(scene, 'my_props'):
    props = scene.my_props
    print("Properties accessible:")
    for prop in props.bl_rna.properties:
        if not prop.is_readonly:
            value = getattr(props, prop.identifier)
            print(f"  {prop.identifier}: {value}")
else:
    print("Properties not registered")
```

### Trace Operator Execution
```python
# Execute via MCP - Add debug prints
import bpy

# Temporarily add verbose output
original_execute = bpy.types.MY_OT_operator.execute

def debug_execute(self, context):
    print(f"[DEBUG] Operator called")
    print(f"[DEBUG] Active object: {context.active_object}")
    result = original_execute(self, context)
    print(f"[DEBUG] Result: {result}")
    return result

bpy.types.MY_OT_operator.execute = debug_execute
print("Debug wrapper installed - run operator to see output")
```

## Test Scene Creation

### Basic Test Scene
```python
# Execute via MCP
import bpy

# Clear scene (optional)
# bpy.ops.object.select_all(action='SELECT')
# bpy.ops.object.delete()

# Create test objects
test_objects = []

# Cube
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
cube = bpy.context.active_object
cube.name = "Test_Cube"
test_objects.append(cube)

# Sphere
bpy.ops.mesh.primitive_uv_sphere_add(location=(3, 0, 0))
sphere = bpy.context.active_object
sphere.name = "Test_Sphere"
test_objects.append(sphere)

# Empty
bpy.ops.object.empty_add(location=(0, 3, 0))
empty = bpy.context.active_object
empty.name = "Test_Empty"
test_objects.append(empty)

print(f"Created {len(test_objects)} test objects")
```

### Scene with Specific State
```python
# Execute via MCP
import bpy

# Create object with modifiers
bpy.ops.mesh.primitive_cube_add()
obj = bpy.context.active_object
obj.name = "Test_Modified"

# Add modifiers
mod1 = obj.modifiers.new("Subsurf", 'SUBSURF')
mod1.levels = 2

mod2 = obj.modifiers.new("Bevel", 'BEVEL')
mod2.width = 0.1

# Add material
mat = bpy.data.materials.new("Test_Material")
mat.use_nodes = True
obj.data.materials.append(mat)

# Add vertex groups
vg = obj.vertex_groups.new(name="Test_Group")
vg.add([0, 1, 2, 3], 1.0, 'REPLACE')

print(f"Created test object with {len(obj.modifiers)} modifiers")
```

## Real-Time Validation

### Validate Operator Before/After
```python
# Execute via MCP
import bpy

# Capture state before
obj = bpy.context.active_object
before = {
    'location': tuple(obj.location),
    'vertex_count': len(obj.data.vertices) if obj.type == 'MESH' else 0,
    'modifier_count': len(obj.modifiers),
}

# Run operator
bpy.ops.my_addon.my_operator()

# Check state after
after = {
    'location': tuple(obj.location),
    'vertex_count': len(obj.data.vertices) if obj.type == 'MESH' else 0,
    'modifier_count': len(obj.modifiers),
}

# Report changes
print("Changes:")
for key in before:
    if before[key] != after[key]:
        print(f"  {key}: {before[key]} -> {after[key]}")
```

### Check for Errors
```python
# Execute via MCP
import bpy
import sys
from io import StringIO

# Capture stdout/stderr
old_stdout = sys.stdout
old_stderr = sys.stderr
sys.stdout = StringIO()
sys.stderr = StringIO()

try:
    bpy.ops.my_addon.my_operator()
    success = True
except Exception as e:
    success = False
    error = str(e)

stdout = sys.stdout.getvalue()
stderr = sys.stderr.getvalue()

sys.stdout = old_stdout
sys.stderr = old_stderr

print(f"Success: {success}")
if stdout:
    print(f"Output: {stdout}")
if stderr:
    print(f"Errors: {stderr}")
if not success:
    print(f"Exception: {error}")
```

## Performance Profiling

### Time Operator Execution
```python
# Execute via MCP
import bpy
import time

# Warm up
bpy.ops.my_addon.my_operator()

# Measure
times = []
for i in range(10):
    start = time.perf_counter()
    bpy.ops.my_addon.my_operator()
    elapsed = time.perf_counter() - start
    times.append(elapsed)

import statistics
print(f"Timing over {len(times)} runs:")
print(f"  Mean: {statistics.mean(times)*1000:.2f}ms")
print(f"  Min: {min(times)*1000:.2f}ms")
print(f"  Max: {max(times)*1000:.2f}ms")
if len(times) > 1:
    print(f"  Std: {statistics.stdev(times)*1000:.2f}ms")
```

## Console Output Monitoring

### Capture Blender Console
```python
# Execute via MCP
import bpy

# Recent reports
for report in bpy.context.window_manager.reports:
    print(f"[{report.type}] {report.message}")
```

## Error Handling

### Handle MCP Connection Issues
- Ensure Blender MCP server is running
- Check Blender version compatibility
- Verify MCP configuration

### Handle Execution Errors
- Wrap code in try/except
- Report meaningful error messages
- Suggest fixes for common issues

## Best Practices

1. **Test incrementally** - Run small code snippets
2. **Capture state** - Record before/after for validation
3. **Use descriptive names** - Prefix test objects with "Test_"
4. **Clean up** - Remove test objects after testing
5. **Profile realistically** - Test with representative data
6. **Check context** - Verify poll() conditions before testing

## MCP Commands Summary

| Task | Approach |
|------|----------|
| Test operator | `bpy.ops.my.operator()` |
| Check registration | `hasattr(bpy.ops.my, 'operator')` |
| Inspect scene | Query `bpy.context` |
| Create test data | Use `bpy.ops` or direct API |
| Profile | `time.perf_counter()` |
| Debug | Add print statements |
