# Blender Version Compatibility

Expert knowledge for supporting multiple Blender versions.

## When to Use This Skill
- Supporting multiple Blender versions
- Migrating addons to newer versions
- Handling deprecated APIs
- Writing version-agnostic code

## Version Detection Patterns

### Basic Version Check
```python
import bpy

BLENDER_VERSION = bpy.app.version  # Tuple: (4, 1, 0)
BLENDER_VERSION_STRING = bpy.app.version_string  # "4.1.0"

# Version comparisons
if BLENDER_VERSION >= (4, 0, 0):
    # Blender 4.0+ code
    pass

if BLENDER_VERSION < (3, 6, 0):
    # Legacy code
    pass

# Check specific version
if BLENDER_VERSION[:2] == (4, 1):
    # Exactly Blender 4.1.x
    pass
```

### Version Constants
```python
# compat.py
import bpy

BLENDER_VERSION = bpy.app.version

IS_BLENDER_4_2_PLUS = BLENDER_VERSION >= (4, 2, 0)
IS_BLENDER_4_1_PLUS = BLENDER_VERSION >= (4, 1, 0)
IS_BLENDER_4_0_PLUS = BLENDER_VERSION >= (4, 0, 0)
IS_BLENDER_3_6_PLUS = BLENDER_VERSION >= (3, 6, 0)
IS_BLENDER_3_0_PLUS = BLENDER_VERSION >= (3, 0, 0)

# Feature flags
HAS_NODE_INTERFACE = IS_BLENDER_4_0_PLUS
HAS_SMOOTH_BY_ANGLE = IS_BLENDER_4_1_PLUS
```

## Common Breaking Changes by Version

### Blender 2.80 (Major Overhaul)
```python
# Selection
# OLD: obj.select = True
# NEW:
obj.select_set(True)

# Collections (replaced layers)
# OLD: scene.objects.link(obj)
# NEW:
collection.objects.link(obj)

# Preferences
# OLD: bpy.context.user_preferences
# NEW:
bpy.context.preferences

# Make local
# OLD: bpy.ops.object.make_local(type='ALL')
# NEW:
bpy.ops.object.make_local(type='SELECT_OBDATA_MATERIAL')
```

### Blender 3.0
```python
# Python version: 3.9 -> 3.10
# Library overrides became default for linked data
```

### Blender 4.0
```python
# Node socket creation
# OLD:
node_tree.inputs.new('NodeSocketFloat', "Value")
node_tree.outputs.new('NodeSocketGeometry', "Geometry")

# NEW:
node_tree.interface.new_socket(
    name="Value",
    socket_type='NodeSocketFloat',
    in_out='INPUT'
)
node_tree.interface.new_socket(
    name="Geometry",
    socket_type='NodeSocketGeometry',
    in_out='OUTPUT'
)
```

### Blender 4.1
```python
# Auto-smooth removed from mesh
# OLD:
mesh.use_auto_smooth = True
mesh.auto_smooth_angle = 0.523599

# NEW: Use modifier
mod = obj.modifiers.new("Smooth by Angle", 'SMOOTH_BY_ANGLE')
mod.angle = 0.523599
```

## Compatibility Wrapper Patterns

### Node Socket Wrapper
```python
def create_node_socket(node_tree, name, socket_type, in_out):
    """Create node socket - compatible with 3.x and 4.x"""
    if bpy.app.version >= (4, 0, 0):
        return node_tree.interface.new_socket(
            name=name,
            socket_type=socket_type,
            in_out=in_out
        )
    else:
        if in_out == 'INPUT':
            return node_tree.inputs.new(socket_type, name)
        else:
            return node_tree.outputs.new(socket_type, name)

def get_node_sockets(node_tree, in_out='INPUT'):
    """Get node tree sockets - compatible with 3.x and 4.x"""
    if bpy.app.version >= (4, 0, 0):
        return [s for s in node_tree.interface.items_tree
                if s.item_type == 'SOCKET' and s.in_out == in_out]
    else:
        if in_out == 'INPUT':
            return list(node_tree.inputs)
        else:
            return list(node_tree.outputs)
```

### Auto-Smooth Wrapper
```python
import math

def set_auto_smooth(obj, enabled=True, angle_degrees=30):
    """Set auto smooth - compatible with 4.0 and 4.1+"""
    angle_radians = math.radians(angle_degrees)

    if bpy.app.version >= (4, 1, 0):
        # Use modifier approach
        mod_name = "Smooth by Angle"
        mod = obj.modifiers.get(mod_name)

        if enabled:
            if mod is None:
                mod = obj.modifiers.new(mod_name, 'SMOOTH_BY_ANGLE')
            mod.angle = angle_radians
        else:
            if mod is not None:
                obj.modifiers.remove(mod)
    else:
        # Use mesh property
        if hasattr(obj.data, 'use_auto_smooth'):
            obj.data.use_auto_smooth = enabled
            if enabled:
                obj.data.auto_smooth_angle = angle_radians

def has_auto_smooth(obj):
    """Check if object has auto smooth enabled"""
    if bpy.app.version >= (4, 1, 0):
        for mod in obj.modifiers:
            if mod.type == 'SMOOTH_BY_ANGLE':
                return True
        return False
    else:
        return getattr(obj.data, 'use_auto_smooth', False)
```

### Context Override Wrapper
```python
def run_with_override(operator_func, override_dict):
    """Run operator with context override - compatible across versions"""
    if bpy.app.version >= (3, 2, 0):
        with bpy.context.temp_override(**override_dict):
            return operator_func()
    else:
        return operator_func(override_dict)

# Usage
override = {'active_object': obj, 'selected_objects': [obj]}
run_with_override(lambda: bpy.ops.object.transform_apply(scale=True), override)
```

