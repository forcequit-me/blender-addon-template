#!/usr/bin/env python3
"""
Blender Addon Build Script

Automates packaging, versioning, and release preparation for Blender addons.

Usage:
    python build.py package              # Create distribution ZIP
    python build.py package --clean      # Clean build folder first
    python build.py version              # Show current version
    python build.py version 1.2.0        # Set new version
    python build.py version --bump patch # Bump patch version (1.0.0 -> 1.0.1)
    python build.py version --bump minor # Bump minor version (1.0.0 -> 1.1.0)
    python build.py version --bump major # Bump major version (1.0.0 -> 2.0.0)
    python build.py validate             # Validate addon structure
    python build.py clean                # Remove build artifacts
"""

import argparse
import ast
import os
import re
import shutil
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

# =============================================================================
# CONFIGURATION - Edit these for your addon
# =============================================================================

# Name of your addon folder (the folder that gets installed in Blender)
ADDON_FOLDER = "addon_name"

# Files/folders to EXCLUDE from the package
EXCLUDE_PATTERNS = [
    "__pycache__",
    "*.pyc",
    "*.pyo",
    ".git",
    ".gitignore",
    ".DS_Store",
    "Thumbs.db",
    "*.blend1",
    "*.blend2",
    ".vscode",
    ".idea",
    "tests",
    "*.log",
    ".env",
]

# Files/folders to INCLUDE at the root level (outside addon folder)
# These get packaged alongside the addon folder
INCLUDE_ROOT_FILES = [
    # "LICENSE",
    # "README.md",
]

# Build output directory
BUILD_DIR = "build"

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.resolve()


def get_addon_path() -> Path:
    """Get the addon source directory."""
    return get_project_root() / ADDON_FOLDER


def get_build_path() -> Path:
    """Get the build output directory."""
    return get_project_root() / BUILD_DIR


def get_init_path() -> Path:
    """Get the __init__.py path."""
    return get_addon_path() / "__init__.py"


def should_exclude(path: Path) -> bool:
    """Check if a path should be excluded from packaging."""
    name = path.name

    for pattern in EXCLUDE_PATTERNS:
        if pattern.startswith("*"):
            # Wildcard pattern (e.g., *.pyc)
            if name.endswith(pattern[1:]):
                return True
        else:
            # Exact match
            if name == pattern:
                return True

    return False


def parse_bl_info(init_content: str) -> Optional[dict]:
    """Parse bl_info dictionary from __init__.py content."""
    # Find bl_info assignment
    match = re.search(r'bl_info\s*=\s*(\{[^}]+\})', init_content, re.DOTALL)
    if not match:
        return None

    try:
        # Safely evaluate the dictionary
        bl_info_str = match.group(1)
        bl_info = ast.literal_eval(bl_info_str)
        return bl_info
    except (SyntaxError, ValueError) as e:
        print(f"Error parsing bl_info: {e}")
        return None


def get_version() -> Optional[Tuple[int, int, int]]:
    """Get current addon version from bl_info."""
    init_path = get_init_path()

    if not init_path.exists():
        print(f"Error: {init_path} not found")
        return None

    content = init_path.read_text(encoding='utf-8')
    bl_info = parse_bl_info(content)

    if bl_info and 'version' in bl_info:
        return tuple(bl_info['version'])

    return None


def set_version(new_version: Tuple[int, int, int]) -> bool:
    """Set addon version in bl_info."""
    init_path = get_init_path()

    if not init_path.exists():
        print(f"Error: {init_path} not found")
        return False

    content = init_path.read_text(encoding='utf-8')

    # Replace version tuple in bl_info
    pattern = r'("version"\s*:\s*\()(\d+,\s*\d+,\s*\d+)(\))'
    replacement = f'\\g<1>{new_version[0]}, {new_version[1]}, {new_version[2]}\\g<3>'

    new_content, count = re.subn(pattern, replacement, content)

    if count == 0:
        print("Error: Could not find version in bl_info")
        return False

    init_path.write_text(new_content, encoding='utf-8')
    return True


