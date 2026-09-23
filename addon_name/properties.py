import bpy
from bpy.props import BoolProperty, PointerProperty
from bpy.types import PropertyGroup


class ADDON_NAME_Properties(PropertyGroup):
    # A pointer, not a name string, so the reference survives the object being renamed.
    target: PointerProperty(
        type=bpy.types.Object,
        name="Target",
        description="Object the Example button selects",
    )
    show_settings: BoolProperty(
        name="Settings",
        description="Fold or unfold the settings",
        default=False,
    )
