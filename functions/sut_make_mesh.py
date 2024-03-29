import bpy

from . sut_utils import (
    auto_unwrap,
    auto_smooth_normals,
    copy_selected_objects, 
    select_children_objects_recursively
)

def make_single_mesh(selected_collection, context):
    # For scene / own global variables
    sut_tool = context.scene.sut_tool

    # Avoid "Operator bpy.ops.object.mode_set.poll() Context missing active object"
    context.view_layer.objects.active = selected_collection.all_objects[0]

    # Go into object mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # Deselect everything
    bpy.ops.object.select_all(action='DESELECT')

    # Select all objects as active
    select_children_objects_recursively(selected_collection)

    # Clone the selected collection
    temp_collection_name = 'SUT_COL_' + selected_collection.name
    temp_collection = bpy.data.collections.new(name=temp_collection_name)
    copy_selected_objects(temp_collection, 0)
    bpy.context.scene.collection.children.link(temp_collection)

    # Deselect everything
    bpy.ops.object.select_all(action='DESELECT')

    # Select all objects as active
    select_children_objects_recursively(temp_collection)

    # Apply modifiers
    bpy.ops.object.convert(target='MESH')

    # Merge the objects
    bpy.ops.object.join()
    new_merged = temp_collection.all_objects[0]

    # Apply transform (Fixes scaling when uv unwrapping + sets object origin to world center)
    new_merged.select_set(True)
    bpy.ops.object.transform_apply(
        location=True,
        rotation=False,
        scale=True
    )
    new_merged.select_set(False)

    # Prepare naming for the final mesh
    mesh_name = 'SM_' + selected_collection.name
    mesh_collection = bpy.data.collections[sut_tool.final_col_name]

    # Check if mesh exists, remove if it does
    try:
        old_mesh = bpy.data.collections[sut_tool.final_col_name].objects[mesh_name]
        bpy.data.objects.remove(old_mesh)
    except:
        pass

    # Set the new name, now that it is available
    new_merged.name = mesh_name

    # Move to "Mesh" collection
    mesh_collection.objects.link(new_merged)
    temp_collection.objects.unlink(new_merged)

    # Delete the temp collection
    bpy.data.collections.remove(temp_collection)

    # Auto smooth normals
    new_merged.select_set(True)
    bpy.context.view_layer.objects.active = new_merged
    if sut_tool.auto_smooth_enable is True:
        auto_smooth_normals(context)
    else:
        bpy.ops.object.shade_flat()
    bpy.ops.object.select_all(action='DESELECT')

    # Auto unwrap
    auto_unwrap(new_merged, context)