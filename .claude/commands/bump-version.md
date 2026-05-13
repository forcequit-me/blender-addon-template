---
description: Bump addon version and update changelog
argument-hint: "[major|minor|patch]"
allowed-tools: Read, Edit, Bash, Grep
---

Bump the addon version using semantic versioning and update the changelog.

**Ask user:**
1. What type of version bump?
   - `patch` - Bug fixes, minor changes (1.0.0 → 1.0.1)
   - `minor` - New features, backward compatible (1.0.0 → 1.1.0)
   - `major` - Breaking changes, major overhaul (1.0.0 → 2.0.0)
   - `custom` - Set specific version number

2. If `custom` selected:
   - What version number? (format: X.Y.Z)

3. What changes should be noted in the changelog?
   - Ask for summary of changes (Added, Changed, Fixed, etc.)

**Process:**

1. Show current version:
   ```bash
   python build.py version
   ```

2. Bump version:
   ```bash
   python build.py version --bump {type}
   # or for custom:
   python build.py version {X.Y.Z}
   ```

3. Update CHANGELOG.md:
   - Read current CHANGELOG.md
   - Add new version section under [Unreleased]
   - Move [Unreleased] items to new version section
   - Add today's date
   - Include user-provided change notes
   - Categorize into: Added, Changed, Deprecated, Removed, Fixed, Security

4. Show summary:
   - Old version → New version
   - Changelog updates made
   - Remind to commit changes

**Changelog Entry Template:**
```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New feature description

### Changed
- Change description

### Fixed
- Bug fix description
```

**After completion:**
- Suggest running `/build` to package new version
- Remind to commit version bump: `git add -A && git commit -m "chore: bump version to X.Y.Z"`
- Suggest creating git tag: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`
