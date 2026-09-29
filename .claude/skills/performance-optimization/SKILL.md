---
name: performance-optimization
description: How to measure before optimizing the add-on - perf_counter timing, cProfile inside Blender, a headless benchmark on a generated heavy scene, and comparing before and after. Use when someone says the add-on is slow, before changing code for speed, or to prove a speed change worked. Blender-specific fixes live in blender-performance.
---

# Measuring performance

Rule: no speed change without a number before and after, on a file big enough to matter.

## 1. Time the whole thing

```python
import time

start = time.perf_counter()
bpy.ops.wm.addon_name_example()
print(f"example: {(time.perf_counter() - start) * 1000:.1f} ms")
```

`perf_counter`, not `time.time`. Repeat 5 to 10 times and take the median; the first run pays for caches.

## 2. Find where the time goes

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()
bpy.ops.wm.addon_name_example()
profiler.disable()
pstats.Stats(profiler).sort_stats("cumulative").print_stats(15)
```

Read the top of `cumulative` for the slow path, `tottime` for the slow line. Time spent inside `bpy.ops` calls or `bpy_prop_collection` iteration points at `blender-performance` fixes.

## 3. Headless benchmark on a heavy scene

Build the worst case in code so it is repeatable. Save as `tests/bench_<name>.py` (next to the smoke test, never in the package) and run with `--factory-startup` as the smoke test does.

```python
import sys
import time
from pathlib import Path

import addon_utils
import bpy

MODULE = "addon_name"
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
addon_utils.enable(MODULE, default_set=True)

def build(count=20000):
    for i in range(count):
        empty = bpy.data.objects.new(f"E{i}", None)
        bpy.context.scene.collection.objects.link(empty)

times = []
for _ in range(5):
    build()                                    # rebuild each run: undo does not work headless
    start = time.perf_counter()
    bpy.ops.wm.addon_name_example()
    times.append(time.perf_counter() - start)
print(f"BENCH median {sorted(times)[len(times) // 2] * 1000:.1f} ms")
```

If you reset with `read_factory_settings()` instead, enable the add-on again after it; the reset switches add-ons off.

## 4. Draw and handler cost

A slow `draw()` or handler does not show up as a slow click; it shows as viewport lag. Time the function directly on a heavy file:

```python
from addon_name import utils
props = bpy.context.scene.addon_name
start = time.perf_counter()
for _ in range(1000):
    utils.has_work(props)
print(f"per call: {(time.perf_counter() - start):.3f} ms")   # 1000 calls, so seconds = ms per call
```

Budget: a fraction of a millisecond. For scale: a scan of 16,000 data blocks for unused ones measured 1.5 ms, about 10% of a frame, which is enough to need throttling.

## 5. Decide

- Under 100 ms for a click: leave it.
- Algorithm first (a list membership test in a loop, a nested scan of `bpy.data`), then API choice (operators to direct access, `batch_remove`, numpy), then caching.
- Write the measured number in a comment next to any code that exists only for speed, so nobody "simplifies" it away.
- Run the smoke tests on `BLENDER_MIN` and `BLENDER_LATEST` after the change.
