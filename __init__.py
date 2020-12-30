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

from . operator.sut_op import Sut_OT_Operator 
from . panel.sut_properties import SutProperties 
from . panel.sut_panel import Sut_PT_Panel

from bpy.utils import (
    register_class, 
    unregister_class
)
from bpy.props import PointerProperty

from bpy.types import Scene

classes = (
    Sut_OT_Operator, 
    Sut_PT_Panel, 
    SutProperties
)

def register():
    for cls in classes:
        register_class(cls)
    Scene.sut_tool = PointerProperty(type=SutProperties)

def unregister():
    for cls in reversed(classes):
        unregister_class(cls)
    del Scene.sut_tool


if __name__ == "__main__":
    register()