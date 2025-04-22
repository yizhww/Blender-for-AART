import bpy

# 定义插件的元信息，用于在 Blender 的插件管理界面中显示相关信息
bl_info = {
    "name": "Basic Add-on Sample",  # 插件名称
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
class ExampleOperator(bpy.types.Operator):
    '''ExampleAddon'''
    bl_idname = "object.example_ops"  # 操作符的唯一标识符，用于在其他地方引用该操作符
    bl_label = "ExampleOperator"  # 操作符在界面中显示的名称

    # 确保在操作之前备份数据，用户撤销操作时可以恢复
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context: bpy.types.Context):
        # 检查操作符是否可以执行，条件是当前有激活的对象
        return context.active_object is not None

    def execute(self, context: bpy.types.Context):
        # 操作符的执行逻辑，将激活对象的缩放比例乘以 2
        context.active_object.scale *= 2
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
    bl_label = "Example Addon Side Bar Panel"  # 面板在界面中显示的名称
    bl_idname = "SCENE_PT_sample"  # 面板的唯一标识符

    def draw(self, context: bpy.types.Context):
        layout = self.layout
        layout.operator(ExampleOperator.bl_idname)
        layout.label(text = "hello world")

    @classmethod  # 添加这个装饰器
    def poll(cls, context: bpy.types.Context):
        return True


def register():
    # 注册操作符类，使其在 Blender 中可用
    bpy.utils.register_class(ExampleOperator)
    # 注册面板类，使其在 Blender 中可用
    bpy.utils.register_class(ExampleAddonPanel)


def unregister():
    # 注销操作符类，使其在 Blender 中不可用
    bpy.utils.unregister_class(ExampleOperator)
    # 注销面板类，使其在 Blender 中不可用
    bpy.utils.unregister_class(ExampleAddonPanel)