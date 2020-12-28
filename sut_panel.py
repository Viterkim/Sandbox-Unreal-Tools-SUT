import bpy

class Sut_PT_Panel(bpy.types.Panel):
    bl_idname = "SUT_PT_Panel"
    bl_label = "Sandbox Unreal Tools"
    bl_category = "SUT"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
            layout = self.layout
            scene = context.scene
            sut_tool = scene.my_tool

            layout.prop(sut_tool, "sut_island_margin")
            layout.prop(sut_tool, "sut_texture_size")
            layout.prop(sut_tool, "sut_texel_density")
            layout.prop(sut_tool, "greybox_col_name")
            layout.prop(sut_tool, "final_col_name")
            layout.prop(sut_tool, "every_col_is_own_mesh")
            layout.prop(sut_tool, "sut_send_to_unreal")
            row = layout.row()
            row.operator('view3d.sut', text="SUT")

            # Collection name for greybox collection (SUT)

            # Collection name for final mesh collection (Mesh)