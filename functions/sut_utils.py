import bpy

def select_children_objects_recursively(input_col):
    '''Recursively selects all objects within a collection, and its children'''
    # Select all the objects
    for obj in input_col.all_objects:
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

    for child_col in input_col.children:
        select_children_objects_recursively(child_col)

def copy_selected_objects(to_col, linked):
    '''Duplicates selected objects into a desired collection'''
    for o in bpy.context.selected_objects:
        dupe = o.copy()
        if not linked and o.data:
            dupe.data = dupe.data.copy()
        to_col.objects.link(dupe)

def use_texel_density(sut_tool):
    '''Uses the Texel Density addon with desired values'''
    bpy.ops.object.preset_set(td_value=sut_tool.sut_texel_density)
    bpy.context.scene.td.texture_size = sut_tool.sut_texture_size
    bpy.ops.object.texel_density_set()
    bpy.ops.object.select_all(action='DESELECT')

def validate_collection_names(self, sut_tool):
    """Ensures greybox collection is made & final collection either exists or will be created  
      
    Returns:
        bool: Returning value
    """
    
    # Check if collections don't exist, and create them
    try:
        bpy.data.collections[sut_tool.greybox_col_name] 
    except:
        self.report(
            {'ERROR'}, 
            "You have not created a '" + sut_tool.greybox_col_name + "' greybox collection yet!"
        )
        return False
    try:
        bpy.data.collections[sut_tool.final_col_name]
    except:
        new_col = bpy.data.collections.new(name=sut_tool.final_col_name)
        bpy.context.scene.collection.children.link(new_col)

    return True

def hide_collection_viewport(collection_name, flag):
    '''Hides or Shows a specified collection, based on which flag is given'''
    # We don't know what is going on but it works
    bpy.context.scene.view_layers[0].layer_collection.children[collection_name].hide_viewport = flag