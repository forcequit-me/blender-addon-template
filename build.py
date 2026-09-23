#!/usr/bin/env python3
"""Build the add-on zip.

    python build.py package [--clean]                       legacy zip, for Install from Disk
    python build.py package --extension [--clean] [--blender PATH]
                                                            extension zip, for extensions.blender.org
    python build.py validate                                check bl_info, manifest and README
    python build.py version [X.Y.Z]                         show the version, or set it in both places
    python build.py clean                                   delete build/ and __pycache__

The extension build runs `blender --command extension build`. Blender is found from --blender,
then the BLENDER environment variable, then PATH, then the newest standard install.
"""

import argparse
import ast
import glob
import os
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ADDON_FOLDER = "addon_name"
BUILD_DIR = "build"
EXCLUDE = {"__pycache__", ".git", ".vscode", ".idea", "build"}

ROOT = Path(__file__).parent.resolve()
ADDON = ROOT / ADDON_FOLDER
INIT = ADDON / "__init__.py"
MANIFEST = ADDON / "blender_manifest.toml"
# Until /setup-addon moves it over README.md, ADDON_README.md is the add-on's README and
# README.md describes the template.
README = ROOT / "ADDON_README.md"
if not README.is_file():
    README = ROOT / "README.md"


def bl_info():
    match = re.search(r"bl_info\s*=\s*(\{.*?\})", INIT.read_text(encoding="utf-8"), re.S)
    if not match:
        raise RuntimeError(f"No bl_info in {INIT}")
    return ast.literal_eval(match.group(1))


def manifest():
    # Only the flat `key = "value"` lines are needed, so no TOML parser is required.
    text = MANIFEST.read_text(encoding="utf-8")
    return dict(re.findall(r'^(\w+)\s*=\s*"([^"]*)"', text, re.M))


def dotted(parts):
    return ".".join(str(p) for p in parts)


def zip_stem():
    # "My Tool!" -> "My-Tool"
    name = re.sub(r"[^A-Za-z0-9 -]", "", bl_info()["name"])
    return re.sub(r"[\s-]+", "-", name).strip("-")


def validate():
    errors = []
    for path in (INIT, MANIFEST, README):
        if not path.is_file():
            errors.append(f"Missing {path}")

    if not errors:
        info, man = bl_info(), manifest()
        for key in ("name", "version", "blender", "category"):
            if key not in info:
                errors.append(f"Missing bl_info key: {key}")
        pairs = [
            ("name", info.get("name"), man.get("name")),
            ("version", dotted(info.get("version", ())), man.get("version")),
            ("blender", dotted(info.get("blender", ())), man.get("blender_version_min")),
        ]
        for key, a, b in pairs:
            if a != b:
                errors.append(f"bl_info {key} {a!r} does not match manifest {b!r}")

    for error in errors:
        print(f"ERROR: {error}")
    if not errors:
        print("Validation PASSED")
    return not errors


def clean():
    shutil.rmtree(ROOT / BUILD_DIR, ignore_errors=True)
    for pycache in ADDON.rglob("__pycache__"):
        shutil.rmtree(pycache)
    print("Cleaned")


def find_blender(given):
    candidates = [given, os.environ.get("BLENDER"), shutil.which("blender")]
    installs = glob.glob("C:/Program Files/Blender Foundation/Blender */blender.exe")
    installs.sort(key=lambda p: [int(n) for n in re.findall(r"\d+", Path(p).parent.name)])
    candidates += reversed(installs)
    candidates.append("/Applications/Blender.app/Contents/MacOS/Blender")
    for path in candidates:
        if path and Path(path).is_file():
            return path
    return None


def package_legacy(zip_path):
    count = 0
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in ADDON.rglob("*"):
            if not path.is_file() or any(p in EXCLUDE for p in path.parts):
                continue
            # A legacy install ignores the manifest; leaving it out avoids confusing the installer.
            if path.suffix in {".pyc", ".pyo", ".log"} or path.name == "blender_manifest.toml":
                continue
            zf.write(path, path.relative_to(ROOT))
            count += 1
        # Ship the add-on's README inside the package folder.
        zf.write(README, f"{ADDON_FOLDER}/README.md")
        count += 1
    print(f"Built {zip_path} ({count} files)")


def package_extension(zip_path, blender):
    panels = ADDON / "panels.py"
    if panels.is_file() and re.search(r'_URL\s*=\s*"[^"]+"', panels.read_text(encoding="utf-8")):
        print("WARNING: panels.py has links set. extensions.blender.org does not allow them; "
              "remove the links footer before uploading there.")
    exe = find_blender(blender)
    if not exe:
        sys.exit("ERROR: Blender not found. Pass --blender <path> or set the BLENDER environment variable.")
    subprocess.run([exe, "--factory-startup", "--command", "extension", "build",
                    "--source-dir", str(ADDON), "--output-filepath", str(zip_path)], check=True)
    print(f"Built {zip_path}")


def package(extension=False, clean_first=False, blender=None):
    if clean_first:
        clean()
    if not validate():
        sys.exit(1)
    build = ROOT / BUILD_DIR
    build.mkdir(exist_ok=True)
    suffix = "-extension" if extension else ""
    zip_path = build / f"{zip_stem()}-v{dotted(bl_info()['version'])}{suffix}.zip"
    zip_path.unlink(missing_ok=True)
    if extension:
        package_extension(zip_path, blender)
    else:
        package_legacy(zip_path)


def set_version(new):
    if not re.fullmatch(r"\d+\.\d+\.\d+", new):
        sys.exit("ERROR: version must look like 1.2.3")
    as_tuple = "(" + ", ".join(new.split(".")) + ")"
    INIT.write_text(re.sub(r'("version"\s*:\s*)\([^)]*\)', rf"\g<1>{as_tuple}",
                           INIT.read_text(encoding="utf-8"), count=1), encoding="utf-8")
    MANIFEST.write_text(re.sub(r'^version\s*=\s*"[^"]*"', f'version = "{new}"',
                               MANIFEST.read_text(encoding="utf-8"), count=1, flags=re.M),
                        encoding="utf-8")
    print(f"Version set to {new} in bl_info and blender_manifest.toml")


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")
    package_cmd = sub.add_parser("package")
    package_cmd.add_argument("--clean", action="store_true", help="empty build/ first")
    package_cmd.add_argument("--extension", action="store_true", help="build an extension zip")
    package_cmd.add_argument("--blender", help="path to the Blender executable")
    version_cmd = sub.add_parser("version")
    version_cmd.add_argument("new", nargs="?", help="new version, e.g. 1.2.0")
    sub.add_parser("validate")
    sub.add_parser("clean")

    args = parser.parse_args()
    if args.cmd == "package":
        package(args.extension, args.clean, args.blender)
    elif args.cmd == "version":
        if args.new:
            set_version(args.new)
        else:
            print(dotted(bl_info()["version"]))
    elif args.cmd == "validate":
        sys.exit(0 if validate() else 1)
    elif args.cmd == "clean":
        clean()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
