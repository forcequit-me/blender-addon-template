# Blender Add-on Template for Claude Code

A starting point for a Blender 5.0+ add-on, with a Claude Code dev kit that builds, tests and checks it for you.

You get a small working add-on (one operator, a sidebar panel, preferences, a headless smoke test), a build script that makes both a legacy zip and an extension zip, and a `.claude/` folder of slash commands, skills, agents and hooks that know how this project is laid out.

Once you run `/setup-addon`, this README is replaced by your add-on's own README, `ADDON_README.md`. Until then, `build.py` ships `ADDON_README.md` in the zip, never this file. Its structure is explained in `docs/README Spec.md`.

## Prerequisites

- [Claude Code](https://docs.claude.com/en/docs/claude-code/overview)
- Blender 5.0 or newer. Two versions installed is best, the oldest you support and the newest, so you can test both.
- Python 3.10 or newer on your PATH, to run `build.py` and the hooks.
- Optional: the [Blender MCP server](https://github.com/ahujasid/blender-mcp) for live testing in a running Blender. It needs [uv](https://docs.astral.sh/uv/) (for `uvx`) and the Blender MCP add-on enabled in Blender. The live commands (`/test-in-blender`, `/live-dev`, `/inspect-scene`, `/create-test-scene`) need it; everything else works without it.

## Quick start

1. Copy this folder, or use it as a GitHub template, and name the copy after your add-on.
2. Open `CLAUDE.md` and set the two Blender paths under "Blender installs" for your machine.
3. Open the folder in Claude Code and run `/setup-blender-dev` to check your machine has what it needs.
4. Run `/setup-addon`. It asks for your add-on's name and renames the placeholders (`addon_name`, `ADDON_NAME_`, `Addon Name`, `Your Name`) everywhere, including the folder.
5. Run `/test-addon`. The smoke test must print `SMOKE OK` on both Blenders.
6. Build something: `/new-operator`, `/new-panel`, or just describe what you want.
7. `/check-addon` before you ship, then `/build`.

Without Claude Code, the same steps by hand:

```
blender --background --factory-startup --python tests/test_blender_smoke.py
python build.py package --clean
python build.py package --extension --clean --blender "<path to blender>"
```

## Legacy zip or extension

Both are supported from the same code. bl_info and `blender_manifest.toml` carry the same name, version and minimum Blender, and the tests fail if they drift apart.

| | Legacy zip | Extension |
|---|---|---|
| Command | `python build.py package` | `python build.py package --extension` |
| Installed from | Preferences > Add-ons > Install from Disk | Preferences > Get Extensions, or extensions.blender.org |
| Links footer | allowed | remove it first (platform rules 6.1 and 3.9) |

The links footer is an optional row of icon buttons (your website, your bug report page) at the bottom of the panel and the preferences. Set `WEBSITE_URL` and `BUG_REPORT_URL` in `panels.py` to show it. It draws nothing while both are empty.

## Commands

| Command | What it does |
|---|---|
| `/setup-addon` | Rename the template's placeholders to your add-on's names |
| `/setup-blender-dev` | Check this machine has everything the workflow needs |
| `/new-operator` | Add an operator using the template's patterns |
| `/new-panel` | Add a panel or sub-panel |
| `/test-addon` | Run the headless tests on both Blenders |
| `/check-addon` | Run the after-change checklist from CLAUDE.md and report pass or fail per step |
| `/build` | Build the zip with build.py and check what is in it |
| `/bump-version` | Set a new version in bl_info and the manifest together, then rebuild |
| `/test-in-blender` | Test the operators in your running Blender (needs the MCP) |
| `/live-dev` | Edit, reload live in the running Blender, check, repeat (needs the MCP) |
| `/inspect-scene` | Read the running Blender's scene state, for debugging (needs the MCP) |
| `/create-test-scene` | Build a scratch test scene in the running Blender (needs the MCP) |
| `/docs-lookup` | Look up the Blender Python API or manual |
| `/api-example` | Find a working code example and prove it runs |
| `/compare-api-versions` | Check an API behaves the same on your oldest and newest Blender |
| `/add-performance-metrics` | Time an operator or handler to find where it is slow, then remove the timing code |

## Skills

Claude loads these on its own when a task calls for them.

| Skill | Covers |
|---|---|
| `addon-architecture` | Package layout, registration, preferences, storing references |
| `addon-writing` | README, tooltips, labels, report messages, comments |
| `blender-api-patterns` | Core bpy patterns and the API traps |
| `blender-ui-patterns` | Panels, fold boxes, dialogs, the links footer |
| `blender-version-targeting` | Setting a minimum Blender, legacy versus extension |
| `blender-documentation` | Where to look things up |
| `blender-mcp-workflows` | Using the Blender MCP for live checks |
| `blender-performance` | Blender-specific speed patterns |
| `performance-optimization` | Measuring before optimizing |
| `threading-async` | Timers, background work, not freezing Blender |

## Agents

Claude hands work to these when it fits, or you can ask for one by name.

| Agent | Does |
|---|---|
| `code-reviewer` | Reviews changed code against CLAUDE.md |
| `blender-api-expert` | Checks bpy usage against the Blender 5.x API |
| `ui-designer` | Reviews the panel and preferences layout, and the README walkthrough |
| `addon-tester` | Runs and writes headless tests |
| `blender-live-tester` | Tests in the running Blender through the MCP |
| `performance-auditor` | Finds slow code and ranks fixes by impact |

## Hooks

Set in `.claude/settings.json`.

- `check_edit.py` is **on**. After every edit it flags house-style breaks (for example an em dash in user-facing text) so Claude fixes them straight away. To turn it off, remove its `PostToolUse` entry.
- `guard_commit.py` is **off**. It blocks a git commit whose message credits an AI tool, such as a co-author trailer. To switch it on, add this `PreToolUse` entry next to `PostToolUse` in `.claude/settings.json`:

```json
"PreToolUse": [
  {
    "matcher": "Bash|PowerShell",
    "hooks": [
      {
        "type": "command",
        "command": "H=\"${CLAUDE_PROJECT_DIR}/.claude/hooks/guard_commit.py\"; [ -f \"$H\" ] || exit 0; if [ \"$OS\" = \"Windows_NT\" ]; then P=python; else P=python3; fi; \"$P\" \"$H\""
      }
    ]
  }
],
```

## House style

The writing rules in `docs/README Spec.md` and the code rules in `CLAUDE.md` are this template's defaults: plain second-person text, one-line tooltips that say what a click does, no em dashes, comments that say why. Change them if you like. Claude follows whatever those files say.

## Layout

```
addon_name/           the add-on (bl_info, manifest, operators, properties, panels, preferences)
  links.py            the links footer's open_link operator and the GitHub icon loader
  icons/              github.png and its Octicons licence
build.py              builds the legacy and extension zips
tests/                headless smoke test
docs/README Spec.md   how the README and tooltips are written
CLAUDE.md             the guide Claude reads first
.claude/              commands, skills, agents, hooks
.mcp.json             Blender MCP server
```
