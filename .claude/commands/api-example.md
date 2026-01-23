---
description: Find code examples from Blender docs
---

Search for working code examples from official Blender documentation.

**Ask user:**
What do you want to do? Examples:
- "create a modifier"
- "add keyframe"
- "create material with nodes"
- "bmesh extrude"
- "custom property"

**Process:**

1. **Identify relevant API:**
   - Map task to Blender API modules
   - Find official documentation examples

2. **Search documentation sources:**
   - API reference code examples
   - Addon tutorial examples
   - Template files from Blender

3. **Provide working examples:**

**Common Tasks with Examples:**

---

**Creating Objects:**
```python
import bpy

# Add mesh primitive
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
obj = bpy.context.active_object
obj.name = "MyCube"

# Create mesh from scratch
mesh = bpy.data.meshes.new("MyMesh")
obj = bpy.data.objects.new("MyObject", mesh)
bpy.context.collection.objects.link(obj)

# Set mesh data
verts = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)]
faces = [(0, 1, 2, 3)]
mesh.from_pydata(verts, [], faces)
mesh.update()
```

---

**Adding Modifiers:**
```python
import bpy

obj = bpy.context.active_object

# Add subdivision surface
subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
subsurf.levels = 2
subsurf.render_levels = 3

# Add bevel
bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
bevel.width = 0.1
bevel.segments = 3
bevel.affect = 'EDGES'

# Apply modifier
bpy.context.view_layer.objects.active = obj
bpy.ops.object.modifier_apply(modifier="Subdivision")
```

---

**Creating Materials:**
```python
import bpy

# Create new material
mat = bpy.data.materials.new(name="MyMaterial")
mat.use_nodes = True

# Get node tree
nodes = mat.node_tree.nodes
links = mat.node_tree.links

# Clear default nodes
nodes.clear()

# Add nodes
output = nodes.new('ShaderNodeOutputMaterial')
output.location = (300, 0)

bsdf = nodes.new('ShaderNodeBsdfPrincipled')
bsdf.location = (0, 0)
bsdf.inputs['Base Color'].default_value = (0.8, 0.1, 0.1, 1.0)
bsdf.inputs['Metallic'].default_value = 0.5

# Connect nodes
links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

# Assign to object
obj = bpy.context.active_object
if obj.data.materials:
    obj.data.materials[0] = mat
else:
    obj.data.materials.append(mat)
```

---

**Animation/Keyframes:**
```python
import bpy

obj = bpy.context.active_object

# Insert keyframe at current frame
obj.location = (0, 0, 0)
obj.keyframe_insert(data_path="location", frame=1)

# Insert keyframe at specific frame
obj.location = (5, 0, 0)
obj.keyframe_insert(data_path="location", frame=50)

# With index (single axis)
obj.keyframe_insert(data_path="location", frame=100, index=0)  # X only

# Delete keyframe
obj.keyframe_delete(data_path="location", frame=50)
```

---

**BMesh Operations:**
```python
import bpy
import bmesh

obj = bpy.context.active_object
mesh = obj.data

# Create BMesh
bm = bmesh.new()
bm.from_mesh(mesh)

# Ensure lookup tables
bm.verts.ensure_lookup_table()
bm.edges.ensure_lookup_table()
bm.faces.ensure_lookup_table()

# Extrude faces
faces_to_extrude = [f for f in bm.faces if f.select]
result = bmesh.ops.extrude_face_region(bm, geom=faces_to_extrude)
verts = [v for v in result['geom'] if isinstance(v, bmesh.types.BMVert)]
bmesh.ops.translate(bm, vec=(0, 0, 1), verts=verts)

# Subdivide
bmesh.ops.subdivide_edges(bm, edges=bm.edges, cuts=2)

# Write back and free
bm.to_mesh(mesh)
bm.free()
mesh.update()
```

---

**Custom Properties:**
```python
import bpy
from bpy.props import FloatProperty, IntProperty, EnumProperty

class MyPropertyGroup(bpy.types.PropertyGroup):
    my_float: FloatProperty(
        name="My Float",
        description="A float property",
        default=1.0,
        min=0.0,
        max=10.0,
    )

    my_enum: EnumProperty(
        name="My Enum",
        items=[
            ('OPT_A', "Option A", "First option"),
            ('OPT_B', "Option B", "Second option"),
        ],
        default='OPT_A',
    )

# Registration
bpy.utils.register_class(MyPropertyGroup)
bpy.types.Scene.my_props = bpy.props.PointerProperty(type=MyPropertyGroup)

# Access
props = bpy.context.scene.my_props
props.my_float = 5.0
```

---

**UI Panel:**
```python
import bpy

class MY_PT_panel(bpy.types.Panel):
    bl_label = "My Panel"
    bl_idname = "MY_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "My Tab"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Properties
        layout.prop(scene.my_props, "my_float")
        layout.prop(scene.my_props, "my_enum")

        # Operators
        layout.operator("mesh.primitive_cube_add", text="Add Cube")

        # Layout options
        row = layout.row(align=True)
        row.operator("object.select_all", text="Select").action = 'SELECT'
        row.operator("object.select_all", text="Deselect").action = 'DESELECT'

        box = layout.box()
        box.label(text="Boxed Section")
```

---

**Output:**
- Working code example for requested task
- Explanation of key parts
- Link to full documentation
- Related examples