def bump_version(bump_type: str) -> Optional[Tuple[int, int, int]]:
    """Bump version by type (major, minor, patch)."""
    current = get_version()

    if not current:
        return None

    major, minor, patch = current

    if bump_type == 'major':
        return (major + 1, 0, 0)
    elif bump_type == 'minor':
        return (major, minor + 1, 0)
    elif bump_type == 'patch':
        return (major, minor, patch + 1)
    else:
        print(f"Error: Unknown bump type '{bump_type}'")
        return None


def version_string(version: Tuple[int, int, int]) -> str:
    """Convert version tuple to string."""
    return f"{version[0]}.{version[1]}.{version[2]}"


# =============================================================================
# COMMANDS
# =============================================================================

def cmd_clean():
    """Remove build artifacts."""
    build_path = get_build_path()

    if build_path.exists():
        shutil.rmtree(build_path)
        print(f"Removed: {build_path}")
    else:
        print("Nothing to clean")

    # Also clean __pycache__ directories
    addon_path = get_addon_path()
    pycache_count = 0

    for pycache in addon_path.rglob("__pycache__"):
        shutil.rmtree(pycache)
        pycache_count += 1

    if pycache_count > 0:
        print(f"Removed {pycache_count} __pycache__ directories")


def cmd_validate() -> bool:
    """Validate addon structure and bl_info."""
    print("Validating addon structure...")
    errors = []
    warnings = []

    addon_path = get_addon_path()
    init_path = get_init_path()

    # Check addon folder exists
    if not addon_path.exists():
        errors.append(f"Addon folder not found: {addon_path}")
        print("\n".join(f"ERROR: {e}" for e in errors))
        return False

    # Check __init__.py exists
    if not init_path.exists():
        errors.append(f"__init__.py not found: {init_path}")
    else:
        content = init_path.read_text(encoding='utf-8')
        bl_info = parse_bl_info(content)

        if not bl_info:
            errors.append("Could not parse bl_info dictionary")
        else:
            # Required bl_info fields
            required_fields = ['name', 'version', 'blender', 'category']
            for field in required_fields:
                if field not in bl_info:
                    errors.append(f"Missing required bl_info field: {field}")

            # Recommended fields
            recommended_fields = ['author', 'description', 'location']
            for field in recommended_fields:
                if field not in bl_info:
                    warnings.append(f"Missing recommended bl_info field: {field}")

            # Validate version format
            if 'version' in bl_info:
                version = bl_info['version']
                if not (isinstance(version, tuple) and len(version) == 3):
                    errors.append("bl_info 'version' should be a tuple of 3 integers")

            # Validate blender version format
            if 'blender' in bl_info:
                blender = bl_info['blender']
                if not (isinstance(blender, tuple) and len(blender) == 3):
                    errors.append("bl_info 'blender' should be a tuple of 3 integers")

        # Check for register/unregister functions
        if 'def register(' not in content:
            errors.append("Missing register() function")
        if 'def unregister(' not in content:
            errors.append("Missing unregister() function")

    # Print results
    if warnings:
        print("\nWarnings:")
        for w in warnings:
            print(f"  WARNING: {w}")

    if errors:
        print("\nErrors:")
        for e in errors:
            print(f"  ERROR: {e}")
        print(f"\nValidation FAILED with {len(errors)} error(s)")
        return False

    print("\nValidation PASSED")
    return True


