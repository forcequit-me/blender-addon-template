---
description: Run the after-change checklist on the add-on and report pass/fail per step
allowed-tools: Bash, Read, Grep, Glob
---

Run the after-change checklist on this add-on, from the repo root. `<BLENDER_MIN>` and `<BLENDER_LATEST>` are the paths in the "Blender installs" section of `CLAUDE.md`; the package is `ADDON_FOLDER` in `build.py`. This command checks and reports; fix nothing unless asked.

Start with `git log --oneline -5` and `git status --short` (if the repo uses git) so you know what changed.

1. **Tests on BLENDER_MIN and BLENDER_LATEST.** Follow `/test-addon`: operator list current, smoke test prints `SMOKE OK` on both, then every other test in `tests/`.

2. **Rebuild clean.** `python build.py package --clean`; `build/` must hold one zip at the bl_info version. If you ship on the extensions platform, also `python build.py package --extension`. Then the fresh-install test from `/test-addon` on each zip.

3. **README matches the panel.** The add-on's README is `README.md`, or `ADDON_README.md` while `/setup-addon` has not run yet (the root `README.md` then describes the template). Walk every `draw()` in `panels.py` and `preferences.py` in the order a user meets them (sub-panels by `bl_order`). "How to use" must list every visible control, in that order, with the exact label. List each mismatch. The README follows `docs/README Spec.md`, and "Why I made this" is not a placeholder any more.

4. **Tooltips and description true.** Every `bl_description`, operator docstring, property `description` and panel docstring says what the code does now, in one line. bl_info `"description"` and the manifest `tagline` are still true. No em dashes (U+2014) in README or tooltips; the `check_edit.py` hook flags them on edit, and a search of `README.md` and the package for the character catches older ones.

5. **bl_info and manifest in step.** Manifest `name`, `version` and `blender_version_min` match bl_info `name`, `version` and `blender`. Nothing left from the placeholders (`addon_name`, `ADDON_NAME_`, `Addon Name`, `Your Name`, and text marked `PLACEHOLDER`) outside `.claude/`, `CLAUDE.md` and `docs/`, unless this is still the bare template.

6. **Links footer fits the build.** Legacy: `WEBSITE_URL` and `BUG_REPORT_URL` in `panels.py` are real URLs, or the footer draws nothing. Extensions: the footer, `draw_links` and the preferences call are gone (rule 6.1), and nothing modifies the OS or other add-ons (rule 3.9).

7. **Committed.** `git status --short` is clean. Uncommitted work: report what, do not commit. Push only when asked.

## Report

```
## Check: <Addon Name> v<version>
| # | Step | Result | Notes |
|---|---|---|---|
| 1 | Tests BLENDER_MIN / BLENDER_LATEST | PASS | smoke + test_functional |
| 2 | Build + fresh install | PASS | Addon-Name-v0.1.0.zip |
| 3 | README matches panel | FAIL | "Clear All" is "Clear List" in the panel |
...
```
End with the list of fixes needed, most important first, and the undo checks to do by hand in a real Blender window.
