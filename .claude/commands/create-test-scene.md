---
description: Build a scratch test scene in the running Blender through the Blender MCP
argument-hint: "[basic|modifiers|materials|hierarchy|collections|heavy|custom description]"
allowed-tools: Read, mcp__blender__get_addon_status, mcp__blender__execute_blender_code, mcp__blender__get_scene_info, mcp__blender__get_viewport_screenshot
---

Build test data for the add-on in the user's open Blender. Ask what the add-on under test needs if `$ARGUMENTS` does not say.

Always work in a new scene so the user's work is untouched:
```python
import bpy
scene = bpy.data.scenes.new("Addon Test")
bpy.context.window.scene = scene
```
Create objects with the data API (`bpy.data.meshes.new`, `bpy.data.objects.new`, `scene.collection.objects.link`) rather than `bpy.ops` primitives, which depend on context. Prefix every name with `Test_`. Never save.

| Preset | Contents |
|---|---|
| basic | a few meshes, an empty, a camera, a light |
| modifiers | meshes with Subdivision, Multires, Bevel, a Geometry Nodes modifier |
| materials | meshes with node materials, one with an alpha texture, one with no material; set values on node inputs, find nodes by `type` |
| hierarchy | parent/child chains, including a child inside a different collection than its parent |
| collections | nested collections, one excluded, one hidden, one instanced |
| heavy | a few thousand objects or a dense mesh, for performance checks |

Read enum values from `bl_rna` before assigning them rather than hardcoding identifiers.

Finish with `mcp__blender__get_scene_info` and a screenshot, then list what was created. When testing is done, offer to clean up: switch the window back to the user's scene, remove the `Test_` objects, meshes, materials and collections by name, then remove the `Addon Test` scene. Do not use `orphans_purge`: it would also delete the user's own unused data.
