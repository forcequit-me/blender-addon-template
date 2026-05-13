"""
Operator tests for Blender addon.

These tests verify that operators are registered correctly and behave as expected.
Most tests require running inside Blender.

Run with:
    blender --background --python tests/run_blender_tests.py
"""

import pytest
from conftest import requires_blender, assert_operator_exists, IN_BLENDER

if IN_BLENDER:
    import bpy


# =============================================================================
# REGISTRATION TESTS
# =============================================================================

@requires_blender
class TestOperatorRegistration:
    """Test that all operators are properly registered."""

    def test_example_operator_registered(self):
        """Verify the example operator is registered."""
        assert_operator_exists("addon.example_operator")

    # Add more operator registration tests here:
    # def test_another_operator_registered(self):
    #     assert_operator_exists("object.another_operator")


# =============================================================================
# OPERATOR BEHAVIOR TESTS
# =============================================================================

@requires_blender
class TestExampleOperator:
    """Tests for the example operator."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Reset to empty scene before each test."""
        bpy.ops.wm.read_factory_settings(use_empty=True)
        yield

    def test_poll_fails_without_active_object(self):
        """Operator poll should fail when no object is active."""
        bpy.context.view_layer.objects.active = None
        # Note: poll() is accessed differently for testing
        assert bpy.ops.addon.example_operator.poll() == False

    def test_poll_succeeds_with_active_object(self, cube):
        """Operator poll should succeed with an active object."""
        assert bpy.ops.addon.example_operator.poll() == True

    def test_execute_returns_finished(self, cube):
        """Operator should return FINISHED on success."""
        result = bpy.ops.addon.example_operator()
        assert result == {'FINISHED'}

    def test_execute_modifies_object(self, cube):
        """Operator should move active object by `offset` on Z (default 1.0)."""
        original_z = cube.location.z
        bpy.ops.addon.example_operator()
        assert cube.location.z == pytest.approx(original_z + 1.0)

    def test_execute_with_custom_offset(self, cube):
        """Operator respects custom offset property."""
        original_z = cube.location.z
        bpy.ops.addon.example_operator(offset=2.5)
        assert cube.location.z == pytest.approx(original_z + 2.5)

    def test_operator_is_undoable(self, cube):
        """Operator should support undo (bl_options includes 'UNDO')."""
        original_z = cube.location.z

        bpy.ops.addon.example_operator()
        assert cube.location.z == pytest.approx(original_z + 1.0)

        bpy.ops.ed.undo()
        assert cube.location.z == pytest.approx(original_z)

    def test_operator_with_properties(self, cube):
        """Test operator with custom property values."""
        # If your operator has properties, test them:
        # result = bpy.ops.addon.example_operator(my_property=5.0)
        # assert result == {'FINISHED'}
        pass


# =============================================================================
# EDGE CASE TESTS
# =============================================================================

@requires_blender
class TestOperatorEdgeCases:
    """Test edge cases and error handling."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Reset scene before each test."""
        bpy.ops.wm.read_factory_settings(use_empty=True)
        yield

    def test_empty_selection(self):
        """Operator handles empty selection gracefully."""
        # Deselect all
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = None

        # Should not crash, poll should return False
        assert bpy.ops.addon.example_operator.poll() == False

    def test_wrong_object_type(self):
        """Operator handles non-mesh objects appropriately."""
        # Create an empty (not a mesh)
        bpy.ops.object.empty_add()
        empty = bpy.context.active_object

        # Depending on your operator's poll(), this may or may not work
        # Adjust test based on expected behavior
        # result = bpy.ops.addon.example_operator.poll()
        # assert result == False  # If operator requires mesh
        pass

    def test_edit_mode(self, cube):
        """Operator handles edit mode correctly."""
        # Switch to edit mode
        bpy.ops.object.mode_set(mode='EDIT')

        # Poll may fail in edit mode (depends on operator)
        # result = bpy.ops.addon.example_operator.poll()
        # assert result == False

        # Return to object mode
        bpy.ops.object.mode_set(mode='OBJECT')

    def test_multiple_selected_objects(self, selected_objects):
        """Operator works with multiple selected objects."""
        # Test behavior with multiple selections
        result = bpy.ops.addon.example_operator()
        assert result == {'FINISHED'}


# =============================================================================
# BATCH OPERATION TESTS
# =============================================================================

@requires_blender
class TestBatchOperations:
    """Test operators that work on multiple objects."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Reset scene before each test."""
        bpy.ops.wm.read_factory_settings(use_empty=True)
        yield

    def test_batch_operation_all_objects(self, multiple_cubes):
        """Operator affects all selected objects."""
        # Select all cubes
        for cube in multiple_cubes:
            cube.select_set(True)
        bpy.context.view_layer.objects.active = multiple_cubes[0]

        # Store original positions
        original_positions = [obj.location.z for obj in multiple_cubes]

        # Execute operator
        # bpy.ops.object.addon_batch_operator()

        # Verify all objects were affected
        # for i, cube in enumerate(multiple_cubes):
        #     assert cube.location.z != original_positions[i]
        pass

    def test_large_selection_performance(self):
        """Operator performs well with many objects."""
        import time

        # Create many objects
        objects = []
        for i in range(100):
            bpy.ops.mesh.primitive_cube_add(location=(i, 0, 0))
            objects.append(bpy.context.active_object)

        # Select all
        for obj in objects:
            obj.select_set(True)

        # Time the operation
        start = time.perf_counter()
        # bpy.ops.addon.example_operator()
        elapsed = time.perf_counter() - start

        # Assert reasonable performance (adjust threshold as needed)
        # assert elapsed < 1.0, f"Operation took too long: {elapsed:.2f}s"

        # Cleanup
        for obj in objects:
            bpy.data.objects.remove(obj)


# =============================================================================
# MODAL OPERATOR TESTS
# =============================================================================

@requires_blender
class TestModalOperator:
    """Tests for modal operators (if any)."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Reset scene before each test."""
        bpy.ops.wm.read_factory_settings(use_empty=True)
        yield

    def test_modal_operator_can_invoke(self, cube):
        """Modal operator can be invoked."""
        # Modal operators are harder to test automatically
        # This is a basic check that invoke doesn't crash
        # result = bpy.ops.object.addon_modal_operator('INVOKE_DEFAULT')
        # assert result == {'RUNNING_MODAL'}
        pass

    def test_modal_operator_can_cancel(self, cube):
        """Modal operator can be cancelled."""
        # Simulating ESC key to cancel modal is complex
        # Usually requires manual testing or custom test framework
        pass
