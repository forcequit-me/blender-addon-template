# Blender Performance Optimization

Expert knowledge for optimizing Blender addon performance.

## When to Use This Skill
- Operator feels slow or unresponsive
- Processing large datasets
- Viewport updates are laggy
- Optimizing batch operations
- Reducing memory usage

## Viewport Update Best Practices

### Minimize Update Calls
```python
# BAD - updates after each change
for obj in objects:
    obj.location.z += 1.0
    bpy.context.view_layer.update()  # Expensive!

# GOOD - batch changes, single update
for obj in objects:
    obj.location.z += 1.0
# Viewport updates automatically at end of operator
```

### Defer Updates
```python
# For many property changes
with bpy.context.view_layer.depsgraph.updates_paused():
    for obj in objects:
        obj.modifiers.new("Subsurf", 'SUBSURF')
# Updates resume automatically
```

### Force Redraw Only When Needed
```python
# Only tag redraw for specific areas
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        area.tag_redraw()
        break  # Don't redraw all viewports
```

## Batch Operations vs Individual Updates

### Object Operations
```python
import time

# SLOW: Using operators in loop
start = time.perf_counter()
for i in range(100):
    bpy.ops.mesh.primitive_cube_add(location=(i, 0, 0))
slow_time = time.perf_counter() - start

# FAST: Direct data creation
start = time.perf_counter()
mesh = bpy.data.meshes.new("SharedMesh")
bpy.ops.mesh.primitive_cube_add()
template = bpy.context.active_object.data

for i in range(100):
    obj = bpy.data.objects.new(f"Cube_{i}", template.copy())
    obj.location.x = i
    bpy.context.collection.objects.link(obj)
fast_time = time.perf_counter() - start

# Speedup: typically 5-20x
```

### Modifier Operations
```python
# SLOW: Operator per modifier
for obj in objects:
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_add(type='SUBSURF')

# FAST: Direct modifier creation
for obj in objects:
    mod = obj.modifiers.new("Subsurf", 'SUBSURF')
    mod.levels = 2
```

### Selection Operations
```python
# SLOW: Operator selection
for obj in objects:
    obj.select_set(False)
bpy.ops.object.select_all(action='DESELECT')

# FAST: Direct selection
for obj in bpy.context.selected_objects:
    obj.select_set(False)
```

## Context Overrides for Efficiency

### Avoid Mode Switching
```python
# SLOW: Switch modes repeatedly
for obj in mesh_objects:
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.subdivide()
    bpy.ops.object.mode_set(mode='OBJECT')

# FAST: Use BMesh (no mode switch needed)
import bmesh
for obj in mesh_objects:
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.subdivide_edges(bm, edges=bm.edges, cuts=1)
    bm.to_mesh(obj.data)
    bm.free()
```

### Batch Context Override
```python
# Process multiple objects with single context setup
override = bpy.context.copy()
for obj in objects:
    override['active_object'] = obj
    override['selected_objects'] = [obj]
    with bpy.context.temp_override(**override):
        bpy.ops.object.transform_apply(scale=True)
```

## Depsgraph Usage Patterns

### Evaluated Data Access
```python
# Get evaluated (with modifiers applied) mesh
depsgraph = bpy.context.evaluated_depsgraph_get()
obj_eval = obj.evaluated_get(depsgraph)
mesh_eval = obj_eval.to_mesh()

# Process evaluated mesh
vertices = [v.co.copy() for v in mesh_eval.vertices]

# Clean up
obj_eval.to_mesh_clear()
```

### Dependency Updates
```python
# Update specific object
obj.update_tag()

# Update entire depsgraph
bpy.context.view_layer.update()

# Check if update needed
depsgraph = bpy.context.evaluated_depsgraph_get()
if depsgraph.id_type_updated('OBJECT'):
    # Objects changed
    pass
```

## Memory Management for Large Datasets

### Chunked Processing
```python
def process_in_chunks(items, chunk_size=1000):
    """Process large lists in chunks to manage memory"""
    for i in range(0, len(items), chunk_size):
        chunk = items[i:i + chunk_size]
        yield chunk

# Usage
for chunk in process_in_chunks(large_object_list, 500):
    for obj in chunk:
        process_object(obj)
    # Memory can be freed between chunks
```

