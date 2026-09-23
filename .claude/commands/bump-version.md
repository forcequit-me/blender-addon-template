---
description: Bump the add-on's version in bl_info and blender_manifest.toml together, then rebuild
argument-hint: "[major|minor|patch|X.Y.Z]"
allowed-tools: Read, Edit, Bash, Grep, Glob
---

Bump the add-on's version. `$ARGUMENTS` is the bump type or an exact version. If it is missing, ask: patch for fixes, minor for new features, major for a big change in how it works.

1. Read `"version"` from bl_info in `<package>/__init__.py` (the package is `ADDON_FOLDER` in `build.py`). Work out the new version and show old and new.
2. Set both at once from the repo root:
   ```
   python build.py version X.Y.Z
   ```
   It writes bl_info `"version": (X, Y, Z)` and the manifest `version = "X.Y.Z"`. Read both back to confirm they match, and that the manifest `name` still matches bl_info `"name"`.
3. Grep the package and README for the old version string in case it appears anywhere else (a status label, a constant). Report hits; do not change them blindly.
4. Rebuild:
   ```
   python build.py package --clean
   ```
   and `python build.py package --extension` if you ship on the extensions platform. Confirm the zips in `build/` carry the new version.
5. Run the smoke test on `BLENDER_MIN` (path in the "Blender installs" section of `CLAUDE.md`); it asserts bl_info and the manifest agree.

No changelog file. Do not tag or push. Commit only if asked, with no AI attribution.
