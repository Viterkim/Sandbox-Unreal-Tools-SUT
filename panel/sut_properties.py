import bpy

from bpy.props import (
    BoolProperty, 
    EnumProperty, 
    FloatProperty, 
    StringProperty
)
from bpy.types import PropertyGroup

# After adding a property, add it as a string to the UI_PROPERTIES constant in sut_panel.py
class SutProperties(PropertyGroup):

    sut_island_margin: FloatProperty(
        name="UV Island Margin",
        description="Bigger greyboxes might need a bigger island margin when smart uv unwrapping",
        min=0,
        max=5,
        step=0.01,
        precision=3,
        default=0.02
    )

    sut_angle_limit: FloatProperty(
        name="UV Degree Angle Limit",
        description="Given in degrees, it will automatically be converted to radians",
        min=0,
        max=360,
        step=1,
        precision=1,
        default=66
    )

    sut_texel_density: EnumProperty(
        name="Texel Density",
        description="Set texel density in the Texel Density addon",
        items=[
            ("40.96", "40.96", ""),
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
        items=[
            ("512", "512", ""),
            ("1024", "1024", ""),
            ("2048", "2048", ""),
            ("4096", "4096", "")
        ],
        default="2048",
    )

    every_col_is_own_mesh: BoolProperty(
        name="Seperate Child Collection Meshes",
        description="Check if you want every collection to be their own seperate merged mesh\n(Origin will still be world origin)",
        default = True
    )

    sut_send_to_unreal: BoolProperty(
        name="Send to Unreal Engine",
        description="Avoids 2 clicks",
        default = True
    )

    greybox_col_name: StringProperty(
        name="Greybox Coll. Name",
        description="The greybox collection name",
        default = "Collection"
    )
    
    final_col_name: StringProperty(
        name="Final Coll. Name",
        description="Final collection for unreal engine.",
        default = "Export" # Seems to be hardcoded now, so disabled this from the UI
    )

    auto_smooth_angle: StringProperty(
        name="Auto Smooth Angle",
        description="Angle for auto smoothing normals on the final mesh",
        default = "30"
    )

    auto_smooth_enable: BoolProperty(
        name="Enable Auto Smooth By Angle",
        description="Enable auto smoothing",
        default = True
    )
