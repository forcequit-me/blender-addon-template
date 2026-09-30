# Keep "name", "version" and "blender" in step with blender_manifest.toml.
# The smoke test and `python build.py validate` fail when they drift apart.
bl_info = {
    "name": "Addon Name",
    "author": "Your Name",
    "version": (0, 1, 0),
    "blender": (5, 0, 0),
    "location": "View3D > Sidebar > Addon Name",
    "description": "PLACEHOLDER: one sentence saying what the add-on does, in the user's words",
    "category": "3D View",
}

import bpy

from . import properties
from . import preferences
from . import operators
from . import panels
from . import links


classes = (
    properties.ADDON_NAME_Properties,
    preferences.ADDON_NAME_AddonPreferences,
    operators.ADDON_NAME_OT_example,
    panels.ADDON_NAME_PT_panel,
    panels.ADDON_NAME_PT_links,
    links.ADDON_NAME_OT_open_link,
)


def register():
    # Blender enables a legacy add-on below its minimum version with only a warning,
    # so refuse here instead of failing later on a missing API. Extensions need no check:
    # Blender will not install one below blender_version_min, and it deletes bl_info from
    # an extension's module, hence globals().get().
    minimum = globals().get("bl_info", {}).get("blender", (0, 0, 0))
    if bpy.app.version < minimum:
        raise RuntimeError(
            f"Addon Name requires Blender {'.'.join(map(str, minimum))} or newer. "
            f"You are running {'.'.join(map(str, bpy.app.version))}."
        )
    links._load_icons()
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.addon_name = bpy.props.PointerProperty(type=properties.ADDON_NAME_Properties)
    # Never touch bpy.data in register(): it raises _RestrictData errors.
    # If you need first-time scene setup, defer it:
    #     bpy.app.timers.register(setup_fn, first_interval=0)


def unregister():
    if hasattr(bpy.types.Scene, "addon_name"):
        del bpy.types.Scene.addon_name
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    links._unload_icons()
