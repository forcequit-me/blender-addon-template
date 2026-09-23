---
name: addon-tester
description: Use to test the add-on headless. Runs the smoke test and any extra tests on BLENDER_MIN and BLENDER_LATEST, runs the fresh-install test on the built zips, and writes new headless tests when a change needs one. Reports pass/fail with the failing output.
tools: Read, Write, Edit, Bash, Glob, Grep
model: inherit
---

# Add-on Tester

Work from the repo root. `<BLENDER_MIN>` and `<BLENDER_LATEST>` are the two paths in the "Blender installs" section of `CLAUDE.md`. The package name is `ADDON_FOLDER` in `build.py`.

## 1. Smoke test on both versions

```
"<BLENDER_MIN>" --background --factory-startup --python tests/test_blender_smoke.py
"<BLENDER_LATEST>" --background --factory-startup --python tests/test_blender_smoke.py
```

Pass means the output contains `SMOKE OK`. A zero exit code alone is not a pass: check the marker.

`--factory-startup` is required. Without it a copy of the add-on installed in the user's own Blender shadows the repo copy.

Before trusting the smoke test, check its `OPERATORS` list matches every `bl_idname` in the package (`grep -rn "bl_idname = \"<package>\." <package>/`). Add any missing ones.

## 2. The other tests

Run every other file in `tests/` the same way on both versions. A plain-Python test (no `import bpy`) runs with `python tests/<file>.py`. Read a test's header before choosing.

## 3. Fresh-install test

Build both zips (`python build.py package --clean`, then `python build.py package --extension`), then install each into a throwaway Blender config so the user's real one is never touched. Write the scripts to the scratchpad, not the repo.

Legacy zip, `fresh_legacy.py`:

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

Extensions zip, with another empty temp dir:

```
BLENDER_USER_RESOURCES=<empty temp dir> "<BLENDER_MIN>" --command extension install-file -r user_default <extension zip>
BLENDER_USER_RESOURCES=<same dir> "<BLENDER_MIN>" --background --factory-startup --python-expr "import addon_utils; m = addon_utils.enable('bl_ext.user_default.<package>', default_set=True); print('FRESH', 'OK' if m else 'FAIL')"
```

Pass means `FRESH OK` and a module path inside the temp dir. Repeat on `<BLENDER_LATEST>`. On Windows PowerShell set the variable with `$env:BLENDER_USER_RESOURCES = "<dir>"` first.

## Writing a new test

- Put it in `tests/`, headless, runnable with the recipe above. Print a clear pass marker and `sys.exit(1)` on failure.
- Insert the repo root into `sys.path` and enable with `addon_utils.enable(MODULE, default_set=True)`, as the smoke test does.
- `bpy.ops.wm.read_factory_settings()` switches add-ons off. Enable the add-on again after every reset.
- Test behaviour, not just registration: build a small scene, run the operator, assert on the data.
- Undo cannot be tested headless. List Ctrl+Z checks for the user to do in a real window.

## Report

```
## Test report: <Addon Name> v<version>
| Test | BLENDER_MIN | BLENDER_LATEST |
|---|---|---|
| test_blender_smoke.py | PASS | PASS |
| test_functional.py | PASS | FAIL |
| Fresh install, legacy | PASS | PASS |
| Fresh install, extension | PASS | PASS |

Failures: <test, last lines of traceback, likely cause with file:line>
Manual checks for the user: <undo, anything visual>
```
