# Pre-Commit Hook

Validation checks to run before committing Blender addon code.

## Checks to Perform

### 1. Validate bl_info Dictionary
```python
# Check __init__.py for valid bl_info
required_fields = ['name', 'author', 'version', 'blender', 'description', 'category']

# bl_info must exist
# All required fields must be present
# 'version' must be tuple of 3 ints
# 'blender' must be tuple of 3 ints (minimum version)
# 'category' must be valid Blender category
```

**Valid Categories:**
- 3D View, Add Mesh, Add Curve, Animation, Compositing
- Development, Game Engine, Import-Export, Lighting
- Material, Mesh, Node, Object, Paint, Physics
- Render, Rigging, Scene, Sequencer, System, Text Editor
- UV, User Interface

### 2. Check Operator Documentation
Every operator class must have:
- Docstring (used as tooltip)
- `bl_description` attribute
- `bl_label` attribute

```python
class MY_OT_example(bpy.types.Operator):
    """This docstring is required"""  # <- Check exists
    bl_idname = "my.example"
    bl_label = "Example"  # <- Check exists
    bl_description = "Detailed description"  # <- Check exists
```

### 3. Verify Registration Pairs
For every `register()` there must be a matching `unregister()`:
- All classes in register must be in unregister
- Unregister should be in reverse order
- Properties added in register must be deleted in unregister

```python
# Check pattern:
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.my_prop = ...  # <- Track

def unregister():
    del bpy.types.Scene.my_prop  # <- Must exist
    for cls in reversed(classes):  # <- Should be reversed
        bpy.utils.unregister_class(cls)
```

### 4. Check Naming Conventions
- Operator IDs: `CATEGORY_OT_name` format
- Panel IDs: `CATEGORY_PT_name` format
- Menu IDs: `CATEGORY_MT_name` format
- Property Group IDs: `CATEGORY_PG_name` format

```python
# Valid patterns:
bl_idname = "mesh.custom_operator"  # lowercase.lowercase_with_underscores
bl_idname = "MESH_OT_custom_operator"  # Also valid

# Class names should match:
class MESH_OT_custom_operator  # Matches bl_idname pattern
```

### 5. Scan for Deprecated API Usage
Check for deprecated patterns based on target Blender version:

**Blender 4.0+ Deprecations:**
- `node_tree.inputs.new()` → `node_tree.interface.new_socket()`
- `node_tree.outputs.new()` → `node_tree.interface.new_socket()`
- `node.inputs['Name']` socket names may have changed

**Blender 4.1+ Deprecations:**
- `mesh.use_auto_smooth` → Use "Smooth by Angle" modifier
- `mesh.auto_smooth_angle` → Modifier property

**Blender 3.0+ Deprecations:**
- `bpy.context.scene.frame_set()` signature changed
- Collection instance offsets

### 6. Check Version Guards
If code uses version-specific APIs, ensure version detection:

```python
# Required pattern for version-specific code:
if bpy.app.version >= (4, 0, 0):
    # Blender 4.0+ code
else:
    # Fallback code
```

Warn if version-specific APIs are used without guards.

### 7. Verify bl_info Version Range
```python
bl_info = {
    "blender": (3, 6, 0),  # Minimum version - check it's reasonable
}
```

- Warn if minimum version is very old (< 2.80)
- Warn if minimum version is newer than necessary
- Suggest adding maximum version if using deprecated APIs

### 8. Python Linting (if configured)
Run basic checks:
- Syntax errors
- Undefined names
- Unused imports
- Line length (if configured)

### 9. Check for Common Mistakes
- Using `bpy.context` in module-level code (will fail)
- Missing `poll()` method on operators that need context
- Not freeing BMesh objects
- Hardcoded file paths
- Using `print()` instead of `self.report()`

### 10. Security Checks
- No `exec()` or `eval()` with user input
- No hardcoded credentials
- Validate file paths before use

## Output Format

```
Pre-Commit Validation
=====================

[PASS] bl_info dictionary valid
[PASS] All operators documented
[WARN] Missing bl_description in MY_OT_example (operators.py:45)
[PASS] Registration pairs verified
[PASS] Naming conventions followed
[FAIL] Deprecated API: node_tree.inputs.new() at nodes.py:23
       Suggestion: Use node_tree.interface.new_socket() for Blender 4.0+
[WARN] Version-specific code without guard at compat.py:15
[PASS] bl_info version range specified
[PASS] No common mistakes detected

Summary: 1 failure, 2 warnings
Commit blocked due to failures.
```

## Blocking vs Warning

**Block commit:**
- Missing bl_info
- Syntax errors
- Missing registration functions
- Deprecated APIs without fallbacks (if targeting older versions)

**Warning only:**
- Missing documentation
- Style issues
- Suggestions for improvement
