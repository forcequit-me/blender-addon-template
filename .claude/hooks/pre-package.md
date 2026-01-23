# Pre-Package Hook

Runs automatically before packaging the addon for distribution.

## Trigger
Before executing `/build package` or `/release` commands.

## Checks Performed

### 1. Addon Validation
```bash
python build.py validate
```
- Verify bl_info has all required fields
- Check register/unregister functions exist
- Validate version format

### 2. Code Quality
- Check for `print()` statements (should use logging or remove)
- Check for `TODO` or `FIXME` comments that should be addressed
- Verify no hardcoded development paths

### 3. Version Consistency
- bl_info version matches expected release version
- CHANGELOG.md has entry for current version (if releasing)

### 4. File Checks
- No `.pyc` or `__pycache__` in addon folder
- No `.blend1` backup files
- No development-only files (test scripts in root, etc.)

### 5. Documentation
- README.md exists and is not template placeholder
- bl_info has description filled in

## Actions

### On Validation Failure
- List all errors found
- Provide suggested fixes
- **Block packaging** until errors resolved

### On Warnings
- List warnings
- Ask user to confirm proceeding
- Allow packaging to continue

## Warning Patterns to Flag

```python
# Development artifacts
print(           # Use self.report() or logging instead
breakpoint()     # Remove debugging
pdb.set_trace()  # Remove debugging

# Hardcoded paths
"C:\\Users\\"    # Use bpy.path or relative paths
"/home/"         # Use bpy.path or relative paths

# Incomplete code
TODO             # Address or document
FIXME            # Address before release
XXX              # Address before release
HACK             # Review before release
```

## Skip Conditions

Hook can be skipped with `--skip-validation` flag for:
- Development builds
- Testing packages
- Emergency hotfixes (with user confirmation)

## Output Format

```
Pre-Package Validation
======================

[PASS] bl_info validation
[PASS] register/unregister functions
[PASS] Version format
[WARN] Found 2 print() statements
       - operators.py:45
       - utils.py:23
[PASS] No backup files
[PASS] README.md exists

Warnings: 1
Errors: 0

Proceed with packaging? (y/n)
```
