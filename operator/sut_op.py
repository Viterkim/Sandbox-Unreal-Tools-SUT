import bpy

from .. functions.sut_make_mesh import make_single_mesh
from .. functions.sut_utils import (
    hide_collection_viewport,
    select_children_objects_recursively,
    use_texel_density,
    validate_collection_names,
    validate_collection_not_empty
)

class Sut_OT_Operator(bpy.types.Operator):
    bl_idname = "view3d.sut"
    bl_label = "SUT"
    bl_description = "SUT"

    def execute(self, context):
        # For scene / own global variables
        sut_tool = context.scene.sut_tool

        if not validate_collection_names(self, sut_tool):
            return {'CANCELLED'}

        if not validate_collection_not_empty(self, sut_tool):
            return {'CANCELLED'}

        # Unhide the Greybox Collection
        hide_collection_viewport(sut_tool.greybox_col_name, False)
        
        # Unhide the Final Collection
        hide_collection_viewport(sut_tool.final_col_name, False)
        
        # Cleanup Mesh Collection
        for obj in bpy.data.collections[sut_tool.final_col_name].all_objects:
            bpy.data.objects.remove(obj)

        # Every collection gets merged into it's own unique mesh (or all collections is a single big mesh)
        greybox_collection = bpy.data.collections[sut_tool.greybox_col_name]
        greybox_col_has_child_col = len(greybox_collection.children) > 0 # Avoid bug + we don't support deeply nested collections
        if sut_tool.every_col_is_own_mesh is True and greybox_col_has_child_col is True:
            # Get final collection, loop over every child collection and run make_single_mesh
            for col in greybox_collection.children:
                if len(col.all_objects) > 0:
                    make_single_mesh(col, context)
        elif len(greybox_collection.all_objects) > 0:
            make_single_mesh(greybox_collection, context)

        # For every single object in the final collection, set the texel density
        final_collection = bpy.data.collections[sut_tool.final_col_name]
        select_children_objects_recursively(final_collection)

        use_texel_density(sut_tool)

        if sut_tool.sut_send_to_unreal is True:
            bpy.ops.wm.send2ue()

        # Hide the Collection
        hide_collection_viewport(sut_tool.final_col_name, True)
        return {'FINISHED'}
