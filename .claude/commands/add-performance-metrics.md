---
description: Time an operator or handler to find where it is slow, then remove the timing code
argument-hint: "<operator idname or function>"
allowed-tools: Read, Edit, Grep, Bash, mcp__blender__execute_blender_code
---

Measure `$ARGUMENTS` before optimising it. Timing code is temporary: it comes out before the add-on is committed.

## 1. Measure from outside first (no code changes)

Build a heavy scene (`/create-test-scene heavy`) and time the operator a few runs through the MCP, or headless with the same scene built in a script (see the benchmark in the `performance-optimization` skill):
```python
import time, bpy
times = []
for _ in range(5):
    t = time.perf_counter()
    bpy.ops.<package>.<operator>()
    times.append(time.perf_counter() - t)
print(f"min {min(times)*1000:.1f} ms, max {max(times)*1000:.1f} ms")
```
Handlers and `draw()` cannot be timed this way; go to step 2.

## 2. Break it down inside the code

Wrap sections temporarily:
```python
import time
_t = time.perf_counter()
... section ...
print(f"[perf] gather {1000 * (time.perf_counter() - _t):.1f} ms")
```
For a whole function, `cProfile` from a headless script is quicker than hand timers. Write its output to a temp or scratchpad folder, not the repo:
```python
import cProfile, pstats
cProfile.run("bpy.ops.<package>.<operator>()", r"<temp dir>/prof.out")
pstats.Stats(r"<temp dir>/prof.out").sort_stats("cumulative").print_stats(15)
```

## 3. Targets

| Code path | Aim for |
|---|---|
| A button click | under 100 ms on a heavy scene, or report progress |
| `draw()` | well under 1 ms; it runs on every redraw |
| depsgraph / frame handlers | near zero when nothing relevant changed |

## 4. Clean up

Remove every `[perf]` print and profiling import, grep the package for `[perf]` and `cProfile` to confirm (the add-on may use `time` legitimately), and report before/after numbers. No permanent profiling toggles in a shipped add-on.