def cmd_version(new_version: Optional[str] = None, bump: Optional[str] = None):
    """Show or set addon version."""
    if bump:
        # Bump version
        new_ver = bump_version(bump)
        if new_ver:
            if set_version(new_ver):
                print(f"Version bumped to {version_string(new_ver)}")
            else:
                print("Failed to update version")
                sys.exit(1)
    elif new_version:
        # Set specific version
        try:
            parts = [int(x) for x in new_version.split('.')]
            if len(parts) != 3:
                raise ValueError("Version must have 3 parts")
            new_ver = tuple(parts)
            if set_version(new_ver):
                print(f"Version set to {version_string(new_ver)}")
            else:
                print("Failed to update version")
                sys.exit(1)
        except ValueError as e:
            print(f"Error: Invalid version format '{new_version}' - {e}")
            print("Use format: MAJOR.MINOR.PATCH (e.g., 1.2.3)")
            sys.exit(1)
    else:
        # Show current version
        version = get_version()
        if version:
            print(f"Current version: {version_string(version)}")
        else:
            print("Could not determine version")
            sys.exit(1)


def cmd_package(clean_first: bool = False):
    """Package addon for distribution."""
    if clean_first:
        cmd_clean()

    # Validate first
    if not cmd_validate():
        print("\nPackaging aborted due to validation errors")
        sys.exit(1)

    print("\nPackaging addon...")

    project_root = get_project_root()
    addon_path = get_addon_path()
    build_path = get_build_path()

    # Get version for filename
    version = get_version()
    version_str = version_string(version) if version else "unknown"

    # Create build directory
    build_path.mkdir(exist_ok=True)

    # Generate output filename
    timestamp = datetime.now().strftime("%Y%m%d")
    zip_name = f"{ADDON_FOLDER}-v{version_str}.zip"
    zip_path = build_path / zip_name

    # Remove existing zip if present
    if zip_path.exists():
        zip_path.unlink()

    # Create ZIP file
    file_count = 0

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Add addon folder contents
        for file_path in addon_path.rglob('*'):
            if file_path.is_file() and not should_exclude(file_path):
                arcname = file_path.relative_to(project_root)
                zf.write(file_path, arcname)
                file_count += 1

        # Add root files if specified
        for root_file in INCLUDE_ROOT_FILES:
            root_path = project_root / root_file
            if root_path.exists():
                zf.write(root_path, root_file)
                file_count += 1

    # Report results
    zip_size = zip_path.stat().st_size
    size_str = f"{zip_size / 1024:.1f} KB" if zip_size < 1024 * 1024 else f"{zip_size / (1024 * 1024):.2f} MB"

    print(f"\nPackage created successfully!")
    print(f"  Output: {zip_path}")
    print(f"  Files:  {file_count}")
    print(f"  Size:   {size_str}")
    print(f"\nInstall in Blender:")
    print(f"  Edit > Preferences > Add-ons > Install > Select {zip_name}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Blender Addon Build Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python build.py package              Create distribution ZIP
  python build.py package --clean      Clean first, then package
  python build.py version              Show current version
  python build.py version 1.2.0        Set version to 1.2.0
  python build.py version --bump patch Bump patch version
  python build.py validate             Validate addon structure
  python build.py clean                Remove build artifacts
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Package command
    package_parser = subparsers.add_parser('package', help='Package addon for distribution')
    package_parser.add_argument('--clean', action='store_true', help='Clean build folder first')

    # Version command
    version_parser = subparsers.add_parser('version', help='Show or set version')
    version_parser.add_argument('new_version', nargs='?', help='New version (e.g., 1.2.0)')
    version_parser.add_argument('--bump', choices=['major', 'minor', 'patch'], help='Bump version')

    # Validate command
    subparsers.add_parser('validate', help='Validate addon structure')

    # Clean command
    subparsers.add_parser('clean', help='Remove build artifacts')

    args = parser.parse_args()

    if args.command == 'package':
        cmd_package(clean_first=args.clean)
    elif args.command == 'version':
        cmd_version(new_version=args.new_version, bump=args.bump)
    elif args.command == 'validate':
        success = cmd_validate()
        sys.exit(0 if success else 1)
    elif args.command == 'clean':
        cmd_clean()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
