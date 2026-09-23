---
description: Build the add-on's zip (legacy, extension or both) with build.py, clean, and verify it holds the right files
argument-hint: "[legacy|extension|both]"
allowed-tools: Bash, Read, Glob
---

Build the zip for this add-on from the repo root. `$ARGUMENTS` picks the kind: `legacy` (default), `extension`, or `both`.

1. Build:
   ```
   python build.py package --clean                 # legacy zip
   python build.py package --extension --clean     # extensions-platform zip
   ```
   For `both`, run the legacy build with `--clean` and then the extension build without it, or the second clean deletes the first zip. Always clean before a release build: without it old zips pile up in `build/` and the wrong one gets shipped. The extension build runs `blender --command extension build`; build.py finds Blender from `--blender <path>`, then the `BLENDER` environment variable, then PATH, then the newest standard install.

2. Check `build/` holds only the zips just built, named from the bl_info name and version: `build/<Name-Hyphenated>-v<version>.zip` for legacy and `build/<Name-Hyphenated>-v<version>-extension.zip` for the extension.

3. List each zip:
   ```
   python -c "import zipfile,glob; [print(z, n) for z in glob.glob('build/*.zip') for n in zipfile.ZipFile(z).namelist()]"
   ```
   - Legacy: one package folder plus `<package>/README.md`, nothing else. No `tests/`, `__pycache__`, `.pyc` or `blender_manifest.toml`.
   - Extension: `blender_manifest.toml` and the package files, no `tests/` or caches.

4. For an extension build, read the build output for the warning build.py prints when `WEBSITE_URL` or `BUG_REPORT_URL` is set in `panels.py`. The links footer must be deleted by hand before uploading to extensions.blender.org (rule 6.1, see the `blender-ui-patterns` skill). Report it if present.

5. Report each zip's path, file count and size.

Next step: the fresh-install test in `/test-addon`, or `/check-addon` for the full checklist.
