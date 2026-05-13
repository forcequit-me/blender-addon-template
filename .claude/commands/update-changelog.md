---
description: Update changelog with recent changes
allowed-tools: Read, Edit, Bash, Grep
---

Update the CHANGELOG.md file with recent changes, either from git history or manual input.

**Ask user:**
1. How do you want to update the changelog?
   - `manual` - I'll describe the changes
   - `from-git` - Generate from recent git commits
   - `review` - Show me the current changelog to review

**Process:**

## If `manual` selected:

1. Ask what type of changes to add:
   - Added (new features)
   - Changed (changes to existing functionality)
   - Deprecated (features to be removed)
   - Removed (removed features)
   - Fixed (bug fixes)
   - Security (security fixes)

2. For each selected type, ask for bullet points

3. Update CHANGELOG.md [Unreleased] section with the entries

## If `from-git` selected:

1. Run git log to get recent commits:
   ```bash
   git log --oneline -20
   ```

2. Parse commit messages and categorize:
   - `feat:` → Added
   - `fix:` → Fixed
   - `change:` or `refactor:` → Changed
   - `deprecate:` → Deprecated
   - `remove:` → Removed
   - `security:` → Security

3. Show proposed changelog entries to user for approval

4. Update CHANGELOG.md with approved entries

## If `review` selected:

1. Read and display current CHANGELOG.md
2. Ask if user wants to make any changes
3. Offer to help reorganize or reformat

**CHANGELOG.md Format:**

```markdown
# Changelog

## [Unreleased]

### Added
- Entry here

### Changed
- Entry here

### Fixed
- Entry here

---

## [1.0.0] - 2024-01-15

### Added
- Initial release
```

**Guidelines for entries:**
- Start with a verb (Add, Fix, Change, Remove, Update)
- Be concise but descriptive
- Reference issue numbers if applicable: `Fix crash on startup (#123)`
- Group related changes together
- Use consistent formatting

**After completion:**
- Show the updated [Unreleased] section
- Remind that `/bump-version` will move these to a versioned release
