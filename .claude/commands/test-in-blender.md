---
description: Test the add-on's operators in the running Blender through the Blender MCP
argument-hint: "[operator idname]"
allowed-tools: Read, Grep, Glob, mcp__blender__get_addon_status, mcp__blender__execute_blender_code, mcp__blender__get_scene_info, mcp__blender__get_object_info, mcp__blender__get_viewport_screenshot
---

Live-test the add-on (and one operator, if given in `$ARGUMENTS`) in the user's open Blender. Follow the `blender-live-tester` agent's rules; the short version:

1. `mcp__blender__get_addon_status`. No connection: stop and point to `/setup-blender-dev`.
2. Create a scratch scene (`bpy.data.scenes.new("Addon Test")`, make it the window's scene). Never touch the user's objects, never save.
3. Load the repo copy, not the installed release. Package name is `ADDON_FOLDER` in `build.py`; if a release is installed as an extension, ask the user to disable it first.
   ```python
   import sys, addon_utils
   REPO = r"<absolute path of the repo root>"
   MODULE = "<package>"
   addon_utils.disable(MODULE, default_set=False)
   for k in [k for k in sys.modules if k == MODULE or k.startswith(MODULE + ".")]:
       del sys.modules[k]
   if REPO not in sys.path:
       sys.path.insert(0, REPO)
   mod = addon_utils.enable(MODULE, default_set=False)
   print("loaded from", mod.__file__ if mod else "FAILED")
   ```
4. Confirm every operator in `tests/test_blender_smoke.py` `OPERATORS` resolves (`getattr(getattr(bpy.ops, cat), name).get_rna_type()`).
5. For each operator under test: set up the context, print state, run it, print state, note the return value and the report message. Try the edge cases that matter (nothing selected, wrong type, wrong mode).
6. `mcp__blender__get_viewport_screenshot` when the result is visual.
7. Report a table of operator, case, result, notes. List undo checks to do by hand. Offer to delete the scratch scene.
