# Blender add-on project guide

Read this first. It explains what lives where and how this add-on is built, tested and documented.

## What this project is

One Blender add-on, started from a template. The template ships a small working add-on (one operator, one sidebar panel, preferences, a smoke test) plus a Claude Code dev kit in `.claude/`. It targets Blender 5.0 and newer and can be packaged two ways: a legacy zip (Install from Disk) or an extension zip (extensions.blender.org).

## Layout

```
./
├── CLAUDE.md                this guide
├── README.md                describes this template until /setup-addon replaces it with ADDON_README.md
├── ADDON_README.md          the add-on's README skeleton; build.py ships it in the zip while it exists
├── addon_name/              the add-on itself: the folder that gets installed
│   ├── __init__.py          bl_info, class tuple, register() and unregister()
│   ├── blender_manifest.toml   extension manifest, kept in step with bl_info
│   ├── operators.py
│   ├── properties.py        PropertyGroup stored on the Scene
│   ├── panels.py            sidebar panel and the links footer
│   ├── links.py             the footer's open_link operator and the GitHub icon loader
│   ├── icons/               github.png and its Octicons licence
│   └── preferences.py
├── build.py                 builds the zips
├── tests/test_blender_smoke.py
├── docs/README Spec.md      how the README, tooltips and UI text are written
├── build/                   built zips, gitignored
├── .mcp.json                Blender MCP server, for live testing in a running Blender
└── .claude/                 dev kit: commands, skills, agents, hooks
```

## Names

The template uses these placeholders. `/setup-addon` renames all of them in place, including the folder:

| Placeholder | What it is |
|---|---|
| `addon_name` | Python package, folder, `ADDON_FOLDER` in build.py, `MODULE` in the smoke test, manifest `id`, the Scene property, operator idname prefix |
| `ADDON_NAME_` | class prefix (`ADDON_NAME_OT_example`, `ADDON_NAME_PT_panel`) |
| `Addon Name` | display name: bl_info and manifest `name`, sidebar tab (`bl_category`), panel label, README title |
| `Your Name` | bl_info `author`, manifest `maintainer` |
| `wm.addon_name_example` | the example operator's idname |

Every renamed name must still be found by `grep`: after a rename, search for the old placeholders and expect no hits. Once an add-on has shipped, never rename its package. Installed copies keep their preferences under the package name.

## Blender installs

Edit these two lines for your machine. The commands in `.claude/` read "the Blender paths in CLAUDE.md" from here.

```
BLENDER_MIN = C:/Program Files/Blender Foundation/Blender 5.0/blender.exe
BLENDER_LATEST = C:/Program Files/Blender Foundation/Blender 5.2/blender.exe
```

BLENDER_MIN is the oldest version you support, BLENDER_LATEST the newest you test on. Together they bracket the supported range. On macOS the path looks like `/Applications/Blender.app/Contents/MacOS/Blender`. On Linux it is wherever you unpacked Blender, for example `~/blender-5.2/blender`.

## Versions and install types

- Minimum Blender is 5.0. To change it, edit bl_info `"blender"` and the manifest `blender_version_min` together. There are no compat layers and no version branches: pick a minimum and write for it.
- `register()` refuses to run below the minimum, because Blender enables a legacy add-on below its minimum with only a warning. Extensions need no check: Blender will not install them below `blender_version_min`. Blender also deletes `bl_info` from an extension's module, so `register()` reads it with `globals().get("bl_info", {})`.
- Keep bl_info and `blender_manifest.toml` in step: `name`, `version`, and minimum Blender. The smoke test and `python build.py validate` both fail when they differ.
- **Legacy install** (Edit > Preferences > Add-ons > Install from Disk): the zip holds one package folder plus README.md. The manifest is left out.
- **Extension** (extensions.blender.org, or a downloaded extension zip): the manifest sits at the zip root. The platform has its own rules. Rule 6.1 forbids store and donation links in the UI, and rule 3.9 forbids touching the OS or other add-ons. So before you publish there, delete the links footer: `ADDON_NAME_PT_links`, `draw_links`, its call in `preferences.py`, `links.py` and `icons/`. `build.py package --extension` warns if either link is still set.

## Links footer

`panels.py` has `WEBSITE_URL = ""` and `BUG_REPORT_URL = ""`. When one is set, an icon button appears at the bottom of the sidebar panel (a header-less sub-panel, `bl_order = 100`, so it stays under any sub-panels you add) and at the bottom of the preferences. While both are empty, nothing is drawn. It is meant for legacy builds only; see above.

## Building

```
python build.py package --clean                    legacy zip:    build/Addon-Name-v0.1.0.zip
python build.py package --extension --clean        extension zip: build/Addon-Name-v0.1.0-extension.zip
python build.py validate                           bl_info, manifest and README present and in step
python build.py version 1.2.0                      set the version in bl_info and the manifest together
```

