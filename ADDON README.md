# Addon Name

Brief description of what this addon does.

## Features

- Feature 1: Description
- Feature 2: Description
- Feature 3: Description

## Requirements

- Blender 3.6.0 or newer
- No external dependencies

## Installation

### From ZIP File

1. Download the latest release ZIP file
2. In Blender, go to **Edit > Preferences > Add-ons**
3. Click **Install...** and select the ZIP file
4. Enable the addon by checking the checkbox

### Manual Installation

1. Download or clone this repository
2. Copy the `addon_name` folder to your Blender addons directory:
   - **Windows:** `%APPDATA%\Blender Foundation\Blender\{version}\scripts\addons\`
   - **macOS:** `~/Library/Application Support/Blender/{version}/scripts/addons/`
   - **Linux:** `~/.config/blender/{version}/scripts/addons/`
3. Enable the addon in Blender preferences

## Usage

### Location

The addon panel is located in the **3D View Sidebar** (press `N` to toggle) under the **Addon Tab** category.

### Basic Workflow

1. Select an object in the 3D viewport
2. Open the addon panel in the sidebar
3. Adjust settings as needed
4. Click the operator button to execute

### Operators

| Operator | Shortcut | Description |
|----------|----------|-------------|
| Example Operator | - | Moves the active object on the Z axis |

### Properties

| Property | Type | Description |
|----------|------|-------------|
| Float Value | Float | Example float property (0-10) |
| Mode | Enum | Operation mode selection |
| Enable Feature | Boolean | Toggle feature on/off |

## Troubleshooting

### Common Issues

**Addon doesn't appear after installation**
- Make sure you enabled the addon in preferences
- Check the Blender console for error messages

**Operator is grayed out**
- Ensure you have an active object selected
- Check that you're in Object mode

### Getting Help

- Check the [Issues](../../issues) page for known problems
- Create a new issue with detailed information about your problem

## Development

See [DEVELOPMENT.md](DEVELOPMENT.md) for development setup and guidelines.

## License

[Specify your license here]

## Credits

- Author: Your Name
- Contributors: List contributors
