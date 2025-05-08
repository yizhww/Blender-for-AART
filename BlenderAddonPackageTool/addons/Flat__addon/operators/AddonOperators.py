import bpy

from ..config import __addon_name__
from ..preference.AddonPreferences import ExampleAddonPreferences


# This Example Operator will scale up the selected object
class ClearParentKeepTransform(bpy.types.Operator):
    """Clear parent of selected objects and keep their transforms"""
    bl_idname = "object.clear_parent_keep_transform"
    bl_label = "Clear Parent Keep Transform"

    # 确保在操作之前备份数据，用户撤销操作时可以恢复
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return context.active_object is not None

    def execute(self, context):
        for obj in context.selected_objects:
            if obj.parent:
                # Store the world matrix
                matrix_world = obj.matrix_world.copy()
                # Clear the parent
                obj.parent = None
                # Set the world matrix back
                obj.matrix_world = matrix_world
        return {'FINISHED'}


class CreateSpecificLayers(bpy.types.Operator):
    """Create specific layers with one click and set colors, and unify sub - layer colors, avoid duplicate creation"""
    bl_idname = "object.create_specific_layers"
    bl_label = "Create Specific Layers"
    bl_options = {'REGISTER', 'UNDO'}

    # 定义图层名称和对应的颜色，将 layer_info 移到操作符类内部
    layer_info = [
        ("SU源文件", 'COLOR_04'),  # 棕色
        ("ART艺术品", 'COLOR_01'),  # 红色
        ("Cam摄像机", 'COLOR_03'),  # 蓝色
        ("People人", 'COLOR_07'),  # 紫色
        ("Light灯光", 'COLOR_05'),  # 黄色
        ("Aset资产", 'COLOR_06'),  # 橙色
        ("Other", 'COLOR_08')  # 白色
    ]

    def execute(self, context):
        for name, color in self.layer_info:
            # 检查场景中是否已经存在同名集合
            existing_collection = bpy.data.collections.get(name)
            if existing_collection is None:
                new_collection = bpy.data.collections.new(name)
                # 设置集合的颜色
                new_collection.color_tag = color
                context.scene.collection.children.link(new_collection)
            else:
                new_collection = existing_collection
                # 如果集合已存在，也更新其颜色
                new_collection.color_tag = color

            # 统一子图层颜色
            self.unify_sub_layer_colors(new_collection)

        return {'FINISHED'}

    def unify_sub_layer_colors(self, parent_collection):
        for sub_collection in parent_collection.children:
            sub_collection.color_tag = parent_collection.color_tag
            # 递归处理子集合的子集合
            self.unify_sub_layer_colors(sub_collection)