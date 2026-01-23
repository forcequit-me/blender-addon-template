"""Property definitions for the addon."""

import bpy
from bpy.types import PropertyGroup
from bpy.props import (
    FloatProperty,
    IntProperty,
    BoolProperty,
    StringProperty,
    EnumProperty,
    FloatVectorProperty,
    PointerProperty,
    CollectionProperty,
)


class AddonProperties(PropertyGroup):
    """Main property group for addon settings."""

    example_float: FloatProperty(
        name="Float Value",
        description="An example float property",
        default=1.0,
        min=0.0,
        max=10.0,
        precision=2,
    )

    example_int: IntProperty(
        name="Integer Value",
        description="An example integer property",
        default=5,
        min=0,
        max=100,
    )

    example_bool: BoolProperty(
        name="Enable Feature",
        description="Toggle an example feature",
        default=False,
    )

    example_string: StringProperty(
        name="Text",
        description="An example string property",
        default="",
        maxlen=256,
    )

    example_enum: EnumProperty(
        name="Mode",
        description="Select operation mode",
        items=[
            ('OPTION_A', "Option A", "First option description"),
            ('OPTION_B', "Option B", "Second option description"),
            ('OPTION_C', "Option C", "Third option description"),
        ],
        default='OPTION_A',
    )

    example_color: FloatVectorProperty(
        name="Color",
        description="An example color property",
        subtype='COLOR',
        size=4,
        min=0.0,
        max=1.0,
        default=(1.0, 1.0, 1.0, 1.0),
    )

    example_vector: FloatVectorProperty(
        name="Vector",
        description="An example vector property",
        size=3,
        default=(0.0, 0.0, 0.0),
    )


# Example of a collection item property group
class AddonCollectionItem(PropertyGroup):
    """Property group for items in a collection."""

    name: StringProperty(
        name="Name",
        default="Item",
    )

    enabled: BoolProperty(
        name="Enabled",
        default=True,
    )

    value: FloatProperty(
        name="Value",
        default=0.0,
    )
