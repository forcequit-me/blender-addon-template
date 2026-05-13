---
description: Query current Blender scene via MCP
argument-hint: "[what to inspect]"
allowed-tools: Bash, Read
---

Inspect the current Blender scene state via MCP connection for debugging and development.

**Prerequisites:**
- Blender MCP server must be running
- Blender instance must be connected

**Process:**

1. **Get scene overview:**
   ```python
   # Execute via MCP
   import bpy

   scene = bpy.context.scene
   print(f"Scene: {scene.name}")
   print(f"Frame: {scene.frame_current} / {scene.frame_start}-{scene.frame_end}")
   print(f"Objects: {len(bpy.data.objects)}")
   print(f"Collections: {len(bpy.data.collections)}")
   ```

2. **List selected objects:**
   ```python
   # Execute via MCP
   import bpy

   selected = bpy.context.selected_objects
   active = bpy.context.active_object

   print(f"Selected ({len(selected)}):")
   for obj in selected:
       marker = " [ACTIVE]" if obj == active else ""
       print(f"  - {obj.name} ({obj.type}){marker}")

   if active:
       print(f"\nActive Object Details:")
       print(f"  Location: {tuple(active.location)}")
       print(f"  Rotation: {tuple(active.rotation_euler)}")
       print(f"  Scale: {tuple(active.scale)}")
   ```

3. **Show collection hierarchy:**
   ```python
   # Execute via MCP
   import bpy

   def print_collection(collection, indent=0):
       prefix = "  " * indent
       obj_count = len(collection.objects)
       print(f"{prefix}📁 {collection.name} ({obj_count} objects)")
       for child in collection.children:
           print_collection(child, indent + 1)

   print("Collection Hierarchy:")
   print_collection(bpy.context.scene.collection)
   ```

4. **Display modifier stack:**
   ```python
   # Execute via MCP
   import bpy

   obj = bpy.context.active_object
   if obj and obj.type == 'MESH':
       print(f"Modifiers on '{obj.name}':")
       if obj.modifiers:
           for i, mod in enumerate(obj.modifiers):
               show = "👁" if mod.show_viewport else "  "
               render = "📷" if mod.show_render else "  "
               print(f"  {i+1}. {show}{render} {mod.name} ({mod.type})")
       else:
           print("  (no modifiers)")
   ```

5. **Show material info:**
   ```python
   # Execute via MCP
   import bpy

   obj = bpy.context.active_object
   if obj and hasattr(obj.data, 'materials'):
       print(f"Materials on '{obj.name}':")
       for i, slot in enumerate(obj.material_slots):
           mat = slot.material
           if mat:
               print(f"  {i+1}. {mat.name}")
               if mat.use_nodes:
                   print(f"      Nodes: {len(mat.node_tree.nodes)}")
           else:
               print(f"  {i+1}. (empty slot)")
   ```

6. **Report current context:**
   ```python
   # Execute via MCP
   import bpy

   ctx = bpy.context

   print("Current Context:")
   print(f"  Mode: {ctx.mode}")
   print(f"  Area: {ctx.area.type if ctx.area else 'None'}")
   print(f"  Space: {ctx.space_data.type if ctx.space_data else 'None'}")
   print(f"  Tool: {ctx.workspace.tools.from_space_view3d_mode(ctx.mode).idname if ctx.workspace else 'None'}")

   if ctx.mode == 'EDIT_MESH':
       obj = ctx.edit_object
       bm = bmesh.from_edit_mesh(obj.data)
       print(f"\nEdit Mode Selection:")
       print(f"  Verts: {len([v for v in bm.verts if v.select])}/{len(bm.verts)}")
       print(f"  Edges: {len([e for e in bm.edges if e.select])}/{len(bm.edges)}")
       print(f"  Faces: {len([f for f in bm.faces if f.select])}/{len(bm.faces)}")
   ```

7. **Mesh data inspection:**
   ```python
   # Execute via MCP
   import bpy

   obj = bpy.context.active_object
   if obj and obj.type == 'MESH':
       mesh = obj.data
       print(f"Mesh '{mesh.name}':")
       print(f"  Vertices: {len(mesh.vertices)}")
       print(f"  Edges: {len(mesh.edges)}")
       print(f"  Polygons: {len(mesh.polygons)}")
       print(f"  UV Layers: {[uv.name for uv in mesh.uv_layers]}")
       print(f"  Vertex Groups: {[vg.name for vg in obj.vertex_groups]}")
       print(f"  Shape Keys: {mesh.shape_keys.key_blocks.keys() if mesh.shape_keys else 'None'}")
   ```

**Output format:**
```
═══════════════════════════════════════
SCENE INSPECTION
═══════════════════════════════════════

Scene: Scene
Frame: 1 / 1-250
Mode: OBJECT

Selected Objects (2):
  - Cube (MESH) [ACTIVE]
  - Camera (CAMERA)

Active Object: Cube
  Location: (0.0, 0.0, 0.0)
  Modifiers: Subdivision Surface, Bevel

Collection Hierarchy:
📁 Scene Collection (3 objects)
  📁 Main (2 objects)
  📁 Lights (1 objects)
═══════════════════════════════════════
```

**Use cases:**
- Debug context-dependent operators
- Verify scene state before/after operations
- Understand current selection for testing
- Check modifier/material setup
