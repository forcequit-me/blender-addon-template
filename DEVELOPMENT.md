# Development Guide

This document describes how to set up a development environment and contribute to this addon.

## Development Environment Setup

### Prerequisites

- Blender 3.6+ installed
- Python 3.10+ (matching Blender's Python version)
- Git
- Code editor (VS Code recommended)

### Setting Up for Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/username/addon-name.git
   cd addon-name
   ```

2. **Link addon to Blender:**

   Create a symbolic link from your development folder to Blender's addon directory:

   **Windows (PowerShell as Admin):**
   ```powershell
   New-Item -ItemType SymbolicLink -Path "$env:APPDATA\Blender Foundation\Blender\4.0\scripts\addons\addon_name" -Target ".\addon_name"
   ```

   **macOS/Linux:**
   ```bash
   ln -s "$(pwd)/addon_name" ~/.config/blender/4.0/scripts/addons/addon_name
   ```

3. **Enable developer extras in Blender:**
   - Edit > Preferences > Interface
   - Enable "Developer Extras"

### VS Code Setup

1. Install the **Blender Development** extension
2. Install the **Python** extension
3. Configure Python interpreter to match Blender's Python

Create `.vscode/settings.json`:
```json
{
    "python.analysis.extraPaths": [
        "C:/Program Files/Blender Foundation/Blender 4.0/4.0/scripts/modules"
    ],
    "python.autoComplete.extraPaths": [
        "C:/Program Files/Blender Foundation/Blender 4.0/4.0/scripts/modules"
    ]
}
```

## Project Structure

```
addon_name/
├── __init__.py          # Main addon file with bl_info and registration
├── operators.py         # Operator classes
├── panels.py            # UI panel classes
├── properties.py        # Property definitions
├── utils.py             # Utility functions
└── compat.py            # Version compatibility wrappers
```

## Claude Code Workflow

This project uses Claude Code for development. Available commands:

### Creating New Features
- `/new-operator` - Create a new operator with boilerplate
- `/new-panel` - Create a new UI panel

### Testing
- `/test-in-blender` - Live test via MCP connection
- `/inspect-scene` - Query current Blender scene
- `/create-test-scene` - Set up test environment

### Quality Assurance
- `/check-compatibility` - Check version compatibility
- `/add-performance-metrics` - Add profiling to operators

### Documentation
- `/docs-lookup` - Search Blender documentation
- `/api-example` - Find code examples

### Release
- `/package-addon` - Package for distribution
- `/upgrade-addon` - Upgrade to newer Blender version

## Code Style

### Naming Conventions

- **Operators:** `CATEGORY_OT_name` (e.g., `ADDON_OT_example_operator`)
- **Panels:** `CATEGORY_PT_name` (e.g., `VIEW3D_PT_addon_panel`)
- **Properties:** Descriptive snake_case (e.g., `example_float`)

### Documentation

Every operator must have:
- Docstring (tooltip)
- `bl_description` attribute
- `bl_label` attribute

```python
class ADDON_OT_example(bpy.types.Operator):
    """Short description shown as tooltip"""
    bl_idname = "addon.example"
    bl_label = "Example"
    bl_description = "Detailed description of what this operator does"
```

### Error Handling

Always catch exceptions in `execute()`:

```python
def execute(self, context):
    try:
        # Main logic
        return {'FINISHED'}
    except Exception as e:
        self.report({'ERROR'}, str(e))
        return {'CANCELLED'}
```

## Testing

### Manual Testing Checklist

- [ ] Addon enables without errors
- [ ] Operators appear in search menu (F3)
- [ ] Panels appear in correct locations
- [ ] All properties work correctly
- [ ] Undo/redo works for operators
- [ ] No console errors during normal use

### Live Testing with MCP

If Blender MCP is configured:

```bash
# In Claude Code
/test-in-blender
```

### Testing Multiple Blender Versions

Test on minimum supported version and latest:
- Blender 3.6 (minimum)
- Blender 4.0
- Blender 4.1+ (latest)

## Version Compatibility

### Adding Version Support

Use `compat.py` for version-specific code:

```python
from .compat import BLENDER_VERSION, is_blender_4

if is_blender_4():
    # Blender 4.0+ code
else:
    # Blender 3.x code
```

### Common Version Differences

| Feature | Blender 3.x | Blender 4.0+ |
|---------|-------------|--------------|
| Node sockets | `inputs.new()` | `interface.new_socket()` |
| Auto smooth | `mesh.use_auto_smooth` | Smooth by Angle modifier |
| Principled Specular | `"Specular"` | `"Specular IOR Level"` |

## Building for Release

```bash
# In Claude Code
/package-addon
```

This will:
1. Validate addon structure
2. Check bl_info
3. Run compatibility checks
4. Create distribution ZIP

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Pull Request Guidelines

- Describe what the PR does
- Reference any related issues
- Ensure no console errors
- Test on supported Blender versions