### Generator Pattern
```python
# BAD: Load all into memory
def get_all_vertices(objects):
    vertices = []
    for obj in objects:
        for v in obj.data.vertices:
            vertices.append(v.co.copy())
    return vertices  # Huge memory usage!

# GOOD: Generator yields one at a time
def iter_vertices(objects):
    for obj in objects:
        for v in obj.data.vertices:
            yield obj, v.co.copy()

# Process without loading all
for obj, co in iter_vertices(objects):
    process_vertex(obj, co)
```

### Clear Unused Data
```python
# Remove orphaned data blocks
bpy.ops.outliner.orphans_purge(do_recursive=True)

# Or manually
for mesh in bpy.data.meshes:
    if mesh.users == 0:
        bpy.data.meshes.remove(mesh)
```

## BMesh vs Mesh Data

### When to Use BMesh
```python
import bmesh

# Complex mesh editing operations
# - Subdivide, extrude, bevel
# - Topology changes
# - Selections

bm = bmesh.new()
bm.from_mesh(mesh)

# Operations
bmesh.ops.subdivide_edges(bm, edges=bm.edges, cuts=2)
bmesh.ops.extrude_face_region(bm, geom=bm.faces)

bm.to_mesh(mesh)
bm.free()
```

### When to Use Direct Mesh Access
```python
# Fast vertex position access/modification
# - Transform vertices
# - Read positions
# - No topology changes

mesh = obj.data

# Read positions (fast)
positions = [v.co.copy() for v in mesh.vertices]

# Write positions (fast)
for v in mesh.vertices:
    v.co.z += 1.0

mesh.update()
```

### Numpy for Large Meshes
```python
import numpy as np

mesh = obj.data

# Fast read with numpy
vertex_count = len(mesh.vertices)
positions = np.empty(vertex_count * 3, dtype=np.float32)
mesh.vertices.foreach_get('co', positions)
positions = positions.reshape(-1, 3)

# Fast write with numpy
positions[:, 2] += 1.0  # Raise all Z
mesh.vertices.foreach_set('co', positions.ravel())
mesh.update()
```

## Performance Profiling

### Basic Timing
```python
import time

start = time.perf_counter()
# Operation
elapsed = time.perf_counter() - start
print(f"Operation took: {elapsed:.4f}s")
```

### Section Profiling
```python
class OperatorProfiler:
    def __init__(self):
        self.timings = {}

    def start(self, section):
        self.timings[section] = {'start': time.perf_counter()}

    def end(self, section):
        self.timings[section]['elapsed'] = (
            time.perf_counter() - self.timings[section]['start']
        )

    def report(self):
        total = sum(t.get('elapsed', 0) for t in self.timings.values())
        print(f"Total: {total:.4f}s")
        for section, data in self.timings.items():
            elapsed = data.get('elapsed', 0)
            pct = (elapsed / total * 100) if total > 0 else 0
            print(f"  {section}: {elapsed:.4f}s ({pct:.1f}%)")
```

## Optimization Checklist

### Before Optimizing
- [ ] Profile to find actual bottleneck
- [ ] Measure baseline performance
- [ ] Identify if CPU, memory, or I/O bound

### Common Optimizations
- [ ] Replace `bpy.ops` with direct data access
- [ ] Batch operations instead of loops
- [ ] Use BMesh for complex mesh operations
- [ ] Use numpy for large vertex arrays
- [ ] Minimize viewport updates
- [ ] Process in chunks for large datasets
- [ ] Use generators for memory efficiency

### Performance Targets
| Operation Type | Target |
|---------------|--------|
| Interactive (button click) | < 100ms |
| Modal (per frame) | < 16ms |
| Batch operation | < 1s or show progress |

## Resources
- Performance tips: https://docs.blender.org/api/current/info_tips_and_tricks.html
- BMesh module: https://docs.blender.org/api/current/bmesh.html
