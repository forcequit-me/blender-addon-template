---
description: Run the add-on's headless tests on BLENDER_MIN and BLENDER_LATEST, and optionally the fresh-install test on the built zips
argument-hint: "[fresh]"
allowed-tools: Bash, Read, Glob, Grep, Edit
---

Run every test for the add-on on both Blenders, from the repo root. `<BLENDER_MIN>` and `<BLENDER_LATEST>` are the paths in the "Blender installs" section of `CLAUDE.md`; the package is `ADDON_FOLDER` in `build.py`.

1. **Operator list up to date.** Compare `OPERATORS` in `tests/test_blender_smoke.py` with every operator `bl_idname` in the package. Add missing ones, remove deleted ones, and say what you changed.

2. **Smoke test, both versions:**
   ```
   "<BLENDER_MIN>" --background --factory-startup --python tests/test_blender_smoke.py
   "<BLENDER_LATEST>" --background --factory-startup --python tests/test_blender_smoke.py
   ```
   Pass = output contains `SMOKE OK`. It also asserts bl_info and the manifest agree on name, version and minimum Blender. Keep `--factory-startup`: without it a copy of the add-on installed in your own Blender shadows the repo copy.

3. **Extra tests.** Run every other file in `tests/` the same way on both versions. Plain-Python tests (no real bpy, possibly a stub module) run with `python tests/<file>.py`. Read the test's header.

4. **Fresh install** (when `$ARGUMENTS` says `fresh`, or before a release). Build first (`/build both`, or just legacy), then install each zip into a throwaway Blender config, so your real one is never touched. Put the script and temp dirs in a temp or scratchpad folder, not the repo.

   Legacy zip, script `fresh_legacy.py`:
   ```python
   import sys, bpy, addon_utils
   zip_path, module = sys.argv[sys.argv.index("--") + 1:]
   bpy.ops.preferences.addon_install(filepath=zip_path, overwrite=True)
   mod = addon_utils.enable(module, default_set=True)
   print("FRESH", "OK" if mod else "FAIL", mod.__file__ if mod else "")
   ```
   ```
   BLENDER_USER_RESOURCES=<empty temp dir> "<BLENDER_MIN>" --background --factory-startup --python fresh_legacy.py -- <legacy zip> <package>
   ```
   Extension zip, with a second empty temp dir:
   ```
   BLENDER_USER_RESOURCES=<empty temp dir> "<BLENDER_MIN>" --command extension install-file -r user_default <extension zip>
   BLENDER_USER_RESOURCES=<same dir> "<BLENDER_MIN>" --background --factory-startup --python-expr "import addon_utils; m = addon_utils.enable('bl_ext.user_default.<package>', default_set=True); print('FRESH', 'OK' if m else 'FAIL')"
   ```
   Pass = `FRESH OK`, with the module loaded from inside the temp dir. Repeat on `BLENDER_LATEST`. In PowerShell set the variable first with `$env:BLENDER_USER_RESOURCES = "<dir>"`.

5. **Report** a table of test by version with PASS/FAIL. For a failure, show the last lines of the traceback and the likely cause with file:line. Do not fix anything unless asked.

6. Remind the user that undo (Ctrl+Z) cannot be tested headless; list the operators whose undo they should try in a real window.

For live testing inside the running Blender, use `/test-in-blender`.
