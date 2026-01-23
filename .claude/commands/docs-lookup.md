---
description: Search Blender documentation
---

Search official Blender documentation for API reference and usage information.

**Ask user:**
What do you want to look up? Examples:
- "bpy.ops.mesh.subdivide"
- "PropertyGroup"
- "how to create a modifier"
- "bmesh edge loop"

**Documentation Sources:**

1. **Python API Reference** (primary for addon development)
   - URL: https://docs.blender.org/api/current/
   - Version-specific: https://docs.blender.org/api/{version}/
   - Examples: /api/4.1/, /api/4.0/, /api/3.6/

2. **Blender Manual** (user-facing features)
   - URL: https://docs.blender.org/manual/en/latest/
   - Good for understanding features from user perspective

3. **Documentation Hub**
   - URL: https://docs.blender.org/
   - Links to all documentation

**Process:**

1. **Identify search type:**
   - API class/function → Python API docs
   - Operator → bpy.ops reference
   - Concept/workflow → Blender Manual
   - Code example → API docs examples section

2. **Search API documentation:**

   **For bpy.types classes:**
   ```
   https://docs.blender.org/api/current/bpy.types.{ClassName}.html

   Examples:
   - bpy.types.Operator
   - bpy.types.Panel
   - bpy.types.Mesh
   - bpy.types.Object
   - bpy.types.PropertyGroup
   ```

   **For bpy.ops operators:**
   ```
   https://docs.blender.org/api/current/bpy.ops.{category}.html

   Examples:
   - bpy.ops.mesh.html (mesh operators)
   - bpy.ops.object.html (object operators)
   - bpy.ops.transform.html (transform operators)
   ```

   **For bpy.props properties:**
   ```
   https://docs.blender.org/api/current/bpy.props.html

   Includes:
   - IntProperty
   - FloatProperty
   - BoolProperty
   - StringProperty
   - EnumProperty
   - PointerProperty
   - CollectionProperty
   ```

   **For modules:**
   ```
   https://docs.blender.org/api/current/{module}.html

   Examples:
   - bmesh.html
   - mathutils.html
   - bpy.utils.html
   - bpy.path.html
   ```

3. **Quick reference links:**

   | Topic | URL |
   |-------|-----|
   | API Index | /api/current/genindex.html |
   | bpy.types | /api/current/bpy.types.html |
   | bpy.ops | /api/current/bpy.ops.html |
   | bpy.props | /api/current/bpy.props.html |
   | bpy.data | /api/current/bpy.data.html |
   | bpy.context | /api/current/bpy.context.html |
   | bmesh | /api/current/bmesh.html |
   | mathutils | /api/current/mathutils.html |
   | Operator tutorial | /api/current/info_tutorial_addon.html |
   | Tips & Tricks | /api/current/info_tips_and_tricks.html |
   | Best Practices | /api/current/info_best_practice.html |

4. **Fetch and summarize:**
   - Retrieve relevant documentation page
   - Extract key information:
     - Class/function signature
     - Parameters and return values
     - Description
     - Code examples
   - Provide direct link for full documentation

**Example output:**

```
═══════════════════════════════════════
DOCUMENTATION: bpy.types.Operator
═══════════════════════════════════════

Base class for operators.

Key Attributes:
  bl_idname (str) - Unique operator identifier
  bl_label (str) - Display name
  bl_description (str) - Tooltip text
  bl_options (set) - {'REGISTER', 'UNDO', etc.}

Key Methods:
  poll(context) - Return True if operator can run
  invoke(context, event) - Called on operator invoke
  execute(context) - Main operator logic
  modal(context, event) - For modal operators
  draw(context) - Draw operator properties

Return Values:
  {'FINISHED'} - Success
  {'CANCELLED'} - Failed/cancelled
  {'RUNNING_MODAL'} - Modal mode
  {'PASS_THROUGH'} - Pass to other handlers

Example:
  class MyOperator(bpy.types.Operator):
      bl_idname = "object.my_operator"
      bl_label = "My Operator"

      def execute(self, context):
          return {'FINISHED'}

Full docs: https://docs.blender.org/api/current/bpy.types.Operator.html
═══════════════════════════════════════
```

**Output:**
- Relevant documentation summary
- Code examples from official docs
- Direct links to full documentation
- Related topics/classes
