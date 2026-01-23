"""Utility functions for the addon."""

import bpy
import bmesh
from mathutils import Vector, Matrix


def get_selected_objects(context, obj_type=None):
    """
    Get selected objects, optionally filtered by type.

    Args:
        context: Blender context
        obj_type: Optional object type filter ('MESH', 'CURVE', etc.)

    Returns:
        List of selected objects
    """
    objects = context.selected_objects

    if obj_type:
        objects = [obj for obj in objects if obj.type == obj_type]

    return objects


def get_active_mesh(context):
    """
    Get the active object's mesh data.

    Args:
        context: Blender context

    Returns:
        Mesh data or None
    """
    obj = context.active_object

    if obj and obj.type == 'MESH':
        return obj.data

    return None


def create_bmesh_from_object(obj, apply_modifiers=False):
    """
    Create a BMesh from an object.

    Args:
        obj: Blender object
        apply_modifiers: Whether to apply modifiers

    Returns:
        BMesh instance (caller must free with bm.free())
    """
    bm = bmesh.new()

    if apply_modifiers:
        depsgraph = bpy.context.evaluated_depsgraph_get()
        obj_eval = obj.evaluated_get(depsgraph)
        bm.from_mesh(obj_eval.data)
    else:
        bm.from_mesh(obj.data)

    return bm


def apply_bmesh_to_object(bm, obj):
    """
    Apply BMesh changes back to an object.

    Args:
        bm: BMesh instance
        obj: Target object
    """
    bm.to_mesh(obj.data)
    obj.data.update()


def calculate_bounds(obj):
    """
    Calculate the bounding box dimensions of an object.

    Args:
        obj: Blender object

    Returns:
        Tuple of (min_point, max_point, dimensions)
    """
    bbox = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]

    min_point = Vector((
        min(v.x for v in bbox),
        min(v.y for v in bbox),
        min(v.z for v in bbox),
    ))

    max_point = Vector((
        max(v.x for v in bbox),
        max(v.y for v in bbox),
        max(v.z for v in bbox),
    ))

    dimensions = max_point - min_point

    return min_point, max_point, dimensions


def ensure_object_mode(context):
    """
    Ensure we're in object mode.

    Args:
        context: Blender context

    Returns:
        Previous mode if changed, None otherwise
    """
    if context.active_object and context.active_object.mode != 'OBJECT':
        previous_mode = context.active_object.mode
        bpy.ops.object.mode_set(mode='OBJECT')
        return previous_mode

    return None


def restore_mode(context, mode):
    """
    Restore a previous mode.

    Args:
        context: Blender context
        mode: Mode to restore
    """
    if mode and context.active_object:
        bpy.ops.object.mode_set(mode=mode)


class UndoHandler:
    """Context manager for grouping operations in a single undo step."""

    def __init__(self, name="Addon Operation"):
        self.name = name

    def __enter__(self):
        bpy.ops.ed.undo_push(message=self.name)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            bpy.ops.ed.undo()
            return False
        return True
