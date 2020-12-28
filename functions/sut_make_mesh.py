from bpy.context import scene
from bpy.data import (
    collections,
    objects
)
from bpy.ops import object as obj

from . sut_unwrap import auto_unwrap
from . sut_utils import (
    copy_selected_objects, 
    select_children_objects_recursively
)

def make_single_mesh(selected_collection, context):
    # For scene / own global variables
    sut_tool = context.scene.sut_tool

    # Go into object mode (maybe actually check stuff instead of this)
    try:
        obj.mode_set(mode="OBJECT")
    except:
        pass

    # Deselect everything
    obj.select_all(action='DESELECT')

    # Temp work
    select_children_objects_recursively(selected_collection)

    # Clone the selected collection
    temp_collection_name = 'SUT_COL_' + selected_collection.name
    temp_collection = collections.new(name=temp_collection_name)
    copy_selected_objects(temp_collection, 0)
    scene.collection.children.link(temp_collection)

    # Deselect everything
    obj.select_all(action='DESELECT')

    # Select all objects as active
    select_children_objects_recursively(temp_collection)

    # Merge the objects
    obj.join()
    new_merged = temp_collection.all_objects[0]

    # Apply transform (Fixes scaling when uv unwrapping + sets object origin to world center)
    new_merged.select_set(True)
    obj.transform_apply(
        location=True,
        rotation=False,
        scale=True
    )
    new_merged.select_set(False)

    # Prepare naming for the final mesh
    mesh_name = 'SM_' + selected_collection.name
    mesh_collection = collections[sut_tool.final_col_name]

    # Check if mesh exists, remove if it does
    try:
        old_mesh = collections[sut_tool.final_col_name].objects[mesh_name]
        objects.remove(old_mesh)
    except:
        pass

    # Set the new name, now that it is available
    new_merged.name = mesh_name

    # Move to "Mesh" collection
    mesh_collection.objects.link(new_merged)
    temp_collection.objects.unlink(new_merged)

    # Delete the temp collection
    collections.remove(temp_collection)

    # Auto unwrap
    auto_unwrap(new_merged, context)