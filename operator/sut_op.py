from bpy.types import Operator
from bpy.data import (
    collections,
    objects as objs
)
from bpy.ops import wm

from .. functions.sut_make_mesh import make_single_mesh
from .. functions.sut_utils import (
    hide_collection_viewport,
    select_children_objects_recursively,
    use_texel_density,
    validate_collection_names
)

class Sut_OT_Operator(Operator):
    bl_idname = "view3d.sut"
    bl_label = "SUT"
    bl_description = "SUT"

    def execute(self, context):
        # For scene / own global variables
        sut_tool = context.scene.sut_tool

        if not validate_collection_names(self, sut_tool):
            return {'FINISHED WITH ERRORS'}

        # Unhide the Greybox Collection
        hide_collection_viewport(sut_tool.greybox_col_name, False)
        
        # Unhide the Final Collection
        hide_collection_viewport(sut_tool.final_col_name, False)
        
        
        # Cleanup Mesh Collection
        for obj in collections[sut_tool.final_col_name].all_objects:
            objs.remove(obj)

        # Every collection gets merged into it's own unique mesh (or all collections is a single big mesh)
        greybox_collection = collections[sut_tool.greybox_col_name]
        if sut_tool.every_col_is_own_mesh is True:
            # Get final collection, loop over every child collection and run make_single_mesh
            for col in greybox_collection.children:
                make_single_mesh(col, context)
        else:
            make_single_mesh(greybox_collection, context)

        # For every single object in the final collection, set the texel density
        final_collection = collections[sut_tool.final_col_name]
        select_children_objects_recursively(final_collection)

        use_texel_density(sut_tool)

        if sut_tool.sut_send_to_unreal is True:
            wm.send2ue()

        # Hide the Collection
        hide_collection_viewport(sut_tool.final_col_name, True)
        return {'FINISHED'}
