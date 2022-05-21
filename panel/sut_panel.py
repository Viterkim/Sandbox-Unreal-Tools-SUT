import bpy

from bpy.types import Panel

# Add to this list after adding a property to SutProperties
UI_PROPERTIES = [
    # "sut_island_margin", # Disabling to cleanup UI
    # "sut_angle_limit", # Disabling to cleanup UI
    "sut_texture_size",
    "sut_texel_density",
    "greybox_col_name",
    # "final_col_name", # Seems to be hardcoded now, so disabled this from the UI
    "auto_smooth_angle",
    "auto_smooth_enable",
    "every_col_is_own_mesh",
    "sut_send_to_unreal"
]

class Sut_PT_Panel(Panel):
    bl_idname = "SUT_PT_Panel"
    bl_label = "Sandbox Unreal Tools"
    bl_category = "SUT"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        sut_tool = scene.sut_tool

        for prop in UI_PROPERTIES:
            layout.prop(sut_tool, prop)

        row = layout.row()
        row.operator('view3d.sut', text="SUT")