---
description: Iterate on the add-on in the running Blender by editing the repo, reloading it live and checking the result
allowed-tools: Read, Edit, Write, Grep, Glob, Bash, mcp__blender__get_addon_status, mcp__blender__execute_blender_code, mcp__blender__get_scene_info, mcp__blender__get_object_info, mcp__blender__get_viewport_screenshot
---

Work on the add-on with the user's open Blender as the test bed.

## Start

1. `mcp__blender__get_addon_status`. No connection: point to `/setup-blender-dev` and stop.
2. Make a scratch scene: `scene = bpy.data.scenes.new("Addon Test")`, `bpy.context.window.scene = scene`. Leave the user's scenes alone and never save the file or preferences.
3. If a released copy of the add-on is installed as an extension, ask the user to disable it in Preferences first so its classes do not clash with the repo copy.
4. Define a reload helper once in Blender (package name is `ADDON_FOLDER` in `build.py`, repo path is the absolute path of the repo root):
   ```python
   import sys, addon_utils
   REPO = r"<absolute path of the repo root>"
   MODULE = "<package>"
   def addon_reload():
       addon_utils.disable(MODULE, default_set=False)
       for k in [k for k in sys.modules if k == MODULE or k.startswith(MODULE + ".")]:
           del sys.modules[k]
       if REPO not in sys.path:
           sys.path.insert(0, REPO)
       mod = addon_utils.enable(MODULE, default_set=False)
       print("loaded from", mod.__file__ if mod else "FAILED")
   import builtins; builtins.addon_reload = addon_reload
   addon_reload()
   ```
   The printed path must be inside the repo. If it points at the installed add-ons folder, the installed release is being tested instead.

## Loop

1. Edit the code in the repo.
2. Run `addon_reload()` through `mcp__blender__execute_blender_code`. A traceback here is a registration error: fix it before going on.
3. Exercise the change: run the operator, print the data it touched, take a screenshot if it is visual.
4. Repeat.

Blender keeps classes registered from the previous load if `unregister()` fails. If a reload behaves strangely, restart Blender rather than debugging stale state.

## Finish

Run `/test-addon` for the headless tests on `BLENDER_MIN` and `BLENDER_LATEST`, then `/check-addon` before committing. Ask whether to delete the scratch scene.
