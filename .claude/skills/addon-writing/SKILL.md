---
name: addon-writing
description: How every word in the add-on is written, following this template's defaults - the 7-section README, tooltips, bl_info description and manifest tagline, report messages, UI labels and code comments, in a plain second-person voice with no em dashes and no AI attribution. Use when writing or editing a README, a tooltip or property description, an operator report, a label, a code comment, or when reviewing any of these after a code change.
---

# Add-on writing

Source of truth: `docs/README Spec.md`. If it and this skill disagree, the spec wins. These are the template's default house style; change the spec if you want a different one, and this skill follows it.

## Voice (everything a user reads)

- Plain, short sentences. Second person: "you", "your file".
- Say what happens. "Deletes every empty of the ticked types", not "allows you to manage empties efficiently".
- No hype: no "powerful", "seamless", "effortless", "blazing", "ultimate", "game-changer".
- **No em dashes.** Use a full stop, a comma or a colon. Check with a search for `—` before finishing. En dashes as dashes are out too. The `check_edit.py` hook flags em dashes in READMEs and in tooltip lines.
- Name controls exactly as they appear on screen, in bold in the README.
- Run a prose clean-up pass (a "stop slop" style skill, if you have one) over any README or long text.

## README: seven sections, in this order

The add-on's user README is `README.md` at the repo root; `build.py` copies it into the zip. Until `/setup-addon` has run, the root `README.md` describes the template and the add-on's README skeleton is `ADDON_README.md` (build.py ships that one while it exists). `/setup-addon` moves it over `README.md`.

```markdown
# Addon Name

One sentence saying what it does for you.

## Why I made this

(The author's own words. Never write or rewrite this paragraph.)

## What it does

(Short, in user words. What changes in their file, what is kept, how to undo. No implementation talk.)

## Install

Edit > Preferences > Add-ons > arrow menu > Install from Disk, pick the zip, tick it on.
Needs Blender 5.0 or newer.

## How to use

Press N in the 3D Viewport and open the Addon Name tab.

- **Example Button**: what happens when you click it, and what the status bar reports.
- ...every visible control, in the order the user meets it, one line each...
- Two icon buttons sit at the bottom of the panel: the link icon opens my website, the **GitHub** icon (or **?**, if the page isn't on GitHub) opens the bug report page.

Edit > Preferences > Add-ons > Addon Name holds the defaults:

- ...each preference, same format...

## Bugs and feedback

Found a bug? <bug report URL>. The bug report button at the bottom of the panel goes there too.

## Thanks

(Credit the people who helped, in your own words. Leave the section out if there is no one to thank.)
```

Rules:

- Title is the plain display name, no prefixes.
- **Why I made this** belongs to the author. For a new add-on, leave a clear placeholder and ask for it. Keep existing text word for word.
- **Install** says how the version you ship is installed. Legacy zip: the Install from Disk line above. Extensions platform: "Edit > Preferences > Get Extensions, search for Addon Name, click Install." If you ship both, give both, platform first.
- The line about the two icon buttons belongs only in a legacy build that shows the links footer. An extensions build has no footer (rule 6.1, see `blender-version-targeting`), so the README shipped with it must not mention one.
- Leave out: version lines, changelogs, build or zip instructions, test notes, an "Author:" line, anything the user cannot see or do.
- How to use must match the panel after every UI change: every visible control, in screen order, with its exact label. Nested controls are indented under the section that reveals them.

## Tooltips

Tooltips are the operator docstring or `bl_description`, and every property `description`. One line, same voice, saying what happens when you click or what the setting changes. It must match the code as it is now.

```python
class ADDON_NAME_OT_delete_empties(bpy.types.Operator):
    """Delete every empty of the ticked types in the whole file, skipping the exclude list"""

render_check: BoolProperty(
    name="Ask Before Rendering",
    description="Confirm which preset you are about to render. Cancel renders nothing",
)
```

| Weak | Better |
| --- | --- |
| "Execute the cleanup operation" | "Delete unused data blocks, following the settings in the sidebar panel" |
| "Toggle list visibility" | "Fold or unfold the exclude list" |
| "Enables recursive mode" | "Keep going until no new unused data blocks come loose" |
| "Operator for parenting" | "Parent the selected objects to the active object" |

- Say the consequence the user might not expect: "Asks you to confirm first", "This one is the same in every file", "The ticks belong to the scene you are in".
- Pick one convention for the final full stop (the template's docstrings leave it off) and keep it across the add-on. Two sentences are fine when the second is a consequence.
- Enum items get a description too; it is the tooltip for each option.
- Internal operators (`bl_options` has `'INTERNAL'`) still get a docstring, because it shows when hovering the button that calls them.

## bl_info description and manifest tagline

`description` is one user-facing sentence in the same voice. It shows in Blender's add-on list. The manifest `tagline` is its short form: 64 characters at most, no punctuation at the end.

- Good: "One click removes every data block your file no longer uses"
- Good: "Line up the selected objects along any axis, with even gaps, in one click."
- Bad: "An addon for advanced material management workflows"

## Report messages

What happened, with numbers, and what was skipped and why: `f"Removed {count} empties"`, `"Parented 212, skipped 3 (loop), 14 excluded"`. `'WARNING'` when nothing happened or something was skipped, with the reason: "No empties selected". Never "Success!" or "Done".

## Labels

Buttons are verbs or verb phrases in Title Case: "Save Current as Preset", "Add Selected", "Clear All". Status text is a plain sentence without a full stop: "Every preset renders here". Empty states say the next step.

## Code comments

- Explain **why**, never **what**. The code already says what.
- Good: `# Left, or the toggle stretches across the row and strands its own label out in the middle of the panel.` / `# Deferred to the first event-loop tick. During start-up registration the add-on preferences and the user keyconfig are not reliably loaded yet.`
- Bad: `# Loop over the objects`, `# Set the value`, `# This function returns the count`.
- No narration of changes ("# Changed to fix bug", "# New approach"), no commented-out code, no TODO without a reason.
- Docstrings: one line saying what the function returns or does, more only for a real constraint.
- Record a hard-won fact next to the code it protects: a Blender quirk, an API that behaves unexpectedly, a measured cost.

## No attribution

Never add AI attribution anywhere: not in code, comments, docstrings, READMEs, commit messages, PR text, file headers. No "Generated by", no "Co-authored-by". The work is the author's. `check_edit.py` flags it in files; `guard_commit.py` (off by default) can block it in commits.
