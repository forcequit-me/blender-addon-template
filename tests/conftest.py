"""
Pytest configuration and shared fixtures for Blender addon tests.

This file is automatically loaded by pytest and provides:
- Common fixtures for test setup/teardown
- Blender environment detection
- Mock helpers for unit tests
"""

import sys
import pytest
from unittest.mock import MagicMock
from pathlib import Path

# =============================================================================
# BLENDER DETECTION
# =============================================================================

def is_blender_available():
    """Check if running inside Blender."""
    try:
        import bpy
        return True
    except ImportError:
        return False

IN_BLENDER = is_blender_available()

# =============================================================================
# PATH SETUP
# =============================================================================

# Add addon to path for imports
ADDON_PATH = Path(__file__).parent.parent / "addon_name"
if str(ADDON_PATH.parent) not in sys.path:
    sys.path.insert(0, str(ADDON_PATH.parent))

# =============================================================================
# SKIP DECORATORS
# =============================================================================

requires_blender = pytest.mark.skipif(
    not IN_BLENDER,
    reason="Test requires Blender environment"
)

skip_in_blender = pytest.mark.skipif(
    IN_BLENDER,
    reason="Test should not run in Blender"
)

# =============================================================================
# BLENDER FIXTURES (only available when running in Blender)
# =============================================================================

if IN_BLENDER:
    import bpy

    @pytest.fixture
    def empty_scene():
        """
        Reset Blender to an empty scene.

        Use this fixture when you need a clean slate without any objects.
        """
        bpy.ops.wm.read_factory_settings(use_empty=True)
        yield
        # Cleanup
        bpy.ops.wm.read_factory_settings(use_empty=True)

    @pytest.fixture
    def default_scene():
        """
        Reset Blender to default startup scene.

        Use this fixture when you need the default cube, camera, light.
        """
        bpy.ops.wm.read_factory_settings(use_empty=False)
        yield
        bpy.ops.wm.read_factory_settings(use_empty=True)

    @pytest.fixture
    def cube():
        """
        Create a cube and return it.

        The cube is automatically cleaned up after the test.
        """
        bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
        obj = bpy.context.active_object
        yield obj
        # Cleanup
        if obj and obj.name in bpy.data.objects:
            bpy.data.objects.remove(obj)

    @pytest.fixture
    def multiple_cubes():
        """
        Create multiple cubes for testing batch operations.

        Returns a list of 5 cube objects.
        """
        bpy.ops.wm.read_factory_settings(use_empty=True)
        cubes = []
        for i in range(5):
            bpy.ops.mesh.primitive_cube_add(location=(i * 2, 0, 0))
            cubes.append(bpy.context.active_object)
        yield cubes
        # Cleanup
        for obj in cubes:
            if obj and obj.name in bpy.data.objects:
                bpy.data.objects.remove(obj)

    @pytest.fixture
    def mesh_object():
        """
        Create a mesh object with editable geometry.

        Returns an object with a simple mesh that can be modified.
        """
        bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.ops.mesh.primitive_plane_add()
        obj = bpy.context.active_object
        yield obj
        if obj and obj.name in bpy.data.objects:
            bpy.data.objects.remove(obj)

    @pytest.fixture
    def selected_objects(multiple_cubes):
        """
        Create and select multiple objects.

        Returns a list of selected objects with the last one active.
        """
        for obj in multiple_cubes:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = multiple_cubes[-1]
        return multiple_cubes

    @pytest.fixture
    def addon_prefs():
        """
        Get addon preferences.

        Returns the addon's preference object, or None if not registered.
        """
        addon_name = "addon_name"  # Update with your addon's module name
        prefs = bpy.context.preferences.addons.get(addon_name)
        if prefs:
            return prefs.preferences
        return None

# =============================================================================
# MOCK FIXTURES (available without Blender)
# =============================================================================

@pytest.fixture
def mock_bpy():
    """
    Create a mock bpy module for unit testing without Blender.

    Usage:
        def test_something(mock_bpy):
            mock_bpy.context.active_object.name = "TestCube"
            # ... test code that imports bpy
    """
    mock = MagicMock()

    # Setup common mock attributes
    mock.context.active_object = MagicMock()
    mock.context.active_object.name = "MockObject"
    mock.context.active_object.type = "MESH"
    mock.context.active_object.location = [0, 0, 0]

    mock.context.selected_objects = []
    mock.context.scene.name = "MockScene"
    mock.context.view_layer.objects.active = mock.context.active_object

    mock.app.version = (4, 0, 0)
    mock.app.version_string = "4.0.0"

    return mock

@pytest.fixture
def mock_context():
    """
    Create a mock Blender context.

    Useful for testing functions that take context as a parameter.
    """
    context = MagicMock()
    context.active_object = MagicMock()
    context.active_object.name = "MockObject"
    context.active_object.type = "MESH"
    context.selected_objects = []
    context.scene = MagicMock()
    context.view_layer = MagicMock()
    return context

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def assert_operator_exists(operator_idname: str):
    """
    Assert that an operator is registered.

    Args:
        operator_idname: The operator ID (e.g., "object.my_operator")
    """
    if not IN_BLENDER:
        pytest.skip("Requires Blender")

    import bpy
    category, name = operator_idname.split(".")
    ops_category = getattr(bpy.ops, category, None)
    assert ops_category is not None, f"Operator category '{category}' not found"

    op = getattr(ops_category, name, None)
    assert op is not None, f"Operator '{operator_idname}' not registered"

def assert_panel_exists(panel_idname: str):
    """
    Assert that a panel is registered.

    Args:
        panel_idname: The panel ID (e.g., "VIEW3D_PT_my_panel")
    """
    if not IN_BLENDER:
        pytest.skip("Requires Blender")

    import bpy
    panel = getattr(bpy.types, panel_idname, None)
    assert panel is not None, f"Panel '{panel_idname}' not registered"

# =============================================================================
# PYTEST CONFIGURATION
# =============================================================================

def pytest_configure(config):
    """Add custom markers."""
    config.addinivalue_line(
        "markers", "blender: mark test as requiring Blender environment"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )

def pytest_collection_modifyitems(config, items):
    """Modify test collection based on environment."""
    if not IN_BLENDER:
        skip_blender = pytest.mark.skip(reason="Requires Blender environment")
        for item in items:
            if "blender" in item.keywords:
                item.add_marker(skip_blender)
