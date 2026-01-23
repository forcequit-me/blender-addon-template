# Changelog

All notable changes to this addon will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial features in development

### Changed

### Deprecated

### Removed

### Fixed

### Security

---

## [1.0.0] - YYYY-MM-DD

### Added
- Initial release
- Example operator for moving objects on Z axis
- UI panel in 3D View sidebar
- Basic property definitions

### Blender Compatibility
- Minimum: Blender 3.6.0
- Maximum: Blender 4.x (tested up to 4.2)

---

## Version History Template

<!--
Copy this template for each new version:

## [X.Y.Z] - YYYY-MM-DD

### Added
- New features

### Changed
- Changes to existing functionality

### Deprecated
- Features that will be removed in future versions

### Removed
- Features removed in this version

### Fixed
- Bug fixes

### Security
- Security vulnerability fixes

### Blender Compatibility
- Minimum: Blender X.X.X
- Maximum: Blender X.X.X
- Breaking changes: List any API changes that required code updates
-->

---

## Versioning Guide

This addon uses [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0): Incompatible API changes, major feature overhauls
- **MINOR** (0.X.0): New features, backward-compatible
- **PATCH** (0.0.X): Bug fixes, backward-compatible

### Version Bump Checklist

- [ ] Update version in `bl_info` dictionary in `__init__.py`
- [ ] Update this CHANGELOG.md
- [ ] Update README.md if needed
- [ ] Tag release in git: `git tag -a v1.0.0 -m "Release v1.0.0"`
- [ ] Create GitHub release with changelog excerpt

---

[Unreleased]: https://github.com/username/addon-name/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/username/addon-name/releases/tag/v1.0.0
