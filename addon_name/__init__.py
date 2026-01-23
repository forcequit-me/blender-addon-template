bl_info = {
    "name": "Addon Name",
    "author": "Your Name",
    "version": (1, 0, 0),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > Addon Tab",
    "description": "Brief description of what this addon does",
    "warning": "",
    "doc_url": "",
    "category": "Object",
}

import bpy

from . import operators
from . import panels
from . import properties


# Collect all classes for registration
classes = [
    properties.AddonProperties,
    operators.ADDON_OT_example_operator,
    panels.VIEW3D_PT_addon_panel,
]


def register():
    """Register all addon classes and properties."""
    for cls in classes:
        bpy.utils.register_class(cls)

    # Register properties
    bpy.types.Scene.addon_props = bpy.props.PointerProperty(type=properties.AddonProperties)

    print(f"{bl_info['name']} v{'.'.join(map(str, bl_info['version']))} registered")


def unregister():
    """Unregister all addon classes and properties."""
    # Unregister properties first
    del bpy.types.Scene.addon_props

    # Unregister classes in reverse order
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    print(f"{bl_info['name']} unregistered")


if __name__ == "__main__":
    register()
