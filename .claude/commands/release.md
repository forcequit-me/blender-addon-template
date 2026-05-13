---
description: Complete release workflow - version, changelog, package, and tag
argument-hint: "[major|minor|patch]"
allowed-tools: Read, Edit, Bash, Grep
---

Execute a complete release workflow: bump version, finalize changelog, package addon, and create git tag.

**This command orchestrates:**
1. `/bump-version` - Update version number
2. `/update-changelog` - Finalize changelog for release
3. `/build` - Create distribution package
4. Git operations - Commit and tag

**Ask user:**
1. What type of release?
   - `patch` - Bug fix release (1.0.0 → 1.0.1)
   - `minor` - Feature release (1.0.0 → 1.1.0)
   - `major` - Major release (1.0.0 → 2.0.0)

2. Summarize the changes for this release (for changelog)

3. Any additional release notes?

**Process:**

### Step 1: Pre-flight Checks
```bash
# Check for uncommitted changes
git status

# Validate addon structure
python build.py validate
```
- If uncommitted changes exist, ask user to commit or stash first
- If validation fails, stop and report errors

### Step 2: Version Bump
```bash
python build.py version --bump {type}
```
- Note old and new version numbers

### Step 3: Update Changelog
- Read CHANGELOG.md
- Move [Unreleased] content to new version section
- Add release date (today)
- Add user-provided release notes
- Clear [Unreleased] section for future changes

### Step 4: Package Addon
```bash
python build.py package --clean
```
- Create distribution ZIP
- Note file size and location

### Step 5: Git Operations
```bash
# Stage changes
git add __init__.py CHANGELOG.md

# Commit
git commit -m "chore: release v{version}"

# Create annotated tag
git tag -a v{version} -m "Release v{version}

{changelog excerpt}"
```

### Step 6: Summary Report

```
╔═══════════════════════════════════════════════════════════╗
║                    RELEASE COMPLETE                        ║
╠═══════════════════════════════════════════════════════════╣
║  Version:    1.0.0 → 1.1.0                                ║
║  Package:    build/addon_name-v1.1.0.zip                  ║
║  Size:       45.2 KB                                      ║
║  Git Tag:    v1.1.0                                       ║
╠═══════════════════════════════════════════════════════════╣
║  Next Steps:                                              ║
║  • Push to remote:  git push && git push --tags           ║
║  • Create GitHub release with the ZIP                     ║
║  • Update documentation if needed                         ║
╚═══════════════════════════════════════════════════════════╝
```

**Abort conditions:**
- Uncommitted changes (unless user confirms)
- Validation errors
- Git not initialized
- Already on a release tag

**Rollback instructions (if needed):**
```bash
# Undo commit (keep changes)
git reset --soft HEAD~1

# Delete tag
git tag -d v{version}

# Restore previous version
python build.py version {old_version}
```
