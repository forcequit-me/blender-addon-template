# Testing Guide

This folder contains tests for the Blender addon. Tests can be run outside Blender (for unit tests) or inside Blender (for integration tests).

## Test Structure

```
tests/
├── README.md              # This file
├── conftest.py            # Pytest configuration and fixtures
├── test_operators.py      # Operator tests
├── test_properties.py     # Property validation tests
├── test_utils.py          # Utility function tests
└── run_blender_tests.py   # Script to run tests inside Blender
```

## Running Tests

### Outside Blender (Unit Tests)

For testing utility functions and logic that doesn't require Blender:

```bash
# Install test dependencies
pip install pytest fake-bpy-module-latest

# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_utils.py -v

# Run tests matching a pattern
python -m pytest tests/ -k "test_validate" -v

# Run with coverage report
pip install pytest-cov
python -m pytest tests/ --cov=addon_name --cov-report=html
```

### Inside Blender (Integration Tests)

For testing operators, panels, and Blender API interactions:

```bash
# Run all Blender tests
blender --background --python tests/run_blender_tests.py

# Run with specific Blender version
"C:\Program Files\Blender Foundation\Blender 4.0\blender.exe" --background --python tests/run_blender_tests.py

# Run specific test file inside Blender
blender --background --python tests/run_blender_tests.py -- --test-file test_operators.py
```

### Using Claude Code

```
/test-addon          # Quick validation
/test-in-blender     # Live testing via MCP
```

## Writing Tests

### Unit Tests (No Blender Required)

```python
# tests/test_utils.py
import pytest
from addon_name.utils import calculate_something

class TestCalculateSomething:
    def test_with_valid_input(self):
        result = calculate_something(5, 10)
        assert result == 15

    def test_with_zero(self):
        result = calculate_something(0, 10)
        assert result == 10

    def test_with_negative(self):
        with pytest.raises(ValueError):
            calculate_something(-1, 10)
```

### Integration Tests (Require Blender)

```python
# tests/test_operators.py
import bpy
import pytest

class TestMyOperator:
    @pytest.fixture(autouse=True)
    def setup(self):
        """Reset scene before each test."""
        bpy.ops.wm.read_factory_settings(use_empty=True)
        yield
        # Cleanup after test if needed

    def test_operator_registered(self):
        """Verify operator is registered."""
        assert hasattr(bpy.ops.object, 'my_operator')

    def test_operator_poll_no_object(self):
        """Operator poll fails with no active object."""
        bpy.context.view_layer.objects.active = None
        assert bpy.ops.object.my_operator.poll() == False

    def test_operator_executes(self):
        """Operator executes successfully."""
        # Create test object
        bpy.ops.mesh.primitive_cube_add()
        obj = bpy.context.active_object

        # Execute operator
        result = bpy.ops.object.my_operator()

        assert result == {'FINISHED'}
```

## Test Categories

### 1. Registration Tests
Verify addon registers correctly:
- All operators registered
- All panels registered
- Properties attached correctly
- No registration errors

### 2. Operator Tests
Test operator behavior:
- poll() returns correct values
- execute() succeeds with valid input
- execute() fails gracefully with invalid input
- Undo/redo works correctly
- Properties affect behavior

### 3. Panel Tests
Test UI panels:
- Panel appears in correct location
- Panel draws without errors
- Properties display correctly

### 4. Edge Case Tests
Test error handling:
- Empty selection
- Wrong object type
- Invalid property values
- Missing dependencies

### 5. Performance Tests
Test performance-critical code:
- Large dataset handling
- Batch operations
- Memory usage

## Fixtures

Common fixtures are defined in `conftest.py`:

```python
@pytest.fixture
def cube():
    """Create a cube and return it."""
    bpy.ops.mesh.primitive_cube_add()
    return bpy.context.active_object

@pytest.fixture
def empty_scene():
    """Reset to empty scene."""
    bpy.ops.wm.read_factory_settings(use_empty=True)
    yield
    bpy.ops.wm.read_factory_settings(use_empty=True)
```

## Mocking Blender

For unit tests that don't need full Blender:

```python
from unittest.mock import MagicMock, patch

def test_without_blender():
    # Mock bpy module
    mock_bpy = MagicMock()
    mock_bpy.context.active_object.name = "Cube"

    with patch.dict('sys.modules', {'bpy': mock_bpy}):
        from addon_name.utils import get_object_name
        result = get_object_name()
        assert result == "Cube"
```

## Continuous Integration

For GitHub Actions, create `.github/workflows/tests.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install pytest fake-bpy-module-latest

      - name: Run unit tests
        run: python -m pytest tests/test_utils.py -v
```

## Tips

1. **Keep tests fast** - Mock expensive operations
2. **Test one thing** - Each test should verify one behavior
3. **Use descriptive names** - `test_operator_fails_with_no_selection`
4. **Reset state** - Clean up between tests
5. **Test edge cases** - Empty, null, extreme values
6. **Document test purpose** - Use docstrings
