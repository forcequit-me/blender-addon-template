from bpy.types import Operator


class ADDON_NAME_OT_example(Operator):
    """Select the target object and make it active"""
    bl_idname = "addon_name.example"
    bl_label = "Example"
    # UNDO because it changes selection; every operator that changes data needs it.
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        target = context.scene.addon_name.target
        if target is None or context.view_layer.objects.get(target.name) is None:
            self.report({'WARNING'}, "Pick a target object in this view layer first")
            return {'CANCELLED'}
        target.select_set(True)
        context.view_layer.objects.active = target
        self.report({'INFO'}, f"Selected {target.name}")
        return {'FINISHED'}
