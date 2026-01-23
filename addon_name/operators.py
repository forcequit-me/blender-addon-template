"""Operator classes for the addon."""

import bpy
from bpy.types import Operator


class ADDON_OT_example_operator(Operator):
    """Example operator that demonstrates basic operator structure"""
    bl_idname = "addon.example_operator"
    bl_label = "Example Operator"
    bl_description = "An example operator that moves the active object"
    bl_options = {'REGISTER', 'UNDO'}

    # Operator properties
    offset: bpy.props.FloatProperty(
        name="Offset",
        description="Amount to move the object on Z axis",
        default=1.0,
        min=-10.0,
        max=10.0,
    )

    @classmethod
    def poll(cls, context):
        """Check if operator can run in current context."""
        return context.active_object is not None

    def invoke(self, context, event):
        """Called when operator is invoked - shows dialog."""
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        """Main operator logic."""
        try:
            obj = context.active_object
            obj.location.z += self.offset

            self.report({'INFO'}, f"Moved {obj.name} by {self.offset} on Z axis")
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Failed: {str(e)}")
            return {'CANCELLED'}

    def draw(self, context):
        """Draw operator properties in popup."""
        layout = self.layout
        layout.prop(self, "offset")


# Additional operators can be added below
# class ADDON_OT_another_operator(Operator):
#     ...
