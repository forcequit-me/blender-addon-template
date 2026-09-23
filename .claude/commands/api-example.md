---
description: Find a working Blender 5.x code example for a task, and prove it runs before handing it over
argument-hint: "<task, e.g. 'add a modifier' or 'react to file load'>"
allowed-tools: WebFetch, WebSearch, Read, Grep, Bash, mcp__blender__bpy_api_lookup
---

Find code for `$ARGUMENTS` that works on `BLENDER_MIN` and `BLENDER_LATEST` (the paths in the "Blender installs" section of `CLAUDE.md`).

1. **Look in the repo and skills first.** The package and the skills in `.claude/skills/` already hold many patterns. `Grep` for the API involved and prefer a pattern already in use.
2. **Then the docs**, versioned to the minimum: `https://docs.blender.org/api/5.0/` (or whatever bl_info `"blender"` says). Many class pages end with runnable examples. `mcp__blender__bpy_api_lookup` if the MCP is connected.
3. **Run it before handing it over.** Save the snippet to a temp or scratchpad folder, not the repo, and run it headless on both versions:
   ```
   "<BLENDER_MIN>" --background --factory-startup --python <snippet.py>
   "<BLENDER_LATEST>" --background --factory-startup --python <snippet.py>
   ```
   Timers do not fire in a background script that exits, and undo is unavailable; say so if the example depends on either.
4. **Give** the snippet in house style, one line on the key call, the gotcha if any, and the doc link.

## House idioms (verified on 5.0 and 5.2)

```python
# Store object references as pointers so they survive renames
class ADDON_NAME_PG_item(bpy.types.PropertyGroup):
    target: bpy.props.PointerProperty(type=bpy.types.Object)

# First-time scene setup: never inside register(), it raises _RestrictData
def _first_run():
    ...
    return None  # run once
bpy.app.timers.register(_first_run, first_interval=0)

# Handler that survives opening another file; remove it in unregister()
from bpy.app.handlers import persistent
@persistent
def _on_load(_):
    ...
bpy.app.handlers.load_post.append(_on_load)

# New materials already have a node tree in 5.x; find nodes by type, not name
mat = bpy.data.materials.new("Mask")
bsdf = next(n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
```
