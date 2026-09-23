---
description: Read the running Blender's scene state through the Blender MCP, for debugging
argument-hint: "[what to inspect: selection, collections, modifiers, materials, context, add-on props]"
allowed-tools: Read, mcp__blender__get_addon_status, mcp__blender__get_scene_info, mcp__blender__get_object_info, mcp__blender__execute_blender_code, mcp__blender__get_viewport_screenshot
---

Inspect the user's open Blender. Read only: change nothing.

1. `mcp__blender__get_addon_status` for the Blender version, then `mcp__blender__get_scene_info` for the overview. `mcp__blender__get_object_info` for a named object.
2. For anything those do not cover, run a read-only snippet with `mcp__blender__execute_blender_code`. Pick what `$ARGUMENTS` asks for:

   | Ask | Print |
   |---|---|
   | selection | `context.mode`, active object, each selected object's name, type, parent, `users_collection` |
   | collections | the tree from `scene.collection`, with object counts, and which are excluded or hidden in the view layer |
   | modifiers | per object: name, type, `show_viewport`, `show_render` |
   | materials | slots per object; node counts; look nodes up by `node.type`, never by name |
   | context | `context.mode`, `area.type`, `space_data.type`; in edit mode, selected vert/edge/face counts via `bmesh.from_edit_mesh` |
   | add-on props | every property the add-on registers on `Scene`/`Object`/`WindowManager` (grep its `properties.py` for the names) and its preferences under `context.preferences.addons[<module>].preferences`, where the module is the package name for a legacy install or `bl_ext.<repo>.<package>` for an extension |

3. `mcp__blender__get_viewport_screenshot` if the question is about what the user sees.

Report in plain text: short headed sections, no decoration. Say what looks wrong if the question is about a bug.
