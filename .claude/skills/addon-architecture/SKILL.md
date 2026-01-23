# Addon Architecture Patterns

Expert knowledge for structuring Blender addons.

## When to Use This Skill
- Starting a new addon project
- Organizing multi-file addons
- Setting up addon preferences
- Implementing keymaps
- Managing addon resources

## Registration/Unregistration Patterns

### Basic Registration
```python
# __init__.py
import bpy

from . import operators
from . import panels
from . import properties

bl_info = {
    "name": "My Addon",
    "author": "Author",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "category": "Object",
}

classes = [
    properties.MyProperties,
    operators.MY_OT_operator,
    panels.MY_PT_panel,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # Register properties AFTER classes
    bpy.types.Scene.my_props = bpy.props.PointerProperty(type=properties.MyProperties)

def unregister():
    # Unregister properties BEFORE classes
    del bpy.types.Scene.my_props

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
```

### Auto-Registration Pattern
```python
# __init__.py
import bpy
import importlib
import inspect

from . import operators
from . import panels
from . import properties

modules = [
    properties,
    operators,
    panels,
]

def get_classes():
    """Automatically find all registrable classes"""
    classes = []
    for module in modules:
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and hasattr(obj, 'bl_idname'):
                classes.append(obj)
    return classes

def register():
    for module in modules:
        importlib.reload(module)

    for cls in get_classes():
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(get_classes()):
        bpy.utils.unregister_class(cls)
```

### Safe Registration
```python
def register():
    for cls in classes:
        try:
            bpy.utils.register_class(cls)
        except ValueError as e:
            print(f"Already registered: {cls.__name__}")

def unregister():
    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError as e:
            print(f"Not registered: {cls.__name__}")
```

## Multi-File Addon Organization

### Recommended Structure
```
my_addon/
├── __init__.py           # Registration and bl_info
├── operators/
│   ├── __init__.py       # Import all operators
│   ├── mesh_ops.py       # Mesh operators
│   └── object_ops.py     # Object operators
├── panels/
│   ├── __init__.py       # Import all panels
│   └── main_panel.py     # Main UI panel
├── properties/
│   ├── __init__.py       # Import all properties
│   └── scene_props.py    # Scene properties
├── utils/
│   ├── __init__.py
│   └── helpers.py        # Utility functions
├── compat.py             # Version compatibility
└── constants.py          # Constants and enums
```

### Module __init__.py Pattern
```python
# operators/__init__.py
from .mesh_ops import (
    MESH_OT_custom_subdivide,
    MESH_OT_custom_smooth,
)
from .object_ops import (
    OBJECT_OT_custom_transform,
)

classes = [
    MESH_OT_custom_subdivide,
    MESH_OT_custom_smooth,
    OBJECT_OT_custom_transform,
]
```

### Main __init__.py
```python
# __init__.py
import bpy

from .operators import classes as operator_classes
from .panels import classes as panel_classes
from .properties import classes as property_classes

bl_info = {...}

def get_all_classes():
    return property_classes + operator_classes + panel_classes

def register():
    for cls in get_all_classes():
        bpy.utils.register_class(cls)

    # Register scene properties
    from .properties import scene_props
    scene_props.register()

def unregister():
    from .properties import scene_props
    scene_props.unregister()

    for cls in reversed(get_all_classes()):
        bpy.utils.unregister_class(cls)
```

## Addon Preferences

### Basic Preferences
```python
class MyAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__  # Must match addon module name

    # Preference properties
    default_value: bpy.props.FloatProperty(
        name="Default Value",
        default=1.0,
    )

    show_advanced: bpy.props.BoolProperty(
        name="Show Advanced Options",
        default=False,
    )

    install_path: bpy.props.StringProperty(
        name="Install Path",
        subtype='DIR_PATH',
    )

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "default_value")
        layout.prop(self, "show_advanced")
        layout.prop(self, "install_path")

# Access preferences
def get_preferences():
    return bpy.context.preferences.addons[__name__].preferences

# Usage
prefs = get_preferences()
value = prefs.default_value
```

### Preferences with Keymaps
```python
class MyAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout

        # Draw addon preferences
        layout.prop(self, "my_setting")

        # Draw keymap
        col = layout.column()
        col.label(text="Keymap:")

        wm = context.window_manager
        kc = wm.keyconfigs.user
        km = kc.keymaps.get("3D View")
        if km:
            for kmi in km.keymap_items:
                if kmi.idname.startswith("my_addon"):
                    col.context_pointer_set("keymap", km)
                    rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
```

## Keymap Registration

### Basic Keymap
```python
addon_keymaps = []

def register_keymaps():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if kc:
        # Add keymap for 3D View
        km = kc.keymaps.new(name="3D View", space_type='VIEW_3D')

        # Add keymap item
        kmi = km.keymap_items.new(
            "my_addon.my_operator",
            type='E',
            value='PRESS',
            shift=True,
        )
        # Store for unregistration
        addon_keymaps.append((km, kmi))

def unregister_keymaps():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

def register():
    # ... register classes ...
    register_keymaps()

def unregister():
    unregister_keymaps()
    # ... unregister classes ...
```

