---
description: Initialize Blender development environment
---

Set up a new Blender addon development environment with all necessary files and structure.

**Ask user:**
1. What is the addon name? (lowercase_with_underscores)
2. What Blender version(s) to target? (e.g., 4.0+, 3.6-4.1)
3. Brief description of the addon
4. Author name
5. What category? (Object, Mesh, Animation, Render, etc.)

**Process:**

1. **Create directory structure:**
   ```
   addon_name/
   ├── __init__.py
   ├── operators.py
   ├── panels.py
   ├── properties.py
   ├── utils.py
   └── compat.py
   ```

2. **Generate `__init__.py`:**
   ```python
   bl_info = {
       "name": "{Addon Name}",
       "author": "{Author}",
       "version": (1, 0, 0),
       "blender": ({min_version}),
       "location": "View3D > Sidebar > {Tab Name}",
       "description": "{Description}",
       "warning": "",
       "doc_url": "",
       "category": "{Category}",
   }

   import bpy

   from . import operators
   from . import panels
   from . import properties

   classes = [
       properties.AddonProperties,
       operators.ADDON_OT_example_operator,
       panels.VIEW3D_PT_addon_panel,
   ]

   def register():
       for cls in classes:
           bpy.utils.register_class(cls)
       bpy.types.Scene.addon_props = bpy.props.PointerProperty(
           type=properties.AddonProperties
       )

   def unregister():
       del bpy.types.Scene.addon_props
       for cls in reversed(classes):
           bpy.utils.unregister_class(cls)

   if __name__ == "__main__":
       register()
   ```

3. **Generate `operators.py`:**
   ```python
   import bpy
   from bpy.types import Operator

   class ADDON_OT_example_operator(Operator):
       """Example operator - replace with your implementation"""
       bl_idname = "addon.example_operator"
       bl_label = "Example Operator"
       bl_description = "An example operator"
       bl_options = {'REGISTER', 'UNDO'}

       @classmethod
       def poll(cls, context):
           return context.active_object is not None

       def execute(self, context):
           self.report({'INFO'}, "Example operator executed")
           return {'FINISHED'}
   ```

4. **Generate `panels.py`:**
   ```python
   import bpy
   from bpy.types import Panel

   class VIEW3D_PT_addon_panel(Panel):
       bl_label = "{Addon Name}"
       bl_idname = "VIEW3D_PT_addon_panel"
       bl_space_type = 'VIEW_3D'
       bl_region_type = 'UI'
       bl_category = "{Tab Name}"

       def draw(self, context):
           layout = self.layout
           scene = context.scene
           props = scene.addon_props

           layout.prop(props, "example_property")
           layout.operator("addon.example_operator")
   ```

5. **Generate `properties.py`:**
   ```python
   import bpy
   from bpy.types import PropertyGroup
   from bpy.props import FloatProperty, IntProperty, BoolProperty

   class AddonProperties(PropertyGroup):
       example_property: FloatProperty(
           name="Example",
           description="An example property",
           default=1.0,
           min=0.0,
           max=10.0,
       )
   ```

6. **Generate `utils.py`:**
   ```python
   """Utility functions for the addon"""

   import bpy

   def get_selected_meshes(context):
       """Return list of selected mesh objects"""
       return [obj for obj in context.selected_objects if obj.type == 'MESH']

   def ensure_object_mode(context):
       """Switch to object mode if not already"""
       if context.mode != 'OBJECT':
           bpy.ops.object.mode_set(mode='OBJECT')
   ```

7. **Generate `compat.py`:**
   ```python
   """Version compatibility utilities"""

   import bpy

   BLENDER_VERSION = bpy.app.version

   def is_blender_4():
       return BLENDER_VERSION >= (4, 0, 0)

   def is_blender_3():
       return (3, 0, 0) <= BLENDER_VERSION < (4, 0, 0)

   # Add version-specific wrappers as needed
   ```

8. **Create symlink/copy to Blender addons folder** (optional):
   - Windows: `%APPDATA%\Blender\{version}\scripts\addons\`
   - macOS: `~/Library/Application Support/Blender/{version}/scripts/addons/`
   - Linux: `~/.config/blender/{version}/scripts/addons/`

**Output:**
- Confirm all files created
- Provide instructions to enable addon in Blender
- Suggest next steps (create first operator, test addon)
