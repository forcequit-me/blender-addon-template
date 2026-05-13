---
description: Package addon for distribution
argument-hint: "[legacy|extension|both]"
allowed-tools: Bash, Read, Glob
---

Package the addon into a distributable zip file with proper structure.

**Process:**

1. **Validate addon before packaging:**
   - Verify `bl_info` is complete and accurate
   - Check version number is updated
   - Ensure all required files are present
   - Remove any development/debug code
   - Check for hardcoded paths

2. **Prepare files:**
   - Include only necessary files:
     - `__init__.py`
     - All `.py` module files
     - Required assets (icons, presets)
     - `README.md` (if included)
   - Exclude:
     - `__pycache__` directories
     - `.pyc` files
     - Test files
     - Development configuration
     - `.git` directory

3. **Create zip structure:**
   ```
   addon_name.zip
   └── addon_name/
       ├── __init__.py
       ├── operators.py
       ├── panels.py
       ├── properties.py
       ├── utils.py
       ├── compat.py
       └── (other modules)
   ```

4. **Generate packaging script:**
   ```python
   import zipfile
   import os
   from pathlib import Path

   addon_name = "addon_name"
   version = "1_0_0"  # From bl_info

   # Files to include
   include_extensions = {'.py', '.json', '.md'}
   exclude_dirs = {'__pycache__', '.git', 'tests', '.vscode'}
   exclude_files = {'*.pyc', '*.pyo', '.DS_Store', 'Thumbs.db'}

   output_file = f"{addon_name}_v{version}.zip"

   with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zf:
       addon_path = Path(addon_name)
       for file_path in addon_path.rglob('*'):
           if file_path.is_file():
               # Check exclusions
               if any(ex in file_path.parts for ex in exclude_dirs):
                   continue
               if file_path.suffix not in include_extensions:
                   continue

               # Add to zip with proper path
               arc_name = file_path
               zf.write(file_path, arc_name)
               print(f"Added: {arc_name}")

   print(f"\nCreated: {output_file}")
   ```

5. **Post-packaging verification:**
   - Test installation from zip in fresh Blender
   - Verify all features work
   - Check no missing dependencies

**bl_info checklist:**
- [ ] `name` is descriptive
- [ ] `author` is set
- [ ] `version` is updated (tuple format)
- [ ] `blender` minimum version is correct
- [ ] `location` describes where to find addon
- [ ] `description` is clear and concise
- [ ] `category` matches addon type
- [ ] `doc_url` points to documentation (if available)

**Output:**
- Create zip file: `addon_name_vX_Y_Z.zip`
- Report package contents
- Confirm successful packaging
