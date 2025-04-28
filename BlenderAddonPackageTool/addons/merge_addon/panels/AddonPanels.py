import bpy

from ..config import __addon_name__
from ..operators.AddonOperators import MergeObjectsByMaterialOperator
from ....common.i18n.i18n import i18n
from ....common.types.framework import reg_order


class BasePanel(object):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MergeAddon"

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return True


@reg_order(0)
class MergeAddonPanel(BasePanel, bpy.types.Panel):
    bl_label = "AART auto workflow"
    bl_idname = "SCENE_PT_sample"

    def draw(self, context: bpy.types.Context):
        addon_prefs = context.preferences.addons[__addon_name__].preferences

        layout = self.layout
        layout.operator(MergeObjectsByMaterialOperator.bl_idname)

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return True