---
description: Add performance tracking to operator
---

Add performance profiling and metrics to an operator for optimization.

**Ask user:**
1. Which operator to profile? (class name or bl_idname)
2. What level of detail? (basic timing, section breakdown, statistical)
3. Should metrics be logged or displayed to user?

**Process:**

1. **Basic Timing:**
   ```python
   import time

   class MY_OT_profiled_operator(bpy.types.Operator):
       bl_idname = "object.profiled_operator"
       bl_label = "Profiled Operator"

       def execute(self, context):
           start = time.perf_counter()

           # Original execute code here
           self.do_work(context)

           elapsed = time.perf_counter() - start
           self.report({'INFO'}, f"Completed in {elapsed:.3f}s")

           return {'FINISHED'}
   ```

2. **Section Breakdown:**
   ```python
   import time

   class MY_OT_sectioned_operator(bpy.types.Operator):
       bl_idname = "object.sectioned_operator"
       bl_label = "Sectioned Operator"

       def execute(self, context):
           timings = {}

           # Section 1: Preparation
           start = time.perf_counter()
           data = self.prepare_data(context)
           timings['prepare'] = time.perf_counter() - start

           # Section 2: Processing
           start = time.perf_counter()
           result = self.process_data(data)
           timings['process'] = time.perf_counter() - start

           # Section 3: Apply
           start = time.perf_counter()
           self.apply_result(result, context)
           timings['apply'] = time.perf_counter() - start

           # Report
           total = sum(timings.values())
           print(f"Performance ({total:.3f}s total):")
           for section, duration in timings.items():
               pct = (duration / total) * 100 if total > 0 else 0
               print(f"  {section}: {duration:.3f}s ({pct:.1f}%)")

           self.report({'INFO'}, f"Completed in {total:.3f}s")
           return {'FINISHED'}
   ```

3. **Performance Decorator:**
   ```python
   import time
   import functools

   def profile_operator(func):
       """Decorator to profile operator execute method"""
       @functools.wraps(func)
       def wrapper(self, context):
           start = time.perf_counter()
           result = func(self, context)
           elapsed = time.perf_counter() - start

           # Log performance
           print(f"[PERF] {self.bl_idname}: {elapsed:.4f}s")

           # Report to user
           self.report({'INFO'}, f"Completed in {elapsed:.3f}s")

           return result
       return wrapper

   class MY_OT_decorated_operator(bpy.types.Operator):
       bl_idname = "object.decorated_operator"
       bl_label = "Decorated Operator"

       @profile_operator
       def execute(self, context):
           # Your code here
           return {'FINISHED'}
   ```

4. **Statistical Profiling:**
   ```python
   import time
   import statistics

   class PerformanceTracker:
       """Track performance across multiple runs"""

       _stats = {}

       @classmethod
       def record(cls, operator_id, duration):
           if operator_id not in cls._stats:
               cls._stats[operator_id] = []
           cls._stats[operator_id].append(duration)

       @classmethod
       def report(cls, operator_id):
           if operator_id not in cls._stats:
               return "No data"

           times = cls._stats[operator_id]
           return {
               'runs': len(times),
               'mean': statistics.mean(times),
               'median': statistics.median(times),
               'stdev': statistics.stdev(times) if len(times) > 1 else 0,
               'min': min(times),
               'max': max(times),
           }

       @classmethod
       def clear(cls, operator_id=None):
           if operator_id:
               cls._stats.pop(operator_id, None)
           else:
               cls._stats.clear()

   # Usage in operator
   class MY_OT_tracked_operator(bpy.types.Operator):
       bl_idname = "object.tracked_operator"
       bl_label = "Tracked Operator"

       def execute(self, context):
           start = time.perf_counter()

           # Your code here

           elapsed = time.perf_counter() - start
           PerformanceTracker.record(self.bl_idname, elapsed)

           # Show stats every 5 runs
           stats = PerformanceTracker.report(self.bl_idname)
           if stats['runs'] % 5 == 0:
               print(f"Stats after {stats['runs']} runs:")
               print(f"  Mean: {stats['mean']:.4f}s")
               print(f"  Range: {stats['min']:.4f}s - {stats['max']:.4f}s")

           return {'FINISHED'}
   ```

5. **Context Manager:**
   ```python
   import time
   from contextlib import contextmanager

   @contextmanager
   def timer(name="Operation", report_func=None):
       """Context manager for timing code blocks"""
       start = time.perf_counter()
       yield
       elapsed = time.perf_counter() - start
       message = f"{name}: {elapsed:.4f}s"
       print(message)
       if report_func:
           report_func({'INFO'}, message)

   # Usage
   class MY_OT_context_operator(bpy.types.Operator):
       bl_idname = "object.context_operator"
       bl_label = "Context Operator"

       def execute(self, context):
           with timer("Data preparation"):
               data = self.prepare_data()

           with timer("Processing"):
               result = self.process(data)

           with timer("Apply results", self.report):
               self.apply(result)

           return {'FINISHED'}
   ```

6. **Debug Toggle:**
   ```python
   import bpy
   import time

   # Add to addon preferences or properties
   class AddonPreferences(bpy.types.AddonPreferences):
       bl_idname = __name__

       enable_profiling: bpy.props.BoolProperty(
           name="Enable Performance Profiling",
           default=False,
       )

   class MY_OT_toggleable_profile(bpy.types.Operator):
       bl_idname = "object.toggleable_profile"
       bl_label = "Toggleable Profile"

       def execute(self, context):
           prefs = context.preferences.addons[__name__].preferences

           if prefs.enable_profiling:
               start = time.perf_counter()

           # Your code here

           if prefs.enable_profiling:
               elapsed = time.perf_counter() - start
               print(f"[PERF] {self.bl_idname}: {elapsed:.4f}s")

           return {'FINISHED'}
   ```

**Performance Guidelines:**

| Target | Threshold | Action if exceeded |
|--------|-----------|-------------------|
| Interactive | < 100ms | Optimize immediately |
| Modal (per frame) | < 16ms | Use async/batching |
| Batch operation | < 1s | Add progress indicator |
| Background task | Any | Use threading |

**Output:**
- Modified operator code with profiling
- Performance baseline
- Optimization suggestions based on results
