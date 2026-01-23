# Performance Optimization Skill

Expert knowledge for profiling and optimizing Blender addon performance.

## When to Use This Skill
- Operator feels slow or unresponsive
- Processing large datasets
- Viewport updates are laggy
- Optimizing batch operations
- Comparing algorithm performance
- Identifying bottlenecks

## Performance Profiling with time Module

### Basic Timing Pattern
```python
import time

def my_slow_function():
    start = time.perf_counter()

    # Your code here
    for i in range(1000):
        bpy.ops.mesh.primitive_cube_add()

    end = time.perf_counter()
    elapsed = end - start
    print(f"Execution time: {elapsed:.4f} seconds")
```

### Operator Performance Decorator
```python
import time
import functools

def profile_performance(func):
    """Decorator to measure operator performance"""
    @functools.wraps(func)
    def wrapper(self, context):
        start = time.perf_counter()
        result = func(self, context)
        elapsed = time.perf_counter() - start

        # Report to user
        self.report({'INFO'}, f"Completed in {elapsed:.3f}s")

        # Log for debugging
        print(f"{self.bl_idname}: {elapsed:.4f}s")

        return result
    return wrapper

class MY_OT_operator(bpy.types.Operator):
    bl_idname = "object.my_operator"
    bl_label = "My Operator"

    @profile_performance
    def execute(self, context):
        # Your code
        return {'FINISHED'}
```

### Multi-Section Profiling
```python
import time

class MY_OT_complex_operator(bpy.types.Operator):
    bl_idname = "object.complex_operator"
    bl_label = "Complex Operator"

    def execute(self, context):
        timings = {}

        # Section 1: Data preparation
        start = time.perf_counter()
        data = self.prepare_data(context)
        timings['prepare'] = time.perf_counter() - start

        # Section 2: Processing
        start = time.perf_counter()
        result = self.process_data(data)
        timings['process'] = time.perf_counter() - start

        # Section 3: Apply results
        start = time.perf_counter()
        self.apply_results(result, context)
        timings['apply'] = time.perf_counter() - start

        # Report breakdown
        total = sum(timings.values())
        print(f"Performance breakdown (total: {total:.3f}s):")
        for section, duration in timings.items():
            percentage = (duration / total) * 100
            print(f"  {section}: {duration:.3f}s ({percentage:.1f}%)")

        return {'FINISHED'}
```

### Statistical Profiling (Multiple Runs)
```python
import time
import statistics

def benchmark_operator(operator_id, runs=10):
    """Run operator multiple times and collect statistics"""
    times = []

    for i in range(runs):
        start = time.perf_counter()
        eval(f"bpy.ops.{operator_id}()")
        elapsed = time.perf_counter() - start
        times.append(elapsed)

    return {
        'mean': statistics.mean(times),
        'median': statistics.median(times),
        'stdev': statistics.stdev(times) if len(times) > 1 else 0,
        'min': min(times),
        'max': max(times),
        'runs': runs
    }

# Usage
stats = benchmark_operator('mesh.subdivide', runs=10)
print(f"Mean: {stats['mean']:.4f}s +/- {stats['stdev']:.4f}s")
print(f"Range: {stats['min']:.4f}s - {stats['max']:.4f}s")
```

## Performance Context Manager
```python
import time
from contextlib import contextmanager

@contextmanager
def timer(name="Operation"):
    """Context manager for timing code blocks"""
    start = time.perf_counter()
    yield
    elapsed = time.perf_counter() - start
    print(f"{name}: {elapsed:.4f}s")

# Usage
with timer("Mesh subdivision"):
    bpy.ops.mesh.subdivide(number_cuts=5)

with timer("Material creation"):
    mat = create_complex_material()
```

## Common Performance Bottlenecks

### 1. bpy.ops vs Direct Access
```python
import time
import bpy

# SLOW: Using operators
start = time.perf_counter()
for obj in bpy.context.selected_objects:
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_add(type='SUBSURF')
slow_time = time.perf_counter() - start

# FAST: Direct data access
start = time.perf_counter()
for obj in bpy.context.selected_objects:
    mod = obj.modifiers.new('Subsurf', 'SUBSURF')
    mod.levels = 2
fast_time = time.perf_counter() - start

print(f"Operators: {slow_time:.4f}s")
print(f"Direct: {fast_time:.4f}s")
print(f"Speedup: {slow_time/fast_time:.1f}x")
```

### 2. Viewport Updates
```python
# SLOW: Multiple viewport updates
for i in range(100):
    obj.location.x = i
    bpy.context.view_layer.update()  # Updates viewport each time!

# FAST: Batch updates
for i in range(100):
    obj.location.x = i
# Viewport updates once at the end
```

