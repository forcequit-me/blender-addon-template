---
name: blender-documentation
description: Where to look things up for Blender 5.0+ add-on work - the Python API reference (current and per version), release notes with Python API changes, the user manual, the extensions platform rules, the gotchas pages, and the local and live alternatives. Use when you need an API signature, want to know when something changed, or need the manual's wording for a Blender feature.
---

# Blender documentation

Fastest first: the running build knows its own API better than any page.

`<BLENDER_MIN>` and `<BLENDER_LATEST>` below are the two paths in the "Blender installs" section of `CLAUDE.md`.

## 1. Ask Blender

```text
"<BLENDER_MIN>" --background --factory-startup --python-expr "import bpy; f = bpy.types.WindowManager.bl_rna.functions['invoke_confirm']; print([(p.identifier, p.type) for p in f.parameters])"
```

- Properties: `bpy.types.X.bl_rna.properties["name"]` (`.type`, `.default`, `.enum_items`, `.description`).
- Functions: `bpy.types.X.bl_rna.functions["name"].parameters`.
- Operators: `bpy.ops.object.parent_set.get_rna_type().properties`.
- With the MCP connected: `bpy_api_lookup` and `describe_node_type` (`blender-mcp-workflows`).
- Blender's own UI code is the best example of any layout: `<Blender install folder>/<version>/scripts/startup/bl_ui/`, for example `C:/Program Files/Blender Foundation/Blender 5.0/5.0/scripts/startup/bl_ui/` on Windows. Right-click any button in Blender > Edit Source (with Developer Extras on) jumps to it.

Check against `BLENDER_MIN`, the minimum, not only the newest installed build.

## 2. API reference

| What | URL |
| --- | --- |
| Current API | <https://docs.blender.org/api/current/> |
| A specific version | <https://docs.blender.org/api/5.0/> (also `/5.1/`, `/5.2/`) |
| One type | `https://docs.blender.org/api/current/bpy.types.UILayout.html` |
| One operator module | `https://docs.blender.org/api/current/bpy.ops.object.html` |
| Properties | <https://docs.blender.org/api/current/bpy.props.html> |
| Timers | <https://docs.blender.org/api/current/bpy.app.timers.html> |
| Handlers | <https://docs.blender.org/api/current/bpy.app.handlers.html> |
| GPU drawing (bgl is gone) | <https://docs.blender.org/api/current/gpu.html> |
| Change log (added and removed per version) | <https://docs.blender.org/api/current/change_log.html> |

Must-read pages, short and full of traps:

- Gotchas: <https://docs.blender.org/api/current/info_gotcha.html>
- Threading gotchas: <https://docs.blender.org/api/current/info_gotchas_threading.html>
- Best practice: <https://docs.blender.org/api/current/info_best_practice.html>
- Tips and tricks: <https://docs.blender.org/api/current/info_tips_and_tricks.html>

## 3. Release notes (what changed and when)

Python API changes per release, the place to look when something broke:

- <https://developer.blender.org/docs/release_notes/5.0/python_api/>
- <https://developer.blender.org/docs/release_notes/5.1/python_api/>
- <https://developer.blender.org/docs/release_notes/5.2/python_api/>

The old wiki.blender.org release notes are archived; do not cite them.

## 4. User manual and extensions platform

Use the manual for what a feature does from the user's side and for Blender's own words for menus and settings, so README and tooltip wording matches what users see.

- <https://docs.blender.org/manual/en/latest/>
- Installing legacy add-ons: <https://docs.blender.org/manual/en/latest/editors/preferences/addons.html>
- Add-ons as extensions, the manifest and the `blender --command extension` tool: <https://docs.blender.org/manual/en/latest/advanced/extensions/index.html>
- Extensions platform terms (rules 6.1 and 3.9, see `blender-version-targeting`): <https://extensions.blender.org/terms-of-service/>

## 5. Project documents

For how this add-on is named, documented, built and released, the repo wins over any web page:

- `CLAUDE.md`: Blender install paths, testing recipe, after-change checklist.
- `docs/README Spec.md`: README and tooltip rules.

## Search tips

- `site:docs.blender.org/api/current <TypeName>` finds the type page.
- When a page and the running Blender disagree, the running Blender is right for that version.
- Community answers (Stack Exchange, forums) are often for 2.8x to 4.x. Check any snippet against `BLENDER_MIN` before using it.
