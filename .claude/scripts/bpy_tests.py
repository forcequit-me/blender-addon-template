"""Run add-on tests with PyPI's bpy module, for machines without a Blender app (cloud sessions).

    pip install bpy==5.2.3          # needs the Python that wheel targets (5.2: 3.13, 5.0: 3.11)
    python .claude/scripts/bpy_tests.py [add-on folder ...]     # default: this repo

Runs every tests/test_*.py of each add-on folder in its own process, with an empty throwaway
user folder so no installed add-on shadows the repo copy (what --factory-startup does for
the app). A good sign, not a replacement for running the real Blender.
"""

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def run(test, addon):
    with tempfile.TemporaryDirectory() as user:
        env = dict(os.environ, BLENDER_USER_RESOURCES=user)
        try:
            # Plain-Python tests (their own stand-in bpy, or none) run as they are. Blender tests
            # import bpy first: it puts addon_utils and the rest of Blender's modules on the path.
            text = test.read_text(encoding="utf-8", errors="replace")
            if "bpy_stub" in text or "import bpy" not in text:
                args = [str(test)]
            else:
                args = ["-c", f"import bpy, runpy; runpy.run_path({str(test)!r}, run_name='__main__')"]
            p = subprocess.run([sys.executable, *args], cwd=addon, env=env, capture_output=True,
                               text=True, errors="replace", timeout=900)
        except subprocess.TimeoutExpired:
            return False, "timed out after 15 minutes"
    out = (p.stdout + p.stderr).strip()
    # Each test ends by printing its OK line (SMOKE OK, ALL PASS, ... checks passed). Blender carries
    # on after a test's exception, so a traceback fails it too.
    done = [line for line in out.splitlines() if re.search(r"\b(OK|PASS|PASSED|passed)\b", line)]
    ok = p.returncode == 0 and bool(done) and "Traceback" not in out
    return ok, done[-1] if ok else out


def main():
    import bpy
    print(f"bpy {bpy.app.version_string}, Python {sys.version.split()[0]}")
    failed = 0
    for addon in (Path(a).resolve() for a in sys.argv[1:] or ["."]):
        for test in sorted((addon / "tests").glob("test_*.py")):
            ok, detail = run(test, addon)
            failed += not ok
            print(f"{'PASS' if ok else 'FAIL'}  {addon.name}/{test.name}  {detail if ok else ''}")
            if not ok:
                print("    " + "\n    ".join(detail.splitlines()[-25:]))
    print(f"{failed} failed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
