"""After an edit, flag breaks of the house rules so they get fixed straight away.

Runs after every Edit or Write (PostToolUse). Looks at .py files and the add-on README
(README.md, or ADDON_README.md before setup) inside the project, except under .claude/, build/,
.git/ and cache or virtualenv folders. Exit 2 shows the warnings to Claude; the edit itself has
already happened. Any problem inside the hook itself exits 0, because a broken check must never
block normal work.

To change a rule, edit the patterns below. To switch the hook off, remove its entry from
.claude/settings.json.
"""
import json
import os
import re
import sys
from pathlib import Path

EM_DASH = "—"
READMES = {"README.md", "ADDON_README.md"}
SKIP_DIRS = {".claude", "build", ".git", "__pycache__", ".venv", "venv", "node_modules"}
# Lines that hold text a user sees: tooltips, labels, reports.
USER_TEXT = re.compile(r"\b(description|bl_description|bl_label|text|name)\s*=|\.report\(")
ATTRIBUTION = re.compile(r"co-authored-by|generated (by|with) (claude|ai)|written by claude", re.I)
USER_PATH = re.compile(r"[A-Za-z]:[\\/]+Users[\\/]+|/Users/[A-Za-z]|/home/[A-Za-z]")


def in_scope(path):
    if not (path.suffix == ".py" or path.name in READMES):
        return False
    project = os.environ.get("CLAUDE_PROJECT_DIR")
    if project:
        try:
            parts = path.resolve().relative_to(Path(project).resolve()).parts
        except ValueError:
            return False                      # outside the project: not ours to judge
    else:
        parts = path.parts
    return not any(p in SKIP_DIRS for p in parts[:-1])


def check(path, text):
    warnings = []
    for n, line in enumerate(text.splitlines(), 1):
        if EM_DASH in line and (path.name in READMES or USER_TEXT.search(line)):
            warnings.append(f"line {n}: em dash in user-facing text (house style: no em dashes)")
        if ATTRIBUTION.search(line):
            warnings.append(f"line {n}: AI attribution (not allowed anywhere)")
        if path.suffix == ".py" and USER_PATH.search(line):
            warnings.append(f"line {n}: hardcoded user folder path; use bpy.utils or bpy.path instead")
    return warnings


def main():
    try:
        # Read bytes: the Windows console encoding cannot decode every UTF-8 character.
        data = json.loads(sys.stdin.buffer.read().decode("utf-8", "replace"))
        file_path = (data.get("tool_input") or {}).get("file_path") or ""
        if not file_path:
            return 0
        path = Path(file_path)
        if not in_scope(path) or not path.is_file():
            return 0
        warnings = check(path, path.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return 0
    if not warnings:
        return 0
    shown = warnings[:10]
    more = f" (+{len(warnings) - 10} more)" if len(warnings) > 10 else ""
    print(f"House-rule check on {path.name}{more}:\n  " + "\n  ".join(shown), file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
