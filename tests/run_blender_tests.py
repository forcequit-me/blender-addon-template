#!/usr/bin/env python3
"""
Run pytest tests inside Blender.

This script is designed to be run by Blender in background mode:
    blender --background --python tests/run_blender_tests.py

Optional arguments (after --):
    --test-file FILE    Run specific test file
    --verbose           Verbose output
    --exit-first        Stop on first failure

Examples:
    blender --background --python tests/run_blender_tests.py
    blender --background --python tests/run_blender_tests.py -- --test-file test_operators.py
    blender --background --python tests/run_blender_tests.py -- --verbose --exit-first
"""

import sys
import os
from pathlib import Path

def main():
    # Get the tests directory
    tests_dir = Path(__file__).parent.resolve()
    addon_dir = tests_dir.parent

    # Add paths for imports
    sys.path.insert(0, str(tests_dir))
    sys.path.insert(0, str(addon_dir))

    # Parse arguments (everything after --)
    args = []
    if '--' in sys.argv:
        args = sys.argv[sys.argv.index('--') + 1:]

    # Build pytest arguments
    pytest_args = [str(tests_dir)]

    # Default: verbose output
    pytest_args.append('-v')

    # Process custom arguments
    test_file = None
    for i, arg in enumerate(args):
        if arg == '--test-file' and i + 1 < len(args):
            test_file = args[i + 1]
        elif arg == '--verbose':
            pytest_args.append('-vv')
        elif arg == '--exit-first':
            pytest_args.append('-x')

    # If specific test file requested
    if test_file:
        pytest_args = [str(tests_dir / test_file), '-v']

    # Try to import and run pytest
    try:
        import pytest
    except ImportError:
        print("=" * 60)
        print("ERROR: pytest is not installed in Blender's Python")
        print("=" * 60)
        print()
        print("To install pytest in Blender's Python:")
        print()
        print("1. Find Blender's Python executable:")
        print("   - Windows: C:\\Program Files\\Blender Foundation\\Blender X.X\\X.X\\python\\bin\\python.exe")
        print("   - macOS: /Applications/Blender.app/Contents/Resources/X.X/python/bin/python3.X")
        print("   - Linux: /usr/share/blender/X.X/python/bin/python3.X")
        print()
        print("2. Install pytest:")
        print('   "<path_to_blender_python>" -m pip install pytest')
        print()
        print("Alternative: Run tests outside Blender for unit tests:")
        print("   python -m pytest tests/test_utils.py -v")
        print()
        sys.exit(1)

    # Enable addon if not already enabled
    try:
        import bpy
        addon_name = addon_dir.name

        # Ensure addon is in path
        if str(addon_dir.parent) not in bpy.utils.script_paths():
            # Try to register addon directory
            pass

        # Try to enable addon
        try:
            bpy.ops.preferences.addon_enable(module=addon_name)
            print(f"Enabled addon: {addon_name}")
        except Exception as e:
            print(f"Note: Could not enable addon '{addon_name}': {e}")
            print("Tests will run anyway - some may fail if addon isn't registered")

    except ImportError:
        print("Warning: bpy not available - running outside Blender")

    print()
    print("=" * 60)
    print("Running Blender Addon Tests")
    print("=" * 60)
    print(f"Test directory: {tests_dir}")
    print(f"Pytest args: {pytest_args}")
    print()

    # Run pytest
    exit_code = pytest.main(pytest_args)

    print()
    print("=" * 60)
    if exit_code == 0:
        print("All tests passed!")
    else:
        print(f"Tests failed with exit code: {exit_code}")
    print("=" * 60)

    # Exit Blender with the test result code
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
