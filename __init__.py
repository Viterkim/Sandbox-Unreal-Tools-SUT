bl_info = {
    "name" : "SUT - Sandbox Unreal Tools",
    "author" : "ExoMemphiz & Viter",
    "description" : "Faster Greyboxing / Prototyping workflow for Unreal Engine & Blender",
    "blender" : (4, 3, 0),
    "version" : (0, 2, 0),
    "location" : "View3D",
    "warning" : "",
    "category" : "Import-Export"
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