---
description: Turn this template into your add-on - rename every placeholder in place, swap in the add-on README, smoke-test on both Blenders and build
argument-hint: "<display name, e.g. Light Linker>"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Rename this template into a real add-on, in place, from the repo root. Run it once, on a fresh copy of the template.

## 1. Names

Ask for the display name if `$ARGUMENTS` is empty, and for the author name. Derive the rest and show the table before changing anything:

| Placeholder | Becomes | Rule | Example |
|---|---|---|---|
| `Addon Name` | display name | as typed; bl_info and manifest `name`, sidebar tab, panel label, README title | `Light Linker` |
| `addon_name` | package | lowercase; spaces and other non-alphanumerics to `_`; must start with a letter | `light_linker` |
| `ADDON_NAME_` | class prefix | package in capitals plus `_` (a shorter one is fine, e.g. `LL_`) | `LIGHT_LINKER_` |
| `Your Name` | author | bl_info `author`, manifest `maintainer` | `Sam Doe` |

The package becomes the folder name, the operator idname prefix (`wm.addon_name_example` becomes `wm.light_linker_example`), the Scene property, the manifest `id`, `ADDON_FOLDER` in `build.py`, and `MODULE` and `OPERATORS` in the smoke test. Stop and ask for another name if the package would shadow a module Blender or Python already has (`bpy`, `bmesh`, `mathutils`, `addon_utils`, `os`, `json` and so on), or if it is not a valid Python identifier.

Also ask:
- Where it ships: legacy zip, extensions.blender.org, or both.
- For a legacy build, the two links footer URLs, `WEBSITE_URL` and `BUG_REPORT_URL` in `panels.py`. Both may stay empty: the footer then draws nothing.

## 2. Rename in place

Touch only the add-on's own files: the package folder, `tests/`, `build.py` and `ADDON_README.md`. Leave `CLAUDE.md`, `docs/` and `.claude/` alone: they describe the placeholders on purpose.

1. Rename the folder `addon_name/` to the package, with `git mv` if the repo is under git. Skip `__pycache__`.
2. In those files, case-sensitive, replace in this order:
   - `ADDON_NAME_` with the class prefix
   - `addon_name` with the package
   - `Addon Name` with the display name
   - `Your Name` with the author
3. Set `WEBSITE_URL` and `BUG_REPORT_URL` if given. If the add-on ships only on the extensions platform, offer to delete `ADDON_NAME_PT_links` (now `<PREFIX>_PT_links`), `draw_links` and its call in preferences, and the README line about the two icon buttons (rule 6.1, see the `blender-ui-patterns` skill).
4. The manifest: `id` is the package, `name` and `version` match bl_info, `tagline` is 64 characters or fewer with no punctuation at the end. Leave a clear `tagline` for the author to write if there is no description yet.
5. README: `ADDON_README.md` is the add-on's user README (the root `README.md` describes the template). After the renames, move `ADDON_README.md` over `README.md`, replacing it, and delete `ADDON_README.md`. Leave "Why I made this" as the placeholder: the author writes it.

## 3. Leftovers

Search the whole repo, skipping `.git/`, `build/` and `.claude/`, case-sensitive, for each placeholder separately:

```
grep -rn --exclude-dir=.git --exclude-dir=build --exclude-dir=.claude -e "addon_name" -e "ADDON_NAME" -e "Addon Name" -e "Addon-Name" -e "Your Name" .
```

- Any hit in the package, `tests/`, `build.py` or `README.md` is a missed rename: fix it.
- Hits in `CLAUDE.md` or `docs/` are expected where they explain the placeholders. Report them; change them only if they read as if they were about this add-on.
- Do not widen the search to generic words like `addon` or `name`: Blender API names such as `addon_utils`, `template_list` or `bl_idname` are not leftovers.

## 4. Test and build

Check the paths in the "Blender installs" section of `CLAUDE.md` exist (`"<BLENDER_MIN>" --version`, same for `BLENDER_LATEST`). If one is wrong on this machine, ask for the right path and update that section.

```
"<BLENDER_MIN>" --background --factory-startup --python tests/test_blender_smoke.py
"<BLENDER_LATEST>" --background --factory-startup --python tests/test_blender_smoke.py
python build.py package --clean
```

Both runs must print `SMOKE OK: <package> (N operators)`, and `build/` must hold one `<Name-Hyphenated>-v<version>.zip`. If it ships on the extensions platform, also run `python build.py package --extension` and confirm the `-extension.zip`.

## 5. Git (optional)

If there is no `.git/`, offer `git init -b main`. If the folder is still a clone carrying the template's history, ask whether to keep it or start fresh; never delete `.git/` without a yes. Do not commit unless asked, and never with AI attribution. Do not create a remote repository.

## 6. Hand back

- **Write "Why I made this" yourself.** It is your own words; it will not be drafted for you.
- Text still marked `PLACEHOLDER` (bl_info `description`, manifest `tagline`, docstrings, README lines) is for you to write. List every hit of `grep -rn PLACEHOLDER` outside `.claude/`, and fill the README ones as the panel takes shape (`docs/README Spec.md`).
- Rename `wm.addon_name_example` (now `wm.<package>_example`) to a real operator when you build the first feature (`/new-operator`).
