import bpy
import math
import copy

def auto_unwrap(input_obj, context):
    sut_tool = context.scene.my_tool

    bpy.ops.object.select_all(action='DESELECT')
    if (input_obj.type == 'MESH'):
        input_obj.select_set(True)
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action='SELECT') # for all faces
        bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=sut_tool.sut_island_margin, area_weight=0.0, correct_aspect=True, scale_to_bounds=False)
        bpy.ops.object.mode_set(mode="OBJECT")
        input_obj.select_set(False)

def copy_selected_objects_(to_col, linked):
    for o in bpy.context.selected_objects:
        dupe = o.copy()
        if not linked and o.data:
            dupe.data = dupe.data.copy()
        to_col.objects.link(dupe)

def select_children_objects_recursively(input_col):
    # Select all the objects
    for obj in input_col.all_objects:
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

    for child_col in input_col.children:
        select_children_objects_recursively(child_col)

def make_single_mesh(selected_collection, context):
    # For scene / own global variables
    sut_tool = context.scene.my_tool

    # Go into object mode (maybe actually check stuff instead of this)
    try:
        bpy.ops.object.mode_set(mode="OBJECT")
    except:
        dont_complain = 85

    # Deselect everything
    bpy.ops.object.select_all(action='DESELECT')

    # Temp work
    select_children_objects_recursively(selected_collection)

    # Clone the selected collection
    temp_collection_name = 'SUT_COL_' + selected_collection.name
    temp_collection = bpy.data.collections.new(name=temp_collection_name)
    copy_selected_objects_(temp_collection, 0)
    bpy.context.scene.collection.children.link(temp_collection)

    # Deselect everything
    bpy.ops.object.select_all(action='DESELECT')

    # Select all objects as active
    select_children_objects_recursively(temp_collection)

    # Merge the objects
    bpy.ops.object.join()
    new_merged = temp_collection.all_objects[0]

    # Apply transform (Fixes scaling when uv unwrapping + sets object origin to world center)
    new_merged.select_set(True)
    bpy.ops.object.transform_apply(location=True, rotation=False, scale=True)
    new_merged.select_set(False)

    # Prepare naming for the final mesh
    mesh_name = 'SM_' + selected_collection.name
    mesh_collection = bpy.data.collections[sut_tool.final_col_name]

    # Check if mesh exists, remove if it does
    try:
        old_mesh = bpy.data.collections[sut_tool.final_col_name].objects[mesh_name]
        bpy.data.objects.remove(old_mesh)
    except:
        dont_complain = 85

    # Set the new name, now that it is available
    new_merged.name = mesh_name

    # Move to "Mesh" collection
    mesh_collection.objects.link(new_merged)
    temp_collection.objects.unlink(new_merged)

    # Delete the temp collection
    bpy.data.collections.remove(temp_collection)

    # Auto unwrap
    auto_unwrap(new_merged, context)



class Sut_OT_Operator(bpy.types.Operator):
    bl_idname = "view3d.sut"
    bl_label = "SUT"
    bl_description = "SUT"

    def execute(self, context):
        # For scene / own global variables
        sut_tool = context.scene.my_tool

        # Check if collections don't exist, and create them
        try:
            bpy.data.collections[sut_tool.greybox_col_name] 
        except:
            self.report({'ERROR'}, "You have not created a '" + sut_tool.greybox_col_name + "' greybox collection yet!")
            return {'FINISHED'}
        try:
            bpy.data.collections[sut_tool.final_col_name]
        except:
            new_col = bpy.data.collections.new(name=sut_tool.final_col_name)
            bpy.context.scene.collection.children.link(new_col)


        # Unhide the Final Collection | We don't know what is going on but it works
        bpy.context.scene.view_layers[0].layer_collection.children[sut_tool.final_col_name].hide_viewport = False

        # Unhide the Greybox Collection | We don't know what is going on but it works
        bpy.context.scene.view_layers[0].layer_collection.children[sut_tool.greybox_col_name].hide_viewport = False
        
        # Cleanup Mesh Collection
        for obj in bpy.data.collections[sut_tool.final_col_name].all_objects:
            bpy.data.objects.remove(obj)

        # Every collection gets merged into it's own unique mesh (or all collections is a single big mesh)
        greybox_collection = bpy.data.collections[sut_tool.greybox_col_name]
        if sut_tool.every_col_is_own_mesh is True:
            # Get final collection, loop over every child collection and run make_single_mesh
            for col in greybox_collection.children:
                make_single_mesh(col, context)
        else:
            make_single_mesh(greybox_collection, context)

        # For every single object in the final collection, set the texel density
        final_collection = bpy.data.collections[sut_tool.final_col_name]
        select_children_objects_recursively(final_collection)


        bpy.ops.object.preset_set(td_value=sut_tool.sut_texel_density)
        bpy.context.scene.td.texture_size = sut_tool.sut_texture_size
        bpy.ops.object.texel_density_set()
        bpy.ops.object.select_all(action='DESELECT')

        if sut_tool.sut_send_to_unreal is True:
            bpy.ops.wm.send2ue()

        # Hide the Collection | We don't know what is going on but it works
        bpy.context.scene.view_layers[0].layer_collection.children[sut_tool.final_col_name].hide_viewport = True
        return {'FINISHED'}
