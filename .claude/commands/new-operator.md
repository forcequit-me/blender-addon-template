---
description: Create a new Blender operator with boilerplate
argument-hint: "[operator-name] [category]"
allowed-tools: Read, Write, Edit, Glob, Grep
---

Create a new Blender operator with proper registration and boilerplate code.

**Ask user:**
1. What is the operator name? (e.g., "custom_subdivide", "apply_modifier")
2. What category does it belong to? (e.g., MESH, OBJECT, VIEW3D)
3. What does this operator do? (brief description)
4. Should it have undo support? (yes/no)
5. Does it need a properties dialog? (yes/no)
6. Where should it appear in the UI? (panel, menu, both, none)

**Process:**

1. Generate operator class with:
   - Proper `bl_idname` format: `{category.lower()}.{operator_name}`
   - Proper class name format: `{CATEGORY}_OT_{operator_name}`
   - `bl_label` from operator name
   - `bl_description` from user description
   - `bl_options` based on undo preference

2. Include standard methods:
   - `poll()` classmethod for context validation
   - `execute()` with try/except error handling
   - `invoke()` if properties dialog needed
   - `draw()` if properties dialog needed

3. Add to operators.py file

4. Register in __init__.py classes list

5. If UI placement requested:
   - Add to appropriate panel's draw() method
   - Or add to menu append function

**Template:**

```python
class {CATEGORY}_OT_{operator_name}(bpy.types.Operator):
    """{description}"""
    bl_idname = "{category}.{operator_name}"
    bl_label = "{Operator Label}"
    bl_description = "{description}"
    bl_options = {{'REGISTER', 'UNDO'}}

    # Add properties here
    # example_prop: bpy.props.FloatProperty(name="Example", default=1.0)

    @classmethod
    def poll(cls, context):
        # Modify based on operator requirements
        return context.active_object is not None

    def execute(self, context):
        try:
            # TODO: Implement operator logic

            self.report({{'INFO'}}, "{Operator Label} completed")
            return {{'FINISHED'}}
        except Exception as e:
            self.report({{'ERROR'}}, str(e))
            return {{'CANCELLED'}}
```

**After creation:**
- Remind user to implement the execute() logic
- Suggest testing with F3 search menu
- Offer to create a panel button for the operator
