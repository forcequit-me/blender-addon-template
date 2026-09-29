---
name: blender-mcp-workflows
description: Using the Blender MCP server (execute_blender_code, get_scene_info, get_viewport_screenshot, bpy_api_lookup, describe_node_type) to check APIs, inspect state and see a panel in your running Blender while building the add-on. Use when the Blender MCP is connected and you need live answers or a visual check; headless tests stay the pass/fail gate.
---

# Blender MCP workflows

The MCP drives the user's **real, running Blender**: their preferences, their installed add-ons, their open file. Treat it like their desk, not a test rig.

## Ground rules

- Start with `get_addon_status` to read `blender_version`, then `get_scene_info` before changing anything.
- Do not edit or delete the user's data. Make a new scene or ask before touching the open file. Name test objects `Test_...` and remove them when done.
- The live Blender runs the **installed** copy of an add-on, not the repo copy, unless you load the repo copy (`/live-dev`). Headless runs with `--factory-startup` (see `blender-version-targeting`) are what prove the repo code works on `BLENDER_MIN` and `BLENDER_LATEST`. Use MCP for questions and visual checks.
- Keep each `execute_blender_code` call small and print what you need.

## Look things up instead of guessing

- `bpy_api_lookup`: `"WindowManager.invoke_confirm"`, `"Scene.compositing_node_group"`, `"bpy.ops.object.parent_set"`, `"ImageFormatSettings.file_format"`. Returns real arguments, types, defaults and enum items for the running build.
- `describe_node_type`: `"ShaderNodeMix"` with `{"data_type": "RGBA"}` gives the socket layout for that mode. Use it before indexing sockets or setting a node enum.
- Remember the running build may be newer than the minimum. An API that exists live still needs checking on `BLENDER_MIN` headless.

## Inspect state

```python
import addon_utils
import bpy
ctx = bpy.context
print(ctx.mode, ctx.scene.name, [o.name for o in ctx.selected_objects])
print(addon_utils.check("addon_name"))        # (enabled by default, enabled now)
props = ctx.scene.addon_name
print({p.identifier: getattr(props, p.identifier) for p in props.bl_rna.properties if p.identifier != "rna_type"})
```

Registration check without running anything:

```python
import bpy
for op in ("wm.addon_name_example",):
    cat, name = op.split(".")
    print(op, getattr(getattr(bpy.ops, cat), name).get_rna_type().name)
print([c for c in dir(bpy.types) if c.startswith("ADDON_NAME_")])
```

## Before and after an operator

```python
import bpy
before = {o.name for o in bpy.data.objects}
result = bpy.ops.wm.addon_name_example()
after = {o.name for o in bpy.data.objects}
print(result, "removed:", sorted(before - after)[:20], "added:", sorted(after - before)[:20])
```

MCP code usually runs without an area, so operators that need a 3D View can fail their poll. Wrap them:

```python
import bpy
win = bpy.context.window_manager.windows[0]
area = next(a for a in win.screen.areas if a.type == 'VIEW_3D')
region = next(r for r in area.regions if r.type == 'WINDOW')
with bpy.context.temp_override(window=win, area=area, region=region):
    bpy.ops.view3d.view_selected()
```

## See the panel

`get_viewport_screenshot` captures the 3D View. Open the add-on's sidebar tab first, then check the rules in `blender-ui-patterns`: controls in order, Settings closed, status line readable, links footer at the bottom (legacy builds). Compare against the README's How to use.

```python
import bpy
for area in bpy.context.window_manager.windows[0].screen.areas:
    if area.type == 'VIEW_3D':
        area.spaces.active.show_region_ui = True
        area.tag_redraw()
```

## Timing on a real file

```python
import bpy, time
t = time.perf_counter()
bpy.ops.wm.addon_name_example()
print(f"{(time.perf_counter() - t) * 1000:.1f} ms")
```

This runs on the open file for real. Run destructive operators only after the user has opened a test file, or ask first. For proper measurement use `performance-optimization`.

## Material and node code

Find nodes by type, not name: `next(n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')`. Names are translated on non-English UIs. Set colours on shader inputs, not `material.diffuse_color`.

## What MCP cannot tell you

- Whether it works on `BLENDER_MIN` if the live one is newer, or the reverse.
- Whether a fresh install of the built zip works: use the fresh-install test in `/test-addon`.
- Undo behaviour: confirm Ctrl+Z by hand in a real window.
