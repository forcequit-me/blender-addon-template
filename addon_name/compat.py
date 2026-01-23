"""Version compatibility wrappers for multi-version Blender support."""

import bpy

# Blender version tuple for easy comparison
BLENDER_VERSION = bpy.app.version
BLENDER_VERSION_STRING = ".".join(map(str, BLENDER_VERSION[:2]))


def is_blender_4():
    """Check if running Blender 4.0 or newer."""
    return BLENDER_VERSION >= (4, 0, 0)


def is_blender_3():
    """Check if running Blender 3.x."""
    return (3, 0, 0) <= BLENDER_VERSION < (4, 0, 0)


def is_blender_28():
    """Check if running Blender 2.80-2.93."""
    return (2, 80, 0) <= BLENDER_VERSION < (3, 0, 0)


# =============================================================================
# Node Tree Socket Compatibility (Changed in 4.0)
# =============================================================================

def create_node_socket(node_tree, name, socket_type, in_out='INPUT'):
    """
    Create a socket on a node tree (input or output).

    Args:
        node_tree: The node tree (material, geometry nodes, etc.)
        name: Socket name
        socket_type: Socket type ('NodeSocketFloat', 'NodeSocketVector', etc.)
        in_out: 'INPUT' or 'OUTPUT'

    Returns:
        The created socket
    """
    if BLENDER_VERSION >= (4, 0, 0):
        # Blender 4.0+: Use interface.new_socket()
        return node_tree.interface.new_socket(
            name=name,
            socket_type=socket_type,
            in_out=in_out
        )
    else:
        # Blender 3.x and earlier: Use inputs/outputs.new()
        if in_out == 'INPUT':
            return node_tree.inputs.new(socket_type, name)
        else:
            return node_tree.outputs.new(socket_type, name)


def remove_node_socket(node_tree, socket):
    """
    Remove a socket from a node tree.

    Args:
        node_tree: The node tree
        socket: The socket to remove
    """
    if BLENDER_VERSION >= (4, 0, 0):
        node_tree.interface.remove(socket)
    else:
        if socket.is_output:
            node_tree.outputs.remove(socket)
        else:
            node_tree.inputs.remove(socket)


def get_node_tree_sockets(node_tree, in_out='INPUT'):
    """
    Get all sockets of a node tree.

    Args:
        node_tree: The node tree
        in_out: 'INPUT' or 'OUTPUT'

    Returns:
        List of sockets
    """
    if BLENDER_VERSION >= (4, 0, 0):
        return [item for item in node_tree.interface.items_tree
                if item.item_type == 'SOCKET' and item.in_out == in_out]
    else:
        if in_out == 'INPUT':
            return list(node_tree.inputs)
        else:
            return list(node_tree.outputs)


# =============================================================================
# Mesh Auto Smooth Compatibility (Changed in 4.1)
# =============================================================================

def set_auto_smooth(obj, enable=True, angle=30.0):
    """
    Enable or configure auto smooth on a mesh object.

    Args:
        obj: Mesh object
        enable: Whether to enable auto smooth
        angle: Auto smooth angle in degrees
    """
    import math

    if obj.type != 'MESH':
        return

    if BLENDER_VERSION >= (4, 1, 0):
        # Blender 4.1+: Use Smooth by Angle modifier
        mod_name = "Smooth by Angle"

        if enable:
            # Add modifier if not present
            mod = obj.modifiers.get(mod_name)
            if mod is None:
                mod = obj.modifiers.new(name=mod_name, type='SMOOTH_BY_ANGLE')
            mod.angle = math.radians(angle)
        else:
            # Remove modifier if present
            mod = obj.modifiers.get(mod_name)
            if mod:
                obj.modifiers.remove(mod)
    else:
        # Blender 4.0 and earlier: Use mesh properties
        mesh = obj.data
        mesh.use_auto_smooth = enable
        if enable:
            mesh.auto_smooth_angle = math.radians(angle)


def get_auto_smooth_angle(obj):
    """
    Get the auto smooth angle of a mesh object.

    Args:
        obj: Mesh object

    Returns:
        Angle in degrees, or None if not enabled
    """
    import math

    if obj.type != 'MESH':
        return None

    if BLENDER_VERSION >= (4, 1, 0):
        mod = obj.modifiers.get("Smooth by Angle")
        if mod:
            return math.degrees(mod.angle)
        return None
    else:
        mesh = obj.data
        if mesh.use_auto_smooth:
            return math.degrees(mesh.auto_smooth_angle)
        return None


# =============================================================================
# Shader Node Compatibility
# =============================================================================

def get_principled_socket_name(socket_name):
    """
    Get the correct Principled BSDF socket name for current Blender version.

    Args:
        socket_name: Generic socket name

    Returns:
        Version-appropriate socket name
    """
    # Socket name changes in Blender 4.0
    socket_map_4_0 = {
        'Specular': 'Specular IOR Level',
        'Subsurface': 'Subsurface Weight',
        'Transmission': 'Transmission Weight',
        'Coat': 'Coat Weight',
        'Sheen': 'Sheen Weight',
    }

    if BLENDER_VERSION >= (4, 0, 0):
        return socket_map_4_0.get(socket_name, socket_name)
    else:
        # Reverse mapping for older versions
        reverse_map = {v: k for k, v in socket_map_4_0.items()}
        return reverse_map.get(socket_name, socket_name)


# =============================================================================
# Context Overrides Compatibility (Changed in 3.2)
# =============================================================================

def call_operator_with_override(operator, **override_context):
    """
    Call an operator with context override.

    Args:
        operator: Operator to call (e.g., bpy.ops.mesh.primitive_cube_add)
        **override_context: Context override parameters

    Returns:
        Operator result
    """
    if BLENDER_VERSION >= (3, 2, 0):
        # Blender 3.2+: Use context.temp_override()
        with bpy.context.temp_override(**override_context):
            return operator()
    else:
        # Older versions: Pass override dict directly
        return operator(override_context)


# =============================================================================
# Utility Functions
# =============================================================================

def print_version_info():
    """Print current Blender version information."""
    print(f"Blender Version: {BLENDER_VERSION_STRING}")
    print(f"  Full version: {BLENDER_VERSION}")
    print(f"  Is Blender 4.x: {is_blender_4()}")
    print(f"  Is Blender 3.x: {is_blender_3()}")
