from bpy import context
from bpy.context import (
    scene,
    selected_objects
)

from bpy.data import collections
from bpy.ops import object as obj

def select_children_objects_recursively(input_col):
    '''Recursively selects all objects within a collection, and its children'''
    # Select all the objects
    for obj in input_col.all_objects:
        obj.select_set(True)
        context.view_layer.objects.active = obj

    for child_col in input_col.children:
        select_children_objects_recursively(child_col)

def copy_selected_objects(to_col, linked):
    '''Duplicates selected objects into a desired collection'''
    for o in selected_objects:
        dupe = o.copy()
        if not linked and o.data:
            dupe.data = dupe.data.copy()
        to_col.objects.link(dupe)

def use_texel_density(sut_tool):
    '''Uses the Texel Density addon with desired values'''
    obj.preset_set(td_value=sut_tool.sut_texel_density)
    scene.td.texture_size = sut_tool.sut_texture_size
    obj.texel_density_set()
    obj.select_all(action='DESELECT')

def validate_collection_names(self, sut_tool):
    """Ensures greybox collection is made & final collection either exists or will be created  
      
    Returns:
        bool: Returning value
    """
    
    # Check if collections don't exist, and create them
    try:
        collections[sut_tool.greybox_col_name] 
    except:
        self.report(
            {'ERROR'}, 
            "You have not created a '" + sut_tool.greybox_col_name + "' greybox collection yet!"
        )
        return False
    try:
        collections[sut_tool.final_col_name]
    except:
        new_col = collections.new(name=sut_tool.final_col_name)
        scene.collection.children.link(new_col)

    return True

def hide_collection_viewport(collection_name, flag):
    '''Hides or Shows a specified collection, based on which flag is given'''
    # We don't know what is going on but it works
    scene.view_layers[0].layer_collection.children[collection_name].hide_viewport = flag