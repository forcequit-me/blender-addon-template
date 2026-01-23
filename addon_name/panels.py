"""UI Panel classes for the addon."""

import bpy
from bpy.types import Panel


class VIEW3D_PT_addon_panel(Panel):
    """Main addon panel in the 3D View sidebar."""
    bl_label = "Addon Name"
    bl_idname = "VIEW3D_PT_addon_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Addon Tab"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.addon_props

        # Properties section
        box = layout.box()
        box.label(text="Settings", icon='PREFERENCES')

        col = box.column(align=True)
        col.prop(props, "example_float")
        col.prop(props, "example_enum")
        col.prop(props, "example_bool")

        layout.separator()

        # Operators section
        box = layout.box()
        box.label(text="Actions", icon='PLAY')

        col = box.column(align=True)
        col.operator("addon.example_operator", icon='OBJECT_ORIGIN')

        # Object info (when object selected)
        if context.active_object:
            layout.separator()
            box = layout.box()
            box.label(text="Active Object", icon='OBJECT_DATA')

            obj = context.active_object
            col = box.column(align=True)
            col.label(text=f"Name: {obj.name}")
            col.label(text=f"Type: {obj.type}")
            col.label(text=f"Location: {obj.location.z:.2f} Z")


# Subpanel example
class VIEW3D_PT_addon_subpanel(Panel):
    """Subpanel for additional options."""
    bl_label = "Advanced"
    bl_idname = "VIEW3D_PT_addon_subpanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Addon Tab"
    bl_parent_id = "VIEW3D_PT_addon_panel"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.label(text="Advanced options go here")
