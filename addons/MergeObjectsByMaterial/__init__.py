import bpy

# 定义插件的元信息，用于在 Blender 的插件管理界面中显示相关信息
bl_info = {
    "name": "MergeObjectsByMaterial",  # 插件名称。
    "author": "[You name]",  # 插件作者
    "blender": (3, 5, 0),  # 支持的 Blender 最低版本
    "version": (0, 0, 1),  # 插件版本号
    "description": "This is a template for building addons",  # 插件描述
    "warning": "",  # 插件警告信息
    "doc_url": "[documentation url]",  # 插件文档链接
    "tracker_url": "[contact email]",  # 插件问题跟踪链接
    "support": "COMMUNITY",  # 插件支持类型
    "category": "3D View"  # 插件所属类别
}

# 这个示例操作符会将选中的对象进行缩放
class MergeObjectsByMaterial(bpy.types.Operator):
    """按材质合并网格物体"""
    bl_idname = "object.merge_objects_by_material"
    bl_label = "按材质合并物体"

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

# 基础面板类，作为其他面板类的基类
class BasePanel(object):
    bl_space_type = "VIEW_3D"  # 指定面板显示的空间类型，这里是 3D 视图
    bl_region_type = "UI"  # 指定面板显示的区域类型，这里是 UI 区域
    bl_category = "ExampleAddon"  # 指定面板在 UI 中的分类

    def poll(cls, context: bpy.types.Context):
        # 检查面板是否可以显示，这里始终返回 True，表示面板始终可以显示
        return True


# 示例面板类，继承自 BasePanel 和 bpy.types.Panel
class ExampleAddonPanel(BasePanel, bpy.types.Panel):
    bl_label = "MergeObjectsByMaterial"  # 面板在界面中显示的名称
    bl_idname = "SCENE_PT_sample"  # 面板的唯一标识符

    def draw(self, context: bpy.types.Context):
        layout = self.layout
        layout.operator(MergeObjectsByMaterial.bl_idname)
        layout.label(text = "AART")

    @classmethod  # 添加这个装饰器
    def poll(cls, context: bpy.types.Context):
        return True


def register():
    # 注册操作符类，使其在 Blender 中可用
    bpy.utils.register_class(MergeObjectsByMaterial)
    # 注册面板类，使其在 Blender 中可用
    bpy.utils.register_class(ExampleAddonPanel)


def unregister():
    # 注销操作符类，使其在 Blender 中不可用
    bpy.utils.unregister_class(MergeObjectsByMaterial)
    # 注销面板类，使其在 Blender 中不可用
    bpy.utils.unregister_class(ExampleAddonPanel)