### Context-Specific Keymaps
```python
# Different keymaps for different contexts
keymaps_config = [
    # (keymap_name, space_type, operator, key, modifiers)
    ("3D View", 'VIEW_3D', "my.operator_3d", 'E', {'shift': True}),
    ("Node Editor", 'NODE_EDITOR', "my.operator_nodes", 'E', {'shift': True}),
    ("Image", 'IMAGE_EDITOR', "my.operator_image", 'E', {'shift': True}),
]

def register_keymaps():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if kc:
        for km_name, space_type, op_id, key, mods in keymaps_config:
            km = kc.keymaps.new(name=km_name, space_type=space_type)
            kmi = km.keymap_items.new(op_id, type=key, value='PRESS', **mods)
            addon_keymaps.append((km, kmi))
```

## Resource Management

### Custom Icons
```python
import os
import bpy.utils.previews

preview_collections = {}

def register_icons():
    pcoll = bpy.utils.previews.new()

    # Path to icons folder
    icons_dir = os.path.join(os.path.dirname(__file__), "icons")

    # Load icons
    pcoll.load("my_icon", os.path.join(icons_dir, "my_icon.png"), 'IMAGE')
    pcoll.load("another_icon", os.path.join(icons_dir, "another.png"), 'IMAGE')

    preview_collections["main"] = pcoll

def unregister_icons():
    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()

# Usage in draw
def draw(self, context):
    pcoll = preview_collections["main"]
    my_icon = pcoll["my_icon"]
    layout.operator("my.operator", icon_value=my_icon.icon_id)
```

### Asset Files
```python
import os

def get_addon_path():
    """Get path to addon directory"""
    return os.path.dirname(os.path.realpath(__file__))

def get_asset_path(filename):
    """Get path to asset file"""
    return os.path.join(get_addon_path(), "assets", filename)

def load_preset(preset_name):
    """Load a preset file"""
    preset_path = get_asset_path(f"presets/{preset_name}.json")
    if os.path.exists(preset_path):
        with open(preset_path, 'r') as f:
            return json.load(f)
    return None
```

## Internationalization (i18n)

### Translation Setup
```python
import bpy
from bpy.app.translations import pgettext as _

# Translation dictionary
translations = {
    "en_US": {
        ("*", "My Operator"): "My Operator",
        ("*", "Execute the operation"): "Execute the operation",
    },
    "ja_JP": {
        ("*", "My Operator"): "マイオペレーター",
        ("*", "Execute the operation"): "操作を実行",
    },
}

def register_translations():
    bpy.app.translations.register(__name__, translations)

def unregister_translations():
    bpy.app.translations.unregister(__name__)

# Usage
class MY_OT_operator(bpy.types.Operator):
    bl_label = _("My Operator")
    bl_description = _("Execute the operation")
```

## Menu Integration

### Append to Existing Menu
```python
def draw_menu(self, context):
    layout = self.layout
    layout.separator()
    layout.operator("my.operator")

def register():
    # ... register classes ...
    bpy.types.VIEW3D_MT_object.append(draw_menu)

def unregister():
    bpy.types.VIEW3D_MT_object.remove(draw_menu)
    # ... unregister classes ...
```

### Custom Menu
```python
class MY_MT_menu(bpy.types.Menu):
    bl_label = "My Menu"
    bl_idname = "MY_MT_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator("my.operator1")
        layout.operator("my.operator2")
        layout.separator()
        layout.menu("MY_MT_submenu")

# Add to header
def draw_header_menu(self, context):
    self.layout.menu("MY_MT_menu")

def register():
    bpy.types.VIEW3D_HT_header.append(draw_header_menu)
```

## Addon State Management

### Persistent Data
```python
from bpy.app.handlers import persistent

@persistent
def load_handler(dummy):
    """Called when blend file is loaded"""
    # Restore addon state
    pass

@persistent
def save_handler(dummy):
    """Called before blend file is saved"""
    # Save addon state
    pass

def register():
    bpy.app.handlers.load_post.append(load_handler)
    bpy.app.handlers.save_pre.append(save_handler)

def unregister():
    bpy.app.handlers.load_post.remove(load_handler)
    bpy.app.handlers.save_pre.remove(save_handler)
```

### Scene-Level State
```python
class AddonState(bpy.types.PropertyGroup):
    is_active: bpy.props.BoolProperty(default=False)
    current_mode: bpy.props.StringProperty(default="DEFAULT")

def register():
    bpy.utils.register_class(AddonState)
    bpy.types.Scene.addon_state = bpy.props.PointerProperty(type=AddonState)

def unregister():
    del bpy.types.Scene.addon_state
    bpy.utils.unregister_class(AddonState)

# Usage
state = bpy.context.scene.addon_state
state.is_active = True
```

## Best Practices

### Module Organization
- Keep `__init__.py` focused on registration
- Separate concerns into modules
- Use explicit imports over wildcards
- Document module responsibilities

### Registration Order
1. Property groups (referenced by other classes)
2. Operators
3. Panels and menus
4. Scene/object properties
5. Keymaps
6. Handlers

### Unregistration Order
Reverse of registration order.

### Error Handling
- Catch registration errors gracefully
- Provide helpful error messages
- Clean up partial registration on failure

## Resources
- Addon Tutorial: https://docs.blender.org/api/current/info_tutorial_addon.html
- Best Practices: https://docs.blender.org/api/current/info_best_practice.html
