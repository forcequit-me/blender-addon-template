---
description: Check this machine has everything the add-on workflow needs, and say how to fix what is missing
allowed-tools: Bash, Read, mcp__blender__get_addon_status
---

Check the dev environment and report each item as OK or MISSING with the fix. Do not install anything without asking.

| Check | How |
|---|---|
| Blender at `BLENDER_MIN` and `BLENDER_LATEST` | Read both paths from the "Blender installs" section of `CLAUDE.md`, then `"<BLENDER_MIN>" --version` and the same for `BLENDER_LATEST`. The two bracket the supported range. If a path is wrong on this machine, find the install (Windows `C:/Program Files/Blender Foundation/Blender X.Y/blender.exe`, macOS `/Applications/Blender.app/Contents/MacOS/Blender`, Linux wherever it was unpacked) and offer to update `CLAUDE.md`. |
| Python on PATH | `python --version` (or `python3` on macOS and Linux). Runs `build.py` and any plain-Python tests. |
| git | `git --version`. Optional, but `/check-addon` reads `git status`. |
| Blender MCP (for live testing, optional) | Call `mcp__blender__get_addon_status`. If it fails: `uvx --version` must work (the server runs as `uvx blender-mcp`), `claude mcp list` should show `blender`, and inside Blender the BlenderMCP add-on must be enabled and connected from its sidebar tab. |
| Repo layout | The repo root holds `CLAUDE.md`, `README.md`, `build.py`, `docs/`, `tests/` and the package folder named by `ADDON_FOLDER` in `build.py`. |

Then a quick proof that headless testing works, from the repo root:
```
"<BLENDER_MIN>" --background --factory-startup --python tests/test_blender_smoke.py
```
It should print `SMOKE OK`.

Still on the bare template (package `addon_name`)? Run `/setup-addon` next. For the day-to-day loop see `/live-dev`.
