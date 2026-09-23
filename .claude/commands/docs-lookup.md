---
description: Look up the Blender Python API or manual for the versions the add-on supports
argument-hint: "<query, e.g. bpy.types.Panel or 'depsgraph handler'>"
allowed-tools: WebFetch, WebSearch, mcp__blender__bpy_api_lookup
---

Answer `$ARGUMENTS` from the official docs for the minimum Blender the add-on supports (bl_info `"blender"`, 5.0 by default).

## Sources, in order

1. `mcp__blender__bpy_api_lookup` when the Blender MCP is connected. It reflects the running version.
2. Versioned API docs. Use the minimum version, not `current`, so the answer holds for it:
   - Class: `https://docs.blender.org/api/5.0/bpy.types.<Class>.html`
   - Operators: `https://docs.blender.org/api/5.0/bpy.ops.<category>.html`
   - Properties: `https://docs.blender.org/api/5.0/bpy.props.html`
   - Modules: `bmesh.html`, `mathutils.html`, `bpy.app.handlers.html`, `bpy.app.timers.html`, `bpy.utils.html`
   - Gotchas worth reading: `info_gotcha.html`, `info_best_practice.html`
3. Manual, for user-facing behaviour: `https://docs.blender.org/manual/en/5.0/`. Extensions and the manifest: `https://docs.blender.org/manual/en/latest/advanced/extensions/index.html`.
4. WebSearch only when the docs do not answer it, for example known bugs or behaviour changes.

If the answer might differ in the newest release you test on, fetch that version's page too and say whether it changed (or use `/compare-api-versions`).

## Output

- The signature or property with its type and default.
- One short example in house style.
- Any gotcha (context requirements, undo, threading, when it is read-only).
- The doc link.
