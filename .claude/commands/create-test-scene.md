---
description: Set up test scene via MCP
argument-hint: "[scene-type basic|complex|empty]"
allowed-tools: Bash, Read
---

Create a test scene in Blender via MCP for testing addon functionality.

**Prerequisites:**
- Blender MCP server must be running
- Blender instance must be connected

**Ask user:**
1. What type of test scene? (basic, complex, specific)
2. What objects needed? (meshes, curves, empties, armatures)
3. Any specific setup requirements?

**Process:**

1. **Basic test scene:**
   ```python
   # Execute via MCP
   import bpy

   # Clear existing objects (optional)
   # bpy.ops.object.select_all(action='SELECT')
   # bpy.ops.object.delete()

   # Create test collection
   test_collection = bpy.data.collections.new("Test Objects")
   bpy.context.scene.collection.children.link(test_collection)

   # Add various mesh types
   meshes = [
       ("Cube", "mesh.primitive_cube_add", {}),
       ("Sphere", "mesh.primitive_uv_sphere_add", {"location": (3, 0, 0)}),
       ("Cylinder", "mesh.primitive_cylinder_add", {"location": (6, 0, 0)}),
       ("Plane", "mesh.primitive_plane_add", {"location": (0, 3, 0)}),
       ("Torus", "mesh.primitive_torus_add", {"location": (3, 3, 0)}),
   ]

   for name, op, kwargs in meshes:
       eval(f"bpy.ops.{op}")(**kwargs)
       obj = bpy.context.active_object
       obj.name = f"Test_{name}"

       # Move to test collection
       for coll in obj.users_collection:
           coll.objects.unlink(obj)
       test_collection.objects.link(obj)

   print(f"Created {len(meshes)} test objects in 'Test Objects' collection")
   ```

2. **Scene with modifiers:**
   ```python
   # Execute via MCP
   import bpy

   # Create cube with modifiers
   bpy.ops.mesh.primitive_cube_add()
   obj = bpy.context.active_object
   obj.name = "Test_Modified_Cube"

   # Add subdivision
   mod = obj.modifiers.new("Subdivision", 'SUBSURF')
   mod.levels = 2

   # Add bevel
   mod = obj.modifiers.new("Bevel", 'BEVEL')
   mod.width = 0.1
   mod.segments = 3

   # Add solidify
   mod = obj.modifiers.new("Solidify", 'SOLIDIFY')
   mod.thickness = 0.05

   print(f"Created modified cube with {len(obj.modifiers)} modifiers")
   ```

3. **Scene with materials:**
   ```python
   # Execute via MCP
   import bpy

   # Create material
   mat = bpy.data.materials.new("Test_Material")
   mat.use_nodes = True

   # Get principled BSDF
   bsdf = mat.node_tree.nodes.get("Principled BSDF")
   if bsdf:
       bsdf.inputs["Base Color"].default_value = (0.8, 0.2, 0.2, 1.0)
       bsdf.inputs["Metallic"].default_value = 0.5
       bsdf.inputs["Roughness"].default_value = 0.3

   # Apply to cube
   bpy.ops.mesh.primitive_cube_add()
   obj = bpy.context.active_object
   obj.name = "Test_Materialed_Cube"
   obj.data.materials.append(mat)

   print(f"Created cube with material '{mat.name}'")
   ```

4. **Scene with hierarchy:**
   ```python
   # Execute via MCP
   import bpy

   # Create parent empty
   bpy.ops.object.empty_add(type='PLAIN_AXES')
   parent = bpy.context.active_object
   parent.name = "Test_Parent"

   # Create children
   for i in range(3):
       bpy.ops.mesh.primitive_cube_add(
           location=(i * 2 - 2, 0, 0),
           scale=(0.5, 0.5, 0.5)
       )
       child = bpy.context.active_object
       child.name = f"Test_Child_{i+1}"
       child.parent = parent

   print(f"Created hierarchy: {parent.name} with {len(parent.children)} children")
   ```

5. **Scene with vertex groups:**
   ```python
   # Execute via MCP
   import bpy

   # Create mesh with vertex groups
   bpy.ops.mesh.primitive_cube_add()
   obj = bpy.context.active_object
   obj.name = "Test_VertexGroups"

   # Add vertex groups
   vg_top = obj.vertex_groups.new(name="Top")
   vg_bottom = obj.vertex_groups.new(name="Bottom")

   # Assign vertices (cube top: 2,3,6,7 bottom: 0,1,4,5)
   vg_top.add([2, 3, 6, 7], 1.0, 'REPLACE')
   vg_bottom.add([0, 1, 4, 5], 1.0, 'REPLACE')

   print(f"Created cube with vertex groups: {[vg.name for vg in obj.vertex_groups]}")
   ```

6. **Custom test scene:**
   ```python
   # Execute via MCP - Template for custom setup
   import bpy

   def create_test_scene(config):
       """Create test scene from configuration"""
       created = []

       for item in config:
           obj_type = item.get('type', 'CUBE')
           name = item.get('name', 'TestObject')
           location = item.get('location', (0, 0, 0))
           scale = item.get('scale', (1, 1, 1))

           # Create object
           if obj_type == 'CUBE':
               bpy.ops.mesh.primitive_cube_add(location=location)
           elif obj_type == 'SPHERE':
               bpy.ops.mesh.primitive_uv_sphere_add(location=location)
           elif obj_type == 'EMPTY':
               bpy.ops.object.empty_add(location=location)

           obj = bpy.context.active_object
           obj.name = name
           obj.scale = scale

           # Add modifiers
           for mod_config in item.get('modifiers', []):
               mod = obj.modifiers.new(mod_config['name'], mod_config['type'])
               for prop, value in mod_config.get('props', {}).items():
                   setattr(mod, prop, value)

           created.append(obj)

       return created

   # Example usage:
   config = [
       {'type': 'CUBE', 'name': 'TestCube', 'location': (0, 0, 0)},
       {'type': 'SPHERE', 'name': 'TestSphere', 'location': (3, 0, 0)},
   ]
   objects = create_test_scene(config)
   ```

7. **Save test scene:**
   ```python
   # Execute via MCP
   import bpy

   # Save as test file
   filepath = "//test_scene.blend"
   bpy.ops.wm.save_as_mainfile(filepath=bpy.path.abspath(filepath))
   print(f"Saved test scene to: {filepath}")
   ```

**Preset scenes:**

| Preset | Contents |
|--------|----------|
| `basic` | Cube, sphere, plane |
| `modifiers` | Cube with subdivision, bevel |
| `materials` | Objects with test materials |
| `hierarchy` | Parent-child relationships |
| `complex` | All of the above |
| `empty` | Clear scene |

**Output:**
- List of created objects
- Scene summary
- Ready-to-use test environment
