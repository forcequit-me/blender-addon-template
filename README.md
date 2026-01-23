# Blender Addon Template - Quick Start Guide

A complete Claude Code workflow for Blender addon development with live testing, API validation, and automated code generation.

---

## Prerequisites

Before using this template, ensure you have:

- [ ] **Claude Code** installed and configured
- [ ] **Blender** 3.6+ installed
- [ ] **Python** 3.10+ (comes with Blender)
- [ ] **Blender MCP Server** (optional, for live testing) - [Setup Guide](https://github.com/ahujasid/blender-mcp)

---

## Quick Start (5 Steps)

```
1. Copy template    →  Copy `blender-addon-template/` to your project folder
2. Rename addon     →  Rename `addon_name/` folder to your addon name
3. Update bl_info   →  Edit `__init__.py` with your addon details
4. Create operator  →  Run `/new-operator` in Claude Code
5. Test in Blender  →  Run `/test-in-blender` or install manually
```

---

## Command Cheat Sheet

### Development Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/new-operator` | Create operator with boilerplate | Adding new functionality |
| `/new-panel` | Create UI panel | Adding user interface |
| `/setup-blender-dev` | Initialize dev environment | Starting fresh project |
| `/add-performance-metrics` | Add timing instrumentation | Profiling slow operators |

### Testing Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/test-addon` | Reload and validate addon | After code changes |
| `/test-in-blender` | Live test via MCP | Real-time testing (requires MCP) |
| `/inspect-scene` | Query scene state via MCP | Debugging context issues |
| `/create-test-scene` | Setup test environment | Automated testing |
| `/live-dev` | Interactive dev mode | Continuous development |

### Compatibility Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/check-compatibility` | Scan for deprecated APIs | Before release |
| `/upgrade-addon` | Update to newer Blender | Version migration |
| `/add-version-support` | Add multi-version support | Supporting older Blender |
| `/compare-api-versions` | Compare APIs across versions | Understanding changes |

### Documentation Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/docs-lookup` | Search Blender docs | Learning API |
| `/api-example` | Find code examples | Need working snippets |

### Release & Build Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/build` | Package addon (uses build.py) | Creating distribution ZIP |
| `/bump-version` | Bump version + update changelog | Before releasing |
| `/update-changelog` | Update CHANGELOG.md | Documenting changes |
| `/release` | Full release workflow | Complete release process |
| `/package-addon` | Create distribution ZIP | Quick packaging |

### build.py CLI Commands

You can also use build.py directly from the terminal:

```bash
python build.py package              # Create distribution ZIP
python build.py package --clean      # Clean first, then package
python build.py validate             # Validate addon structure
python build.py version              # Show current version
python build.py version 1.2.0        # Set specific version
python build.py version --bump patch # Bump patch (1.0.0 → 1.0.1)
python build.py version --bump minor # Bump minor (1.0.0 → 1.1.0)
python build.py version --bump major # Bump major (1.0.0 → 2.0.0)
python build.py clean                # Remove build artifacts
```

---

## Workflow Diagrams

### New Feature Workflow
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  /new-operator  │ ──► │ /test-in-blender│ ──► │/check-compat    │
│  Create code    │     │ Live testing    │     │ Verify support  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                                                        ▼
                                                ┌─────────────────┐
                                                │ /package-addon  │
                                                │ Release ZIP     │
                                                └─────────────────┘
```

### Version Upgrade Workflow
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│/check-compat    │ ──► │/compare-api-    │ ──► │ /upgrade-addon  │
│ Find issues     │     │ versions        │     │ Apply fixes     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                                                        ▼
                                                ┌─────────────────┐
                                                │ /test-addon     │
                                                │ Verify fixes    │
                                                └─────────────────┘
```

### Debug Workflow
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ /inspect-scene  │ ──► │ /test-in-blender│ ──► │/add-performance │
│ Check context   │     │ Test operator   │     │ -metrics        │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Release Workflow
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ /bump-version   │ ──► │/update-changelog│ ──► │    /build       │
│ Set version     │     │ Document changes│     │ Create package  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
        ┌───────────────────────────────────────────────┘
        ▼
┌─────────────────┐     ┌─────────────────┐
│   git commit    │ ──► │    git tag      │
│ + git push      │     │  v1.0.0         │
└─────────────────┘     └─────────────────┘

Or use /release for the complete automated workflow!
```

---

## Subagents Reference

Subagents are specialized reviewers that Claude can invoke automatically:

| Agent | Specialty | Triggered By |
|-------|-----------|--------------|
| `blender-api-expert` | API usage, patterns | Code review requests |
| `ui-designer` | Panel layouts, UX | UI-related changes |
| `addon-tester` | Test case creation | Testing requests |
| `performance-auditor` | Optimization | Performance concerns |
| `code-reviewer` | General quality | Code review |
| `version-compatibility-expert` | Multi-version | Compatibility checks |
| `blender-live-tester` | MCP live testing | Live test commands |
| `release-manager` | Versioning, changelog, packaging | Release commands |

---

## Skills Reference

Skills provide expert knowledge Claude uses automatically:

| Skill | Use Case |
|-------|----------|
| `blender-api-patterns` | Operators, properties, context |
| `blender-performance` | Optimization, batch ops |
| `blender-ui-patterns` | Panels, layouts, widgets |
| `addon-architecture` | Multi-file structure, registration |
| `blender-version-compatibility` | Version detection, compat wrappers |
| `blender-mcp-workflows` | Live testing patterns |
| `blender-documentation` | API reference navigation |
| `performance-optimization` | Profiling, timing |
| `threading-async` | Background tasks, timers |

---

## File Structure Reference

```
your-addon-project/
├── .claude/
│   ├── CLAUDE.md              # Development standards (READ THIS)
│   ├── commands/              # 20 slash commands
│   ├── skills/                # 9 expert knowledge bases
│   ├── agents/                # 8 specialized reviewers
│   ├── hooks/                 # Pre-commit, post-edit, pre-package
│   └── plugins/               # Bundled workflow configuration
│
├── .github/
│   ├── ISSUE_TEMPLATE/        # Bug report, feature request, compat issue
│   └── PULL_REQUEST_TEMPLATE.md
│
├── addon_name/                # YOUR ADDON CODE
│   ├── __init__.py            # bl_info + registration
│   ├── operators.py           # Operator classes
│   ├── panels.py              # UI panels
│   ├── properties.py          # Property definitions
│   ├── utils.py               # Helper functions
│   └── compat.py              # Version compatibility
│
├── build/                     # Build output (generated)
│   └── addon_name-vX.Y.Z.zip  # Distribution package
│
├── tests/                     # Test scripts
│   ├── conftest.py            # Pytest fixtures
│   ├── test_operators.py      # Operator tests
│   ├── test_properties.py     # Property tests
│   ├── test_utils.py          # Utility tests
│   └── run_blender_tests.py   # Blender test runner
│
├── docs/                      # Documentation
├── build.py                   # Build automation script
├── CHANGELOG.md               # Version history
├── CONTRIBUTING.md            # Contribution guidelines
└── README.md                  # User-facing docs
```

---

## Common Patterns Quick Reference

### Operator ID Format
```
Class:  CATEGORY_OT_operator_name
ID:     category.operator_name

Example:
Class:  MESH_OT_custom_subdivide
ID:     mesh.custom_subdivide
```

### Panel ID Format
```
Class:  CATEGORY_PT_panel_name

Example:
Class:  VIEW3D_PT_my_tools
```

### Version Detection
```python
import bpy

if bpy.app.version >= (4, 0, 0):
    # Blender 4.0+ code
elif bpy.app.version >= (3, 0, 0):
    # Blender 3.x code
```

### Operator Return Values
```python
return {'FINISHED'}      # Success
return {'CANCELLED'}     # Failed/aborted
return {'RUNNING_MODAL'} # Modal operator running
return {'PASS_THROUGH'}  # Let other handlers process
```

---

## First Addon Tutorial

### Step 1: Setup Project
```
1. Copy blender-addon-template/ to Desktop/my_first_addon/
2. Rename addon_name/ to my_tools/
3. Open folder in Claude Code
```

### Step 2: Update bl_info
Edit `my_tools/__init__.py`:
```python
bl_info = {
    "name": "My Tools",
    "author": "Your Name",
    "version": (1, 0, 0),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > My Tools",
    "description": "My first Blender addon",
    "category": "Object",
}
```

### Step 3: Create Your First Operator
Run in Claude Code:
```
/new-operator
```
Answer the prompts:
- Name: `random_color`
- Category: `OBJECT`
- Description: `Assign random color to selected objects`
- Undo: yes
- Properties dialog: no
- UI placement: panel

### Step 4: Test the Addon

**Option A: Manual Install**
1. ZIP the `my_tools/` folder
2. Blender → Edit → Preferences → Add-ons → Install
3. Enable "My Tools"
4. Press N in 3D View → My Tools tab

**Option B: Live Test (requires MCP)**
```
/test-in-blender
```

### Step 5: Package for Release
```
/package-addon
```

---

## Testing Your Addon

### Quick Testing Methods

| Method | Command | When to Use |
|--------|---------|-------------|
| Live test | `/test-in-blender` | Real-time testing via MCP |
| Reload test | `/test-addon` | After code changes |
| Manual test | Install ZIP in Blender | Final verification |

### Running Automated Tests

```bash
# Unit tests (no Blender required)
python -m pytest tests/test_utils.py -v

# All tests inside Blender
blender --background --python tests/run_blender_tests.py

# Specific test file in Blender
blender --background --python tests/run_blender_tests.py -- --test-file test_operators.py
```

### Test Files

| File | Purpose |
|------|---------|
| `tests/conftest.py` | Pytest fixtures and configuration |
| `tests/test_operators.py` | Operator registration and behavior tests |
| `tests/test_properties.py` | Property validation tests |
| `tests/test_utils.py` | Utility function tests (no Blender needed) |
| `tests/run_blender_tests.py` | Script to run pytest inside Blender |

See `tests/README.md` for detailed testing documentation.

---

## Troubleshooting

### Addon doesn't appear after install
- Check Blender console (Window → Toggle System Console) for errors
- Verify bl_info is properly formatted
- Ensure __init__.py has register/unregister functions

### Operator grayed out
- Check poll() method - does context meet requirements?
- Verify you have correct object selected/mode active

### Changes not reflecting
- Blender caches addons - use `/test-addon` to force reload
- Or restart Blender completely

### MCP commands not working
- Verify Blender MCP server is running
- Check .mcp.json configuration
- Ensure Blender is open with MCP addon enabled

### Version compatibility errors
- Run `/check-compatibility` to identify issues
- Use `/compare-api-versions` to understand changes
- Add version guards with `bpy.app.version`

---

## Tips & Best Practices

1. **Read CLAUDE.md first** - Contains all conventions and patterns
2. **Use live testing** - MCP makes iteration much faster
3. **Check compatibility early** - Run `/check-compatibility` before release
4. **Let agents review** - They catch common API mistakes
5. **Use skills for reference** - Ask Claude about patterns when unsure
6. **Keep operators focused** - One operator = one action
7. **Always implement poll()** - Prevents crashes from invalid context
8. **Free your BMesh** - Memory leaks are common pitfall
9. **Test on min/max versions** - If supporting multiple Blender versions

---

## Quick Command Reference Card

```
┌────────────────────────────────────────────────────────────────┐
│                    DEVELOPMENT                                  │
│  /new-operator        Create new operator                      │
│  /new-panel           Create new UI panel                      │
│  /setup-blender-dev   Initialize project                       │
├────────────────────────────────────────────────────────────────┤
│                      TESTING                                    │
│  /test-addon          Reload and validate                      │
│  /test-in-blender     Live test (MCP)                          │
│  /inspect-scene       Query scene (MCP)                        │
│  /create-test-scene   Setup test env (MCP)                     │
│  /live-dev            Interactive mode (MCP)                   │
├────────────────────────────────────────────────────────────────┤
│                   COMPATIBILITY                                 │
│  /check-compatibility     Scan for issues                      │
│  /upgrade-addon           Migrate to new version               │
│  /add-version-support     Multi-version support                │
│  /compare-api-versions    API diff between versions            │
├────────────────────────────────────────────────────────────────┤
│                   DOCUMENTATION                                 │
│  /docs-lookup         Search Blender docs                      │
│  /api-example         Find code examples                       │
├────────────────────────────────────────────────────────────────┤
│                 RELEASE & BUILD                                 │
│  /build               Package addon (build.py)                 │
│  /bump-version        Update version + changelog               │
│  /update-changelog    Document changes                         │
│  /release             Full release workflow                    │
│  /package-addon       Quick distribution ZIP                   │
│  /add-performance-metrics  Add profiling                       │
└────────────────────────────────────────────────────────────────┘
```

---

## Resources

- [Blender Python API](https://docs.blender.org/api/current/)
- [Blender Manual](https://docs.blender.org/manual/en/latest/)
- [Blender MCP Server](https://github.com/ahujasid/blender-mcp)
- [Claude Code Documentation](https://docs.anthropic.com/claude-code)

---

*Template Version: 1.0 | Last Updated: 2025*
