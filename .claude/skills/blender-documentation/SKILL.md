# Blender Documentation Reference

Expert knowledge for navigating and using official Blender documentation.

## When to Use This Skill
- Looking up API reference
- Finding code examples
- Understanding Blender concepts
- Checking version-specific changes

## Key Documentation Resources

### Python API Reference
**URL:** https://docs.blender.org/api/current/

Primary resource for addon development:
- Class and function signatures
- Property types and parameters
- Code examples
- Module documentation

### Blender Manual
**URL:** https://docs.blender.org/manual/en/latest/

User-facing documentation:
- Feature explanations
- Workflow descriptions
- UI element documentation
- Concept introductions

### Documentation Hub
**URL:** https://docs.blender.org/

Central access to all documentation:
- Links to API docs
- Manual links
- Developer documentation

## Version-Specific API Access

### URL Pattern
```
https://docs.blender.org/api/{version}/
```

### Available Versions
- `/api/4.2/` - Blender 4.2
- `/api/4.1/` - Blender 4.1
- `/api/4.0/` - Blender 4.0
- `/api/3.6/` - Blender 3.6 LTS
- `/api/3.3/` - Blender 3.3 LTS
- `/api/2.93/` - Blender 2.93 LTS
- `/api/current/` - Latest stable

### Use Cases
- Compare APIs between versions
- Find when features were added/removed
- Check if node names changed
- Verify operator parameters

## Common API Modules

### bpy.types - Type Definitions
```
https://docs.blender.org/api/current/bpy.types.html
```

Key classes:
- `Operator` - Base for all operators
- `Panel` - UI panels
- `PropertyGroup` - Custom properties
- `Mesh`, `Object`, `Material` - Data types
- `UILayout` - UI drawing

### bpy.props - Property Definitions
```
https://docs.blender.org/api/current/bpy.props.html
```

Property types:
- `IntProperty`, `FloatProperty`
- `BoolProperty`, `StringProperty`
- `EnumProperty`
- `FloatVectorProperty`, `IntVectorProperty`
- `PointerProperty`, `CollectionProperty`

### bpy.ops - Operators
```
https://docs.blender.org/api/current/bpy.ops.html
```

Operator categories:
- `bpy.ops.object` - Object operations
- `bpy.ops.mesh` - Mesh editing
- `bpy.ops.transform` - Transformations
- `bpy.ops.view3d` - 3D view
- `bpy.ops.wm` - Window manager

### bpy.data - Blend File Data
```
https://docs.blender.org/api/current/bpy.data.html
```

Data collections:
- `bpy.data.objects`
- `bpy.data.meshes`
- `bpy.data.materials`
- `bpy.data.images`
- `bpy.data.node_groups`

### bpy.context - Current State
```
https://docs.blender.org/api/current/bpy.context.html
```

Context attributes:
- `active_object`, `selected_objects`
- `scene`, `view_layer`
- `mode`
- `area`, `region`

### bmesh - Mesh Editing
```
https://docs.blender.org/api/current/bmesh.html
```

BMesh operations:
- `bmesh.ops` - Operations
- `bmesh.types` - Element types
- `bmesh.utils` - Utilities

### mathutils - Math Types
```
https://docs.blender.org/api/current/mathutils.html
```

Types:
- `Vector`
- `Matrix`
- `Quaternion`
- `Euler`
- `Color`

## Quick Reference URLs

| Topic | URL Path |
|-------|----------|
| API Index | `/api/current/genindex.html` |
| Module Index | `/api/current/py-modindex.html` |
| Operator Tutorial | `/api/current/info_tutorial_addon.html` |
| Best Practices | `/api/current/info_best_practice.html` |
| Tips & Tricks | `/api/current/info_tips_and_tricks.html` |
| Gotchas | `/api/current/info_gotcha.html` |
| API Changes | `/api/current/change_log.html` |

## Navigating API Docs

### Finding a Class
1. Go to `bpy.types.html`
2. Search for class name
3. Or use direct URL: `bpy.types.{ClassName}.html`

Example:
```
https://docs.blender.org/api/current/bpy.types.Operator.html
```

### Finding an Operator
1. Go to `bpy.ops.html`
2. Find category (mesh, object, etc.)
3. Click through to operator

Example:
```
https://docs.blender.org/api/current/bpy.ops.mesh.html#bpy.ops.mesh.subdivide
```

### Finding Property Types
1. Go to `bpy.props.html`
2. All property types documented on one page

### Searching the Docs
- Use browser search (Ctrl+F) on index pages
- Use the search box in API docs
- Google: `site:docs.blender.org/api bpy.types.Mesh`

## Code Examples from Docs

### Where to Find Examples
1. **API Reference** - Most classes have examples
2. **Tutorial Pages** - Step-by-step examples
3. **Templates in Blender** - Text Editor > Templates

### Example Locations in Docs
- `info_tutorial_addon.html` - Basic addon tutorial
- Class documentation - Example sections
- Operator documentation - Usage examples

## Manual Sections for Addon Development

### Relevant Manual Pages
- Scripting: `/manual/en/latest/advanced/scripting/`
- Preferences: `/manual/en/latest/editors/preferences/`
- Extensions: `/manual/en/latest/advanced/extensions/`

### Understanding Features
Before implementing, check manual for:
- How users interact with feature
- Expected behavior
- UI conventions

## Release Notes and API Changes

### Release Notes
```
https://wiki.blender.org/wiki/Reference/Release_Notes
```

Check for:
- New features
- Deprecated APIs
- Breaking changes

### API Changes Log
```
https://docs.blender.org/api/current/change_log.html
```

Details:
- Added/removed classes
- Changed parameters
- Renamed items

## Community Resources

### Blender Artists
- Forum for addon developers
- Code reviews and help

### Blender Stack Exchange
- Q&A for Blender scripting
- Searchable archive

### Blender Developer Documentation
```
https://developer.blender.org/docs/
```

For advanced topics:
- Building Blender
- Contributing code
- Architecture overview

## Documentation Best Practices

### When to Check Docs
1. **Before starting** - Understand available APIs
2. **When stuck** - Find examples and patterns
3. **Before release** - Verify version compatibility
4. **After Blender update** - Check for changes

### Effective Documentation Usage
1. Start with tutorial pages for concepts
2. Use API reference for specifics
3. Check examples for patterns
4. Verify in version-specific docs

### Bookmarks to Keep
- API index page
- bpy.types overview
- Version-specific docs for supported versions
- Change log

## Quick Lookup Patterns

### Class Documentation
```
# Pattern
https://docs.blender.org/api/current/bpy.types.{ClassName}.html

# Examples
bpy.types.Operator
bpy.types.Panel
bpy.types.Mesh
bpy.types.Object
```

### Operator Documentation
```
# Pattern
https://docs.blender.org/api/current/bpy.ops.{category}.html

# Examples
bpy.ops.mesh.html
bpy.ops.object.html
bpy.ops.transform.html
```

### Module Documentation
```
# Pattern
https://docs.blender.org/api/current/{module}.html

# Examples
bmesh.html
mathutils.html
bpy.utils.html
```