### 3. BMesh vs Operators
```python
import bmesh
import time

# SLOW: Using mesh operators
def subdivide_slow(obj, cuts):
    start = time.perf_counter()
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.subdivide(number_cuts=cuts)
    bpy.ops.object.mode_set(mode='OBJECT')
    return time.perf_counter() - start

# FAST: Using BMesh
def subdivide_fast(obj, cuts):
    start = time.perf_counter()
    bm = bmesh.new()
    bm.from_mesh(obj.data)

    bmesh.ops.subdivide_edges(bm, edges=bm.edges, cuts=cuts)

    bm.to_mesh(obj.data)
    bm.free()
    return time.perf_counter() - start

# Compare
slow = subdivide_slow(obj, 3)
fast = subdivide_fast(obj, 3)
print(f"Speedup: {slow/fast:.1f}x faster with BMesh")
```

## Optimization Patterns

### Pattern 1: Cache Expensive Calculations
```python
class MY_OT_cached_operator(bpy.types.Operator):
    bl_idname = "object.cached_operator"
    bl_label = "Cached Operator"

    _cache = {}

    def get_expensive_data(self, key):
        """Cache expensive calculations"""
        if key not in self._cache:
            start = time.perf_counter()
            self._cache[key] = self.calculate_expensive_data(key)
            print(f"Calculated {key}: {time.perf_counter()-start:.4f}s")
        else:
            print(f"Using cached {key}")
        return self._cache[key]

    @classmethod
    def clear_cache(cls):
        """Clear cache when needed"""
        cls._cache.clear()
```

### Pattern 2: Batch Operations
```python
import time

# SLOW: Individual operations
start = time.perf_counter()
for obj in objects:
    obj.location.z += 1.0
    obj.scale = (2, 2, 2)
    obj.rotation_euler.z = 0.5
slow_time = time.perf_counter() - start

# FAST: Prepare all data, then apply
start = time.perf_counter()
transforms = [(obj.location.x, obj.location.y, obj.location.z + 1.0) for obj in objects]

for obj, loc in zip(objects, transforms):
    obj.location = loc
    obj.scale = (2, 2, 2)
    obj.rotation_euler.z = 0.5
fast_time = time.perf_counter() - start
```

### Pattern 3: Lazy Evaluation
```python
class LazyData:
    """Only compute data when actually needed"""
    def __init__(self):
        self._data = None
        self._computed = False

    @property
    def data(self):
        if not self._computed:
            start = time.perf_counter()
            self._data = self.expensive_computation()
            elapsed = time.perf_counter() - start
            print(f"Computed lazy data: {elapsed:.4f}s")
            self._computed = True
        return self._data

    def expensive_computation(self):
        # Expensive operation here
        return [i**2 for i in range(1000000)]
```

## Performance Testing Framework

### Automated Performance Tests
```python
import time

class PerformanceTest:
    """Framework for performance testing"""

    def __init__(self, name):
        self.name = name
        self.results = []

    def run(self, func, *args, **kwargs):
        """Run function and record time"""
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start

        self.results.append({
            'time': elapsed,
            'func': func.__name__
        })

        return result

    def report(self):
        """Print performance report"""
        print(f"\n{self.name} Performance Report")
        print("=" * 50)
        for r in self.results:
            print(f"{r['func']}: {r['time']:.4f}s")

        if self.results:
            total = sum(r['time'] for r in self.results)
            print(f"Total: {total:.4f}s")

# Usage
test = PerformanceTest("Mesh Operations")
test.run(create_mesh, vertices=1000)
test.run(apply_modifiers, obj)
test.run(calculate_normals, mesh)
test.report()
```

## Performance Guidelines

### When to Optimize
1. **Profile first** - Don't optimize without measuring
2. **Find bottlenecks** - Focus on slowest parts
3. **User-perceivable** - Optimize operations > 100ms
4. **Diminishing returns** - 0.001s -> 0.0005s not worth effort

### Optimization Priority
1. **Algorithm choice** - Biggest impact (O(n^2) -> O(n))
2. **API usage** - Use direct access over operators
3. **Batch operations** - Reduce viewport updates
4. **Caching** - Avoid recalculation
5. **Code optimization** - Last resort (often negligible)

### Performance Targets
- **Interactive operations** (clicks): < 100ms
- **Modal updates** (per frame): < 16ms (60 FPS)
- **Batch operations**: Progress feedback if > 1s
- **Background tasks**: Use threading/async patterns

## Profiling Checklist

When profiling an operator:
- [ ] Time total execution
- [ ] Break down into sections
- [ ] Identify slowest section
- [ ] Compare alternatives (ops vs direct, bmesh vs ops)
- [ ] Test with different dataset sizes
- [ ] Profile with realistic data
- [ ] Test on different hardware if possible
- [ ] Document performance characteristics

## Resources
- Python time module: https://docs.python.org/3/library/time.html
- Blender performance tips: https://docs.blender.org/api/current/info_tips_and_tricks.html
- BMesh module: https://docs.blender.org/api/current/bmesh.html
