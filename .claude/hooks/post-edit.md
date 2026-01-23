# Post-Edit Hook

Automatic actions to perform after editing Blender addon code.

## Actions to Perform

### 1. Auto-Format Python Code
If formatter is configured (Black, autopep8, or similar):

```bash
# Black formatting (if available)
black --line-length 100 <edited_file>

# Or autopep8
autopep8 --in-place --max-line-length 100 <edited_file>
```

**Formatting rules for Blender addons:**
- Line length: 100-120 characters (Blender convention)
- Use 4 spaces for indentation
- Two blank lines between top-level definitions
- One blank line between methods

### 2. Update __init__.py Imports
When a new module is added to the addon:

```python
# If new file operators/new_ops.py is created:

# Update __init__.py to include:
from . import new_ops

# Update classes list:
classes = [
    # ... existing classes
    new_ops.NEW_OT_operator,
]

# Update registration if needed
```

**Detection:**
- New .py file created in addon directory
- New class defined that inherits from bpy.types.*
- New property group defined

### 3. Verify Operator ID Naming
After editing operator classes, verify bl_idname follows convention:

```python
# Class name: MESH_OT_custom_tool
# Expected bl_idname: "mesh.custom_tool"

# Auto-suggest fixes:
class MESH_OT_custom_tool(bpy.types.Operator):
    bl_idname = "mesh.custom_tool"  # Correct
    # NOT: bl_idname = "custom.tool"  # Wrong category
```

### 4. Sync Class Registration
When classes are added or removed:

```python
# Scan for all classes inheriting from:
# - bpy.types.Operator
# - bpy.types.Panel
# - bpy.types.Menu
# - bpy.types.PropertyGroup
# - bpy.types.UIList

# Ensure all are in the classes list for registration
classes = [
    # All found classes should be here
]
```

### 5. Update Property References
When PropertyGroup fields change:

```python
# If property renamed from 'old_name' to 'new_name':
# Scan for usages and suggest updates:

# In panels.py:
layout.prop(props, "old_name")  # <- Needs update
# Should be:
layout.prop(props, "new_name")
```

### 6. Check Import Consistency
After edits, verify imports are correct:

```python
# If using function from utils.py in operators.py:
from .utils import helper_function

# Warn if:
# - Importing from non-existent module
# - Circular import detected
# - Unused import added
```

### 7. Validate Panel Locations
When panel bl_space_type or bl_region_type changes:

```python
# Valid combinations:
VALID_PANEL_LOCATIONS = {
    'VIEW_3D': ['UI', 'TOOLS', 'TOOL_PROPS', 'HEADER'],
    'PROPERTIES': ['WINDOW', 'HEADER'],
    'NODE_EDITOR': ['UI', 'TOOLS', 'HEADER'],
    'IMAGE_EDITOR': ['UI', 'TOOLS', 'HEADER'],
    'OUTLINER': ['HEADER'],
    'DOPESHEET_EDITOR': ['UI', 'HEADER'],
    # ... etc
}

# Warn if invalid combination used
```

### 8. Documentation Stub Generation
When new operator created without documentation:

```python
# Auto-generate stub:
class NEW_OT_operator(bpy.types.Operator):
    """[TODO: Add description]"""  # <- Generated
    bl_idname = "new.operator"
    bl_label = "New Operator"
    bl_description = "[TODO: Add detailed description]"  # <- Generated
```

### 9. Type Hint Suggestions
For new functions/methods, suggest type hints:

```python
# Original:
def process_objects(objects, scale):
    pass

# Suggested:
from typing import List
import bpy

def process_objects(objects: List[bpy.types.Object], scale: float) -> None:
    pass
```

### 10. Version Compatibility Check
When using APIs that vary by version:

```python
# If editing code that uses:
node_tree.interface.new_socket(...)

# Suggest adding version guard if not present:
if bpy.app.version >= (4, 0, 0):
    node_tree.interface.new_socket(...)
else:
    node_tree.inputs.new(...)
```

## Output Format

```
Post-Edit Actions
=================

File: operators.py

[AUTO] Formatted code with Black
[AUTO] Added import: from .utils import calculate_bounds
[INFO] New operator detected: MESH_OT_new_tool
[AUTO] Added to classes list in __init__.py
[SUGGEST] Add bl_description to MESH_OT_new_tool
[WARN] Panel VIEW3D_PT_tools uses invalid region 'TOOLS'
       Did you mean 'UI' for sidebar panels?

Actions taken: 3
Suggestions: 1
Warnings: 1
```

## Configuration

These actions can be configured in addon preferences or .claude settings:

```json
{
  "post_edit": {
    "auto_format": true,
    "formatter": "black",
    "line_length": 100,
    "update_imports": true,
    "sync_registration": true,
    "suggest_docs": true,
    "check_compatibility": true
  }
}
```

## Non-Destructive Actions

All auto-modifications should be:
- Reversible (can be undone)
- Non-breaking (don't change behavior)
- Clearly reported to user
- Optional (can be disabled)

Suggestions and warnings should never auto-apply changes that could break functionality.
