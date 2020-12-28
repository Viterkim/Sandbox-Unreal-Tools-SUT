bl_info = {
    "name" : "SUT - Sandbox Unreal Tools",
    "author" : "ExoMemphiz & Viter",
    "description" : "Makes prototyping / greyboxing levels in unreal engine an easier process. Idea is to reduce 'double work' when having to place assets multiple times when you are prototyping anyway.",
    "blender" : (2, 91, 0),
    "version" : (0, 0, 1),
    "location" : "View3D",
    "warning" : "",
    "category" : "Generic"
}

import bpy

from . sut_op import Sut_OT_Operator 
from . sut_properties import SutProperties 
from . sut_panel import Sut_PT_Panel

from bpy.utils import (register_class, unregister_class)
from bpy.props import PointerProperty

classes = (Sut_OT_Operator, Sut_PT_Panel, SutProperties)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.my_tool = PointerProperty(type=SutProperties)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.my_tool


if __name__ == "__main__":
    register()