- `--clean` empties `build/` first, so only current zips sit there and you cannot ship an old one by mistake.
- The extension build runs `blender --command extension build`. build.py finds Blender from `--blender <path>`, then the `BLENDER` environment variable, then PATH, then the newest standard install. Pass `--blender` with BLENDER_LATEST to be explicit.
- Check an extension zip with `blender --command extension validate build/<zip>`.
- The zip name comes from the bl_info name and version.
- Every build you give anyone gets a new version, even before release, so an old copy can always be told apart. Feature: minor. Fix only: patch.

## Testing

Run from the project root, on both Blenders:

```
"<BLENDER_MIN>" --background --factory-startup --python tests/test_blender_smoke.py
"<BLENDER_LATEST>" --background --factory-startup --python tests/test_blender_smoke.py
```

Each must print `SMOKE OK`. The smoke test enables the add-on, checks every operator in `OPERATORS` registers, checks bl_info against the manifest, then disables and re-enables it. Add each new operator's idname to `OPERATORS`.

- `--factory-startup` is required. Without it, a copy of the add-on installed in your own Blender can load instead of the repo copy, and you end up testing the wrong code.
- In test scripts, `bpy.ops.wm.read_factory_settings()` switches add-ons off. Enable the add-on again after every reset.
- Undo cannot be tested headless. Check Ctrl+Z in a real Blender window.
- A fresh-install test: point `BLENDER_USER_RESOURCES` at an empty temp folder so your real config is not touched. Then install the legacy zip with `bpy.ops.preferences.addon_install` and enable it, or install the extension zip with `blender --command extension install-file -r user_default -e <zip>`.

## After changing the add-on

1. Smoke test (and any other tests) on BLENDER_MIN and BLENDER_LATEST.
2. `python build.py package --clean` (and `--extension` if you ship one), then a fresh-install test.
3. README "How to use" still matches the panel: every visible control, in the order the user meets it, with the exact labels.
4. Tooltips, report messages and the bl_info description are still true.
5. bl_info and manifest still in step (`python build.py validate`).
6. Commit.

## Writing READMEs and tooltips

Follow `docs/README Spec.md`. These are this template's defaults; the author can change them:

- Seven README sections. "Why I made this" is written by the author, never by Claude. If it is empty, leave the placeholder and say so.
- Tooltips are one line saying what happens when you click, and must match the code.
- Plain sentences, second person, no hype, no em dashes.

## Code standards

- Classes follow Blender naming: `ADDON_NAME_OT_<name>` for operators, `ADDON_NAME_PT_<name>` for panels. Every class goes in the `classes` tuple in `__init__.py`; `unregister()` walks it in reverse.
- Every operator that changes data has `bl_options = {'REGISTER', 'UNDO'}`.
- Tell the user what happened with `self.report()`. Return `{'CANCELLED'}` with a warning instead of raising.
- Add `poll()` when an operator only makes sense in some contexts, so the button greys out instead of failing.
- Advanced settings go in a fold box (see `show_settings` in `panels.py`), so the panel stays short.
- Prefer direct data access (`bpy.data`, object properties) over `bpy.ops` inside operators. It is faster and does not depend on context.
- Comments say why, not what.
- Operator idnames are `wm.addon_name_<name>`; other prefixes get no right-click Assign Shortcut.
- Use relative imports inside the package (`from . import operators`); extensions require them.

## Pitfalls

- **Never touch `bpy.data` inside `register()`.** It raises `_RestrictData` errors. Run first-time scene setup from `bpy.app.timers.register(fn, first_interval=0)`.
- **Store object and collection references as `PointerProperty`**, not names, so they survive renames. If older versions stored names, migrate them on file load (a `load_post` handler).
- **An update reloads only the add-on's `__init__.py`.** Blender keeps the other files in memory as the old version, so an update that adds a class fails to enable ("module has no attribute") until Blender restarts. `__init__.py` drops the add-on's own submodules from `sys.modules` before importing them, and the smoke test fakes an update (`check_update_loads_new_files`). Keep both. Even so, after Install from Disk the new version only runs once the add-on is unticked and ticked, or Blender restarts.
- **`--factory-startup` in every headless test**, or an installed copy shadows the repo copy.
- **Clean up in `unregister()`**: delete every property you added to Blender types, remove handlers, timers and keymaps, so disable and re-enable works.
- **Python one-liners with nested quotes break in shells.** Write the script to a file and run `blender --python file.py` instead.
- **On Windows, renaming a folder the editor has open can fail with "Access denied".** Create the new folder, move every item into it, then delete the empty old one.
- **Another AI session or tool may have changed files.** Check `git log` and `git status` before assuming a file is as you left it.

## Dev kit

`.claude/` holds the Claude Code dev kit: slash commands (`/setup-addon`, `/check-addon`, `/build`, `/bump-version`, `/test-addon`, `/test-in-blender`, `/new-operator`, `/new-panel`, `/live-dev`, `/inspect-scene`, `/create-test-scene`, `/docs-lookup`, `/api-example`, `/compare-api-versions`, `/add-performance-metrics`, `/setup-blender-dev`), skills, agents and hooks. The `check_edit.py` hook runs after every edit and flags house-style breaks. `guard_commit.py` blocks AI attribution in commit messages; it is off by default, and README.md shows how to switch it on.
