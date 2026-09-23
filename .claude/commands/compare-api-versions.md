---
description: Check whether an API behaves the same in the minimum Blender and a newer release, so code stays working on the minimum
argument-hint: "<API or feature> [version-a] [version-b]"
allowed-tools: Bash, Read, Grep, Glob, WebFetch
---

Compare `$ARGUMENTS` between two Blender versions. Default: `BLENDER_MIN` (the minimum) against `BLENDER_LATEST` (the newest you test on), both from the "Blender installs" section of `CLAUDE.md`. Use this when new code relies on an API you have not used before, or when a new Blender release comes out and the add-on needs checking against it.

## 1. Ask the installed Blenders directly

This is the reliable check: it reads the real RNA, not docs. Write a probe script to a temp or scratchpad folder, for example:
```python
import bpy
cls = bpy.types.Object                      # the class in question
props = {p.identifier: (p.type, getattr(p, "default", None)) for p in cls.bl_rna.properties}
print("has foo:", "foo" in props, props.get("foo"))
# enum items: [i.identifier for i in cls.bl_rna.properties["<enum>"].enum_items]
# operator args: bpy.ops.<cat>.<op>.get_rna_type().properties.keys()
```
Run it on each version:
```
"<BLENDER_MIN>" --background --factory-startup --python <probe.py>
"<BLENDER_LATEST>" --background --factory-startup --python <probe.py>
```
To compare against a release that is not in `CLAUDE.md`, install it (or unpack the portable build) and pass its path instead.

## 2. Read the docs for intent

`https://docs.blender.org/api/<version-a>/<page>.html` against `https://docs.blender.org/api/<version-b>/<page>.html`, and the release notes at `https://developer.blender.org/docs/release_notes/<version>/python_api/` for each release in between, for renames and removals.

## 3. Report

```
<API>: <version-a> vs <version-b>
Same | Changed: <what> | Only in <version-b> (cannot use while the minimum is <version-a>)
Evidence: probe output lines, doc links
What to do: <plain recommendation>
```

The add-on supports one range (the minimum and up), so the fix for a difference is code that works on both, not a version branch. If that is impossible, say so: it means raising the minimum version (bl_info `"blender"`, manifest `blender_version_min`, the `register()` guard and `BLENDER_MIN` together).
