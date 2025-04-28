import bpy

from ..config import __addon_name__
from ..preference.AddonPreferences import ExampleAddonPreferences


# This Example Operator will scale up the selected object
class MergeObjectsByMaterialOperator(bpy.types.Operator):
    '''按材质合并网格物体'''
    bl_idname = "object.merge_operator"
    bl_label = "merge_addon"

    # 确保在操作之前备份数据，用户撤销操作时可以恢复
    bl_options = {'REGISTER', 'UNDO'}
    @classmethod
    def poll(cls, context):
        # 这里可以添加自定义的上下文检查逻辑
        return context.mode == 'OBJECT'

    def execute(self, context):
        def get_material_key(obj):
            """
            对于一个网格物体，返回一个按字母排序后的材质名称元组，
            如果物体没有材质则返回 None。
            """
            if obj.type != 'MESH':
                return None
            # 获取物体材质列表（忽略 None）
            mats = [mat.name for mat in obj.data.materials if mat is not None]
            if not mats:
                return None
            # 排序后转换为元组，作为分组的 key
            return tuple(sorted(mats))

        # 用来按材质 key 分组物体的字典
        groups = {}

        # 遍历当前场景中所有物体，筛选网格物体并按材质分组
        for obj in context.scene.objects:
            if obj.type == 'MESH':
                key = get_material_key(obj)
                if key is not None:
                    groups.setdefault(key, []).append(obj)

        # 对每个分组中物体数量大于 1 的组进行合并操作
        for key, objs in groups.items():
            if len(objs) > 1:
                # 先取消所有物体的选择，确保不会干扰 join 操作
                bpy.ops.object.select_all(action='DESELECT')

                # 使分组中的每个物体都处于可见状态（避免隐藏的物体无法被 join）
                for obj in objs:
                    obj.hide_set(False)

                # 设定组中第一个物体为 active 对象
                active_obj = objs[0]
                context.view_layer.objects.active = active_obj

                # 选中该组中所有物体
                for obj in objs:
                    obj.select_set(True)

                # 执行 join 操作（合并选中的物体）
                bpy.ops.object.join()

                self.report({'INFO'}, f"已合并 {len(objs)} 个物体，材质为: {key}")

        return {'FINISHED'}
