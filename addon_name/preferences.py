from bpy.types import AddonPreferences

from .panels import draw_links


class ADDON_NAME_AddonPreferences(AddonPreferences):
    # __package__ works for both install types: "addon_name" for a legacy install,
    # "bl_ext.<repo>.addon_name" for an extension.
    bl_idname = __package__

    def draw(self, context):
        layout = self.layout
        layout.separator()
        draw_links(layout)
