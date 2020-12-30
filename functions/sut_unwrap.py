import bpy
import math

from bpy.ops import (
    object as obj,
    mesh,
    uv
)

def auto_unwrap(input_obj, context):
    '''Uses the smart uv unwrapping tool with desired values'''
    sut_tool = context.scene.sut_tool

    obj.select_all(action='DESELECT')
    if (input_obj.type == 'MESH'):
        input_obj.select_set(True)
        obj.mode_set(mode="EDIT")
        mesh.select_all(action='SELECT') # for all faces
        uv.smart_project(
            angle_limit=math.radians(66),
            island_margin=sut_tool.sut_island_margin,
            area_weight=0.0,
            correct_aspect=True,
            scale_to_bounds=False
        )
        obj.mode_set(mode="OBJECT")
        input_obj.select_set(False)