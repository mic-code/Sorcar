import bpy

from bpy.props import PointerProperty, FloatProperty, EnumProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_operator import ScObjectOperatorNode

class ScDecalSlice(Node, ScObjectOperatorNode):
    bl_idname = "ScDecalSlice"
    bl_label = "DecalSlice"
    
    in_object: PointerProperty(type=bpy.types.Object, update=ScNode.update_value)

    def init(self, context):
        super().init(context)
        self.inputs.new("ScNodeSocketObject", "Slice Object").init("in_object", True)
    
    def error_condition(self):
        return(
            super().error_condition()
            or self.inputs["Slice Object"].default_value == None
        )
    
    #https://www.blender.org/forum/viewtopic.php?p=105783
    def AssembleOverrideContextForView3dOps(self):        
        for oWindow in bpy.context.window_manager.windows:
            oScreen = oWindow.screen
            for oArea in oScreen.areas:
                if oArea.type == 'VIEW_3D':
                    for oRegion in oArea.regions:
                        if oRegion.type == 'WINDOW':
                            oContextOverride = {'window': oWindow, 'screen': oScreen, 'area': oArea, 'region': oRegion}
                            return oContextOverride
        raise Exception("ERROR: AssembleOverrideContextForView3dOps() could not find a VIEW_3D with WINDOW region to create override context to enable View3D operators.")
    
    def functionality(self):

        original = bpy.context.view_layer.objects.active

        o = self.inputs["Slice Object"].default_value
        o.select_set(state=True)

        oContextOverride = self.AssembleOverrideContextForView3dOps()
        bpy.ops.machin3.slice_decal(oContextOverride,'INVOKE_REGION_WIN')
        original.select_set(state=True)
        bpy.context.view_layer.objects.active = original
        bpy.ops.object.join()
        #bpy.ops.machin3.slice_decal('INVOKE_REGION_WIN')