---
name: blender-performance
description: Blender-specific speed patterns for 5.0+ - direct data access over bpy.ops, batch_remove, numpy foreach_get/foreach_set on attributes, evaluated meshes, BMesh, cheap draw() code with cached and throttled scans, handler cost, and splitting long work across timers. Use when an operator is slow on a big file, the viewport lags while the add-on is enabled, or a panel or handler walks bpy.data.
---

# Blender performance

Measure first (`performance-optimization`). Then these, roughly in order of payoff.

## 1. Direct data access, not operators

`bpy.ops` calls check context, redraw and push undo on every call. In a loop that is the whole cost.

```python
# slow: one operator call per object
for obj in objects:
    context.view_layer.objects.active = obj
    bpy.ops.object.modifier_add(type='SUBSURF')

# fast
for obj in objects:
    obj.modifiers.new("Subdivision", 'SUBSURF').levels = 2
```

When you must use an operator (Blender's parenting, joining), call it once on a prepared selection, not once per object.

## 2. Bulk removal

`bpy.data.batch_remove(ids)` removes many IDs in one pass. `bpy.data.objects.remove()` in a loop rebuilds relations each time.

## 3. Sets, not lists, for membership

IDs are hashable. `obj not in excluded` on a list is linear per check; build `excluded = set(...)` once.

## 4. numpy with foreach_get / foreach_set

```python
import numpy as np

mesh = obj.data
pos = mesh.attributes["position"]
co = np.empty(len(mesh.vertices) * 3, dtype=np.float32)
pos.data.foreach_get("vector", co)             # checked on 5.0 and 5.2
co = co.reshape(-1, 3)
co[:, 2] += 1.0
pos.data.foreach_set("vector", co.ravel())
mesh.update()
```

`mesh.vertices.foreach_get("co", ...)` still works too. Generic attributes read with `"value"`, `"vector"` or `"color"` depending on type. It works on ID collections as well: `bpy.data.objects.foreach_get("location", buf)` fills a flat array of every object's location (checked).

## 5. Evaluated data

```python
depsgraph = context.evaluated_depsgraph_get()
obj_eval = obj.evaluated_get(depsgraph)
mesh_eval = obj_eval.to_mesh()
try:
    count = len(mesh_eval.polygons)
finally:
    obj_eval.to_mesh_clear()
```

Get the depsgraph once per operator, not per object.

## 6. Mesh editing without mode switches

Topology changes: BMesh on the mesh data, no Edit Mode round trips.

```python
import bmesh

bm = bmesh.new()
try:
    bm.from_mesh(mesh)
    bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=1)
    bm.to_mesh(mesh)
finally:
    bm.free()
mesh.update()
```

Positions only: numpy (above). Leave BMesh for topology.

## 7. No forced updates in loops

Do not call `context.view_layer.update()` inside a loop. Blender evaluates once when the operator returns. Call it once, only if you need evaluated results mid-operator.

## 8. draw() runs constantly

Panels and header buttons redraw on mouse moves, during playback and during modal transforms. A `draw()` that walks `bpy.data` costs frame time for every user all the time.

The pattern for a button that shows live state (for example a header icon that lights up while the file has unused data):

- Handlers (`depsgraph_update_post`, `undo_post`, `redo_post`, `load_post`) only set a dirty flag and tag a redraw.
- `draw()` rescans only when dirty, stops at the first hit (`any(...)`, not a full count), and at most every 0.25 s.
- A skipped scan books a one-shot timer so the button still repaints once the window has passed.
- A user action that changes the answer drops the throttle so the UI feels instant.

Tag only the areas that need it:

```python
for window in context.window_manager.windows:
    for area in window.screen.areas:
        if area.type == 'VIEW_3D':
            area.tag_redraw()
```

## 9. Handlers

`depsgraph_update_post` fires on every change, including each step of a drag. Keep it to a flag or a set lookup. Check `depsgraph.id_type_updated('OBJECT')` or iterate `depsgraph.updates` to skip irrelevant updates. Never do file I/O in it.

## 10. Long work without freezing

- A batch over many items: process a slice per `bpy.app.timers` tick and return the next interval, or a modal operator with `event_timer_add`. Show progress with `layout.progress()` or `window_manager.progress_begin/update/end`. Details in `threading-async`.
- Anything slower than about a second needs visible progress and a way to stop.

## Targets

| Action | Budget |
| --- | --- |
| Button click | under 100 ms |
| draw(), handler during a drag | well under 1 ms |
| Batch job | progress shown after 1 s |

Reference: https://docs.blender.org/api/current/info_best_practice.html and https://docs.blender.org/api/current/info_tips_and_tricks.html
