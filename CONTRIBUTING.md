# Contributing Guide

Thank you for your interest in contributing to this Blender addon! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Code Style](#code-style)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Review Process](#review-process)

---

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow

---

## Getting Started

### Prerequisites

- Blender 3.6+ installed
- Python 3.10+ (included with Blender)
- Git for version control
- A code editor (VS Code, PyCharm, etc.)

### Types of Contributions

We welcome:

- **Bug fixes** - Fix issues and improve stability
- **New features** - Add functionality (discuss first in an issue)
- **Documentation** - Improve docs, tutorials, examples
- **Tests** - Add or improve test coverage
- **Translations** - Help localize the addon

---

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR-USERNAME/addon-name.git
cd addon-name
```

### 2. Set Up Development Environment

**Option A: Symlink to Blender addons folder**

```bash
# Windows (run as admin)
mklink /D "%APPDATA%\Blender Foundation\Blender\4.0\scripts\addons\addon_name" "C:\path\to\repo\addon_name"

# macOS/Linux
ln -s /path/to/repo/addon_name ~/.config/blender/4.0/scripts/addons/addon_name
```

**Option B: Use Blender's development mode**

Set `BLENDER_USER_SCRIPTS` environment variable to your repo's parent folder.

### 3. Enable Developer Extras in Blender

1. Edit > Preferences > Interface
2. Enable "Developer Extras"
3. This shows additional debug info and options

### 4. Install Development Dependencies (Optional)

```bash
# For running tests outside Blender
pip install pytest fake-bpy-module-latest
```

---

## Making Changes

### Branch Naming

Create a branch for your changes:

```bash
git checkout -b type/description

# Examples:
git checkout -b fix/operator-crash-on-empty-selection
git checkout -b feature/batch-material-assignment
git checkout -b docs/improve-installation-guide
```

### Commit Messages

Follow conventional commit format:

```
type(scope): short description

Longer description if needed. Explain the "why" not just the "what".

Fixes #123
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(operators): add batch rename operator

fix(panel): prevent crash when no object selected

docs(readme): add installation troubleshooting section
```

---

## Code Style

### Python Style

- Follow [PEP 8](https://pep8.org/) guidelines
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters
- Use type hints where practical

### Blender-Specific Style

- **Operator IDs**: `CATEGORY_OT_operator_name`
- **Panel IDs**: `CATEGORY_PT_panel_name`
- **Property names**: `snake_case` with descriptive names
- Always include `bl_description` for operators
- Always implement `poll()` method for operators

### Example Operator

```python
class ADDON_OT_example_operator(bpy.types.Operator):
    """Short tooltip description"""
    bl_idname = "addon.example_operator"
    bl_label = "Example Operator"
    bl_description = "Detailed description of what this operator does"
    bl_options = {'REGISTER', 'UNDO'}

    # Properties with full documentation
    amount: bpy.props.FloatProperty(
        name="Amount",
        description="The amount to apply",
        default=1.0,
        min=0.0,
        max=10.0,
    )

    @classmethod
    def poll(cls, context):
        """Operator is available when there's an active mesh object."""
        return (
            context.active_object is not None
            and context.active_object.type == 'MESH'
        )

    def execute(self, context):
        try:
            # Implementation
            self.report({'INFO'}, "Operation completed")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed: {e}")
            return {'CANCELLED'}
```

### Documentation Style

- Use docstrings for all public functions and classes
- Include parameter descriptions
- Provide usage examples where helpful

```python
def calculate_offset(base_value: float, multiplier: float = 1.0) -> float:
    """
    Calculate the offset value for positioning.

    Args:
        base_value: The starting value to offset from.
        multiplier: Scale factor for the offset. Defaults to 1.0.

    Returns:
        The calculated offset value.

    Example:
        >>> offset = calculate_offset(5.0, 2.0)
        >>> print(offset)
        10.0
    """
    return base_value * multiplier
```

---

## Testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_operators.py

# Run with verbose output
python -m pytest tests/ -v

# Run tests matching a pattern
python -m pytest tests/ -k "test_operator"
```

### Writing Tests

Place tests in the `tests/` folder. See `tests/README.md` for detailed examples.

### Test Categories

- **Unit tests**: Test individual functions
- **Integration tests**: Test operator workflows
- **Edge case tests**: Test error handling

### Testing in Blender

For tests that require Blender's runtime:

```bash
# Run tests inside Blender
blender --background --python tests/run_blender_tests.py
```

---

## Submitting Changes

### Before Submitting

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New features have tests
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated (under [Unreleased])
- [ ] Commit messages are clear

### Pull Request Process

1. **Push your branch**
   ```bash
   git push origin feature/your-feature
   ```

2. **Create Pull Request**
   - Go to the repository on GitHub
   - Click "New Pull Request"
   - Select your branch
   - Fill out the PR template

3. **PR Title Format**
   ```
   type(scope): description

   # Examples:
   feat(operators): add batch material assignment
   fix(panel): resolve crash on startup
   ```

4. **PR Description**
   - Describe what changes you made
   - Explain why these changes are needed
   - Link related issues
   - Include screenshots/GIFs for UI changes

---

## Review Process

### What to Expect

1. **Automated checks** run first (if configured)
2. **Maintainer review** within a few days
3. **Feedback** may request changes
4. **Approval and merge** once requirements are met

### Responding to Feedback

- Address all review comments
- Push additional commits to the same branch
- Mark conversations as resolved when addressed
- Ask questions if feedback is unclear

### After Merge

- Your branch will be deleted (you can delete locally too)
- Changes will appear in the next release
- You'll be credited in the changelog

---

## Getting Help

- **Questions**: Open a discussion or issue
- **Bugs**: Use the bug report template
- **Features**: Use the feature request template
- **Security**: Report privately to maintainers

---

## Recognition

Contributors are recognized in:
- CHANGELOG.md for each release
- README.md contributors section
- GitHub contributors page

Thank you for contributing!