### Socket Name Wrapper
```python
def get_socket(node, names):
    """Get socket with fallback names for version differences"""
    for name in names if isinstance(names, (list, tuple)) else [names]:
        if name in node.inputs:
            return node.inputs[name]
        if name in node.outputs:
            return node.outputs[name]
    return None

# Usage - handles renamed sockets
specular = get_socket(bsdf_node, ["Specular IOR Level", "Specular"])
```

## Conditional Imports

### Try/Except Pattern
```python
try:
    from bpy.types import SmoothByAngleModifier
    HAS_SMOOTH_BY_ANGLE = True
except ImportError:
    HAS_SMOOTH_BY_ANGLE = False

# Usage
if HAS_SMOOTH_BY_ANGLE:
    mod = obj.modifiers.new("Smooth", 'SMOOTH_BY_ANGLE')
```

### Feature Detection
```python
def has_attribute(type_or_obj, attr_name):
    """Check if attribute exists"""
    if isinstance(type_or_obj, type):
        return hasattr(type_or_obj, attr_name)
    return hasattr(type_or_obj, attr_name)

# Usage
if has_attribute(bpy.types.Mesh, 'use_auto_smooth'):
    # Old API available
    pass
```

## bl_info Version Specification

### Minimum Version Only
```python
bl_info = {
    "name": "My Addon",
    "blender": (3, 6, 0),  # Minimum required version
    # ...
}
```

### Version Range Documentation
```python
bl_info = {
    "name": "My Addon",
    "blender": (3, 6, 0),
    "description": "My addon (supports Blender 3.6 - 4.2)",
    "warning": "Blender 4.0+ recommended for best performance",
    # ...
}
```

## Testing Strategies

### Version Test Script
```python
# test_compatibility.py - Run in each Blender version
import bpy
import sys

def test_addon():
    """Test addon in current Blender version"""
    version = bpy.app.version_string
    print(f"\n{'='*50}")
    print(f"Testing in Blender {version}")
    print('='*50)

    tests = [
        ("Import addon", test_import),
        ("Register", test_register),
        ("Operator exists", test_operator),
        ("Panel renders", test_panel),
        ("Properties work", test_properties),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            test_func()
            print(f"  [PASS] {name}")
            passed += 1
        except Exception as e:
            print(f"  [FAIL] {name}: {e}")
            failed += 1

    print(f"\nResults: {passed} passed, {failed} failed")
    return failed == 0

def test_import():
    import my_addon
    assert my_addon is not None

def test_register():
    import my_addon
    my_addon.register()

def test_operator():
    assert hasattr(bpy.ops.my_addon, 'my_operator')

def test_panel():
    assert 'MY_PT_panel' in dir(bpy.types)

def test_properties():
    props = bpy.context.scene.my_props
    assert props is not None

if __name__ == "__main__":
    success = test_addon()
    sys.exit(0 if success else 1)
```

### Version Matrix
```markdown
## Compatibility Matrix

| Feature | 3.6 | 4.0 | 4.1 | 4.2 |
|---------|-----|-----|-----|-----|
| Basic operators | Yes | Yes | Yes | Yes |
| Node editing | Yes* | Yes | Yes | Yes |
| Auto-smooth | Yes | Yes | No** | No** |

* Uses legacy socket API
** Uses modifier instead
```

## Deprecation Patterns

### Gradual Deprecation
```python
def old_function():
    """Deprecated: Use new_function instead"""
    import warnings
    warnings.warn(
        "old_function is deprecated, use new_function",
        DeprecationWarning,
        stacklevel=2
    )
    return new_function()
```

### Version-Conditional Deprecation Warning
```python
def set_smooth(obj, angle):
    if bpy.app.version >= (4, 1, 0):
        # Warn if code uses old pattern
        import warnings
        warnings.warn(
            "Direct auto_smooth access deprecated in 4.1, use set_auto_smooth()",
            DeprecationWarning
        )
    set_auto_smooth(obj, True, angle)
```

## Migration Helpers

### API Replacement Finder
```python
deprecated_apis = {
    'mesh.use_auto_smooth': {
        'removed_in': (4, 1, 0),
        'replacement': 'SMOOTH_BY_ANGLE modifier',
        'example': 'obj.modifiers.new("Smooth", "SMOOTH_BY_ANGLE")'
    },
    'node_tree.inputs.new': {
        'removed_in': (4, 0, 0),
        'replacement': 'node_tree.interface.new_socket()',
        'example': 'interface.new_socket(name="X", socket_type="NodeSocketFloat", in_out="INPUT")'
    },
}

def check_deprecated_usage(code_string):
    """Check code for deprecated API usage"""
    issues = []
    for api, info in deprecated_apis.items():
        if api in code_string:
            if bpy.app.version >= info['removed_in']:
                issues.append({
                    'api': api,
                    'status': 'REMOVED',
                    'replacement': info['replacement'],
                })
            else:
                issues.append({
                    'api': api,
                    'status': 'DEPRECATED',
                    'removed_in': info['removed_in'],
                })
    return issues
```

## Best Practices

1. **Always specify minimum version** in bl_info
2. **Use wrapper functions** for version-specific APIs
3. **Test on all supported versions** before release
4. **Document version requirements** clearly
5. **Provide migration notes** for breaking changes
6. **Use feature detection** over version checks when possible
7. **Keep compat.py centralized** for all version handling

## Resources
- Release Notes: https://wiki.blender.org/wiki/Reference/Release_Notes
- API Changes: https://docs.blender.org/api/current/change_log.html
- Version History: https://www.blender.org/download/releases/
