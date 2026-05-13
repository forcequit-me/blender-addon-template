---
description: Build and package addon for distribution
argument-hint: "[package|validate|clean]"
allowed-tools: Bash, Read, Glob
---

Build and package the addon using build.py automation.

**Ask user:**
1. What action do you want to perform?
   - `package` - Create distribution ZIP
   - `validate` - Validate addon structure only
   - `clean` - Remove build artifacts

**Process:**

1. If **package** selected:
   - Run `python build.py validate` first
   - If validation passes, run `python build.py package --clean`
   - Report the output ZIP location and size
   - Remind user how to install in Blender

2. If **validate** selected:
   - Run `python build.py validate`
   - Report any errors or warnings
   - Suggest fixes for any issues found

3. If **clean** selected:
   - Run `python build.py clean`
   - Confirm what was removed

**Output:**
- Show build.py output
- For packaging, display:
  - ZIP file path
  - File count
  - Package size
  - Installation instructions
