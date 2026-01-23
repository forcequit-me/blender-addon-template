---
description: Analyze addon for Blender version compatibility
---

Scan the addon code for version-specific API usage and compatibility issues.

**Process:**

1. **Scan for deprecated API patterns:**

   | Pattern | Deprecated In | Replacement |
   |---------|---------------|-------------|
   | `node_tree.inputs.new()` | 4.0 | `node_tree.interface.new_socket()` |
   | `node_tree.outputs.new()` | 4.0 | `node_tree.interface.new_socket()` |
   | `mesh.use_auto_smooth` | 4.1 | Smooth by Angle modifier |
   | `mesh.auto_smooth_angle` | 4.1 | Smooth by Angle modifier |
   | `bpy.context.scene.frame_current` write | varies | `bpy.context.scene.frame_set()` |
   | `obj.select` | 2.80 | `obj.select_set()` |
   | `scene.objects.link()` | 2.80 | `collection.objects.link()` |
   | `bpy.context.user_preferences` | 2.80 | `bpy.context.preferences` |

2. **Check bl_info version specification:**
   - Verify `"blender"` minimum version is set
   - Check if version matches actual API usage
   - Warn if supporting very old versions with new code

3. **Identify version-specific code:**
   - Find `bpy.app.version` checks
   - Locate try/except import blocks
   - Find conditional API usage

4. **Generate compatibility report:**
   ```
   ═══════════════════════════════════════
   COMPATIBILITY REPORT
   ═══════════════════════════════════════

   Current bl_info blender version: (4, 0, 0)

   DEPRECATED API USAGE
   ───────────────────────────────────────
   ⚠️  operators.py:45
       mesh.use_auto_smooth = True
       Deprecated in: Blender 4.1
       Replacement: Use Smooth by Angle modifier

   ⚠️  nodes.py:23
       node_tree.inputs.new('NodeSocketFloat', "Value")
       Deprecated in: Blender 4.0
       Replacement: node_tree.interface.new_socket()

   VERSION-SPECIFIC CODE FOUND
   ───────────────────────────────────────
   ✓ compat.py:12
       if bpy.app.version >= (4, 0, 0):
       Properly guarded version check

   RECOMMENDATIONS
   ───────────────────────────────────────
   1. Add version guard for mesh.use_auto_smooth
   2. Update node socket creation for 4.0 compatibility
   3. Consider updating minimum version to 4.0 in bl_info

   COMPATIBILITY MATRIX
   ───────────────────────────────────────
   Blender 3.6: ⚠️  Partial (needs version guards)
   Blender 4.0: ⚠️  Partial (auto_smooth deprecated)
   Blender 4.1: ✓ Full support
   ```

5. **Suggest fixes:**
   - Provide compatibility wrapper code
   - Show version detection patterns
   - Offer to create compat.py entries

**Patterns to search for:**

```python
# Regex patterns for deprecated APIs
deprecated_patterns = [
    (r'\.inputs\.new\s*\(', '4.0', 'interface.new_socket()'),
    (r'\.outputs\.new\s*\(', '4.0', 'interface.new_socket()'),
    (r'\.use_auto_smooth\s*=', '4.1', 'Smooth by Angle modifier'),
    (r'\.auto_smooth_angle\s*=', '4.1', 'Smooth by Angle modifier'),
    (r'\.select\s*=\s*(True|False)', '2.80', 'select_set()'),
    (r'user_preferences', '2.80', 'preferences'),
    (r'scene\.objects\.link', '2.80', 'collection.objects.link()'),
]
```

**Output:**
- List all compatibility issues found
- Severity rating for each issue
- Specific file and line numbers
- Recommended fixes with code examples
