import bpy

from bpy.props import (BoolProperty, StringProperty, FloatProperty, EnumProperty)
from bpy.types import PropertyGroup


class SutProperties(PropertyGroup):
    sut_island_margin: FloatProperty(
        name="UV Island Margin",
        description="Bigger greyboxes might need a bigger island margin when smart uv unwrapping",
        step=0.01,
        min=0,
        max=5,
        precision=3,
        default=0.005
        )
    sut_texel_density: EnumProperty(
        name="Texel Density",
        description="Set texel density in the Texel Density addon",
        items=[ ("40.96", "40.96", ""),
                ("20.48", "20.48", ""),
                ("10.24", "10.24", ""),
                ("5.12", "5.12", ""),
                ("2.56", "2.56", ""),
                ("1.28", "1.28", ""),
                ("0.64", "0.64", ""),
               ],
        default="20.48",
        )
    sut_texture_size: EnumProperty(
        name="Texture Size",
        description="Set texture size in the Texel Density addon",
        items=[ ("0", "512px", ""),
                ("1", "1024px", ""),
                ("2", "2048px", ""),
                ("3", "4096px", "")
               ],
        default="2",
        )
    every_col_is_own_mesh: BoolProperty(
        name="Split collection result",
        description="Check if you want every collection to be their own seperate merged mesh\n(Origin will still be world origin)",
        default = False
        )
    sut_send_to_unreal: BoolProperty(
        name="Send to Unreal Engine",
        description="Avoids 2 clicks",
        default = False
        )
    greybox_col_name: StringProperty(
        name="Greybox Col Name",
        description="The greyboxing collection name",
        default = "SUT"
        )
    final_col_name: StringProperty(
        name="Final Col Name",
        description="Final collection for unreal engine, default is 'Mesh' from the UE Tools addon",
        default = "Mesh"
        )
