# Version Compatibility

This document describes Blender version support and compatibility considerations.

## Supported Versions

| Blender Version | Support Status | Notes |
|-----------------|----------------|-------|
| 4.2+ | Full | Extension manifest supported (see [EXTENSION_MIGRATION.md](EXTENSION_MIGRATION.md)) |
| 4.1 | Full | Auto-smooth changes |
| 4.0 | Full | Node socket API changes |
| 3.6 LTS | Full | Minimum supported |
| 3.3 LTS | Partial | May work, not tested |
| < 3.0 | Not Supported | Major API differences |

## Package Formats

- **Legacy addon** (3.6 – 4.1, and 4.2 via compat layer): driven by `bl_info` in `__init__.py`.
- **Extension** (4.2+): driven by `blender_manifest.toml`. Required for submission to extensions.blender.org.

Build with `python build.py package --mode=legacy|extension|both`. See [EXTENSION_MIGRATION.md](EXTENSION_MIGRATION.md) for migration details.

## Version-Specific Features

### Blender 4.1+

**Auto Smooth Changes:**
- `mesh.use_auto_smooth` removed
- `mesh.auto_smooth_angle` removed
- Use "Smooth by Angle" modifier instead

```python
# Old (3.x - 4.0)
mesh.use_auto_smooth = True
mesh.auto_smooth_angle = math.radians(30)

# New (4.1+)
mod = obj.modifiers.new("Smooth by Angle", 'SMOOTH_BY_ANGLE')
mod.angle = math.radians(30)
```

**Compatibility wrapper:** Use `compat.set_auto_smooth(obj, enable, angle)`

### Blender 4.0+

**Node Tree Socket API:**
- `node_tree.inputs.new()` deprecated
- `node_tree.outputs.new()` deprecated
- Use `node_tree.interface.new_socket()` instead

```python
# Old (3.x)
node_tree.inputs.new('NodeSocketFloat', 'Value')

# New (4.0+)
node_tree.interface.new_socket(
    name='Value',
    socket_type='NodeSocketFloat',
    in_out='INPUT'
)
```

**Compatibility wrapper:** Use `compat.create_node_socket()`

**Principled BSDF Socket Names:**
| Old Name (3.x) | New Name (4.0+) |
|----------------|-----------------|
| Specular | Specular IOR Level |
| Subsurface | Subsurface Weight |
| Transmission | Transmission Weight |
| Coat | Coat Weight |
| Sheen | Sheen Weight |

**Compatibility wrapper:** Use `compat.get_principled_socket_name()`

### Blender 3.2+

**Context Overrides:**
```python
# Old (< 3.2)
bpy.ops.mesh.primitive_cube_add({'area': area})

# New (3.2+)
with bpy.context.temp_override(area=area):
    bpy.ops.mesh.primitive_cube_add()
```

**Compatibility wrapper:** Use `compat.call_operator_with_override()`

## Known Compatibility Issues

### Issue 1: Node Socket Access

**Symptom:** `AttributeError: 'NoneType' object has no attribute 'default_value'`

**Cause:** Socket names changed between versions.

**Solution:** Use `compat.get_principled_socket_name()` or try/except.

### Issue 2: Auto Smooth Not Working

**Symptom:** Objects don't have smooth shading in Blender 4.1+

**Cause:** Property-based auto smooth replaced with modifier.

**Solution:** Use `compat.set_auto_smooth()` wrapper.

### Issue 3: Geometry Nodes Input Missing

**Symptom:** `KeyError` when accessing geometry node inputs.

**Cause:** Node socket API changed in 4.0.

**Solution:** Use `compat.get_node_tree_sockets()` wrapper.

## Testing Matrix

| Feature | 3.6 LTS | 4.0 | 4.1 | 4.2 |
|---------|---------|-----|-----|-----|
| Basic operators | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| UI panels | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Properties | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| BMesh operations | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Node socket creation | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Auto smooth | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |

## Migration Guide

### Upgrading from 3.x to 4.0

1. **Update node socket code:**
   ```python
   # Replace all instances of:
   node_tree.inputs.new(type, name)
   # With:
   from .compat import create_node_socket
   create_node_socket(node_tree, name, type, 'INPUT')
   ```

2. **Check Principled BSDF references:**
   ```python
   # Replace hardcoded socket names:
   node.inputs['Specular']
   # With:
   from .compat import get_principled_socket_name
   node.inputs[get_principled_socket_name('Specular')]
   ```

### Upgrading from 4.0 to 4.1

1. **Update auto smooth code:**
   ```python
   # Replace:
   mesh.use_auto_smooth = True
   mesh.auto_smooth_angle = angle
   # With:
   from .compat import set_auto_smooth
   set_auto_smooth(obj, True, math.degrees(angle))
   ```

## Adding Support for New Versions

1. Check Blender release notes for API changes
2. Update `compat.py` with new wrappers if needed
3. Test all features in new version
4. Update this compatibility document
5. Update `bl_info["blender"]` if minimum version changes

## Version Detection

```python
import bpy

# Tuple comparison
if bpy.app.version >= (4, 0, 0):
    # Blender 4.0+ code
    pass

# Using compat helpers
from .compat import is_blender_4, is_blender_3

if is_blender_4():
    # Blender 4.x code
    pass
elif is_blender_3():
    # Blender 3.x code
    pass
```

## Reporting Compatibility Issues

If you encounter a compatibility issue:

1. Note the exact Blender version (`Help > About Blender`)
2. Copy the full error message from the console
3. Describe what you were trying to do
4. Create an issue with this information
