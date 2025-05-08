import bpy

from ..config import __addon_name__
from ..operators.AddonOperators import ClearParentKeepTransform
from ....common.i18n.i18n import i18n
from ....common.types.framework import reg_order

bpy.types.Scene.my_enum_property = bpy.props.EnumProperty(
    items=[
        ('OPTION1', "选项 1", "这是选项 1 的说明"),
        ('OPTION2', "选项 2", "这是选项 2 的说明"),
        ('OPTION3', "选项 3", "这是选项 3 的说明")
    ],
    name="选择一个选项"
)

# 定义一个布尔属性
bpy.types.Scene.show_extra_content = bpy.props.BoolProperty(name="显示额外内容", default=False)

# 定义一个枚举属性用于选择标签
bpy.types.Scene.selected_tab = bpy.props.EnumProperty(
    items=[
        ('TAB1', "标签 1", "标签 1 的说明"),
        ('TAB2', "标签 2", "标签 2 的说明")
    ],
    name="选择标签",
    default='TAB1'
)

# 定义一个浮点数属性
bpy.types.Scene.my_float_property = bpy.props.FloatProperty(name="Float Property", default=0.0)

class BasePanel(object):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "AARTAUTO"

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return True


@reg_order(0)
class AARTAddonPanel(BasePanel, bpy.types.Panel):
    bl_label = "AART"
    bl_idname = "test"

    def draw(self, context: bpy.types.Context):
        addon_prefs = context.preferences.addons[__addon_name__].preferences
        layout = self.layout

        # 基本UI元素
        # 按钮（Operator）
        layout.operator(ClearParentKeepTransform.bl_idname)
        layout.operator("object.create_specific_layers")
        # 标签（Label）
        layout.label(text="这是一个测试：draw 方法中可以使用的各种 UI 元素和布局方式")
        # 输入框（Property）
        scene = context.scene
        layout.prop(scene, "my_float_property", text="输入一个浮点数")
        # 下拉菜单（EnumProperty）
        scene = context.scene
        layout.prop(scene, "my_enum_property", text="选择一个选项")
        # 下拉菜单（EnumProperty）

        # 布局管理
        # 行布局（Row）
        row = layout.row()
        row.label(text="标签 1")
        row.label(text="标签 2")
        # 列布局（Column）
        col = layout.column()
        col.label(text="标签 3")
        col.label(text="标签 4")

        # 动态UI
        # 根据条件显示 UI 元素

        ''' 
        1. 嵌套布局结构
        通过嵌套行（row）、列（column）和盒子（box）等布局元素，
        可以创建出层次丰富的界面。这种方式可以将不同类型的 UI 元素进行分组，
        使界面更加清晰和有条理。
        '''
        # 外层盒子
        outer_box = layout.box()
        outer_box.label(text="外层盒子内容")

        # 在外层盒子中创建一行
        outer_row = outer_box.row()

        # 左侧列
        left_col = outer_row.column()
        left_col.label(text="左侧列内容")
        left_col.operator("object.select_all", text="全选物体").action = 'SELECT'

        # 右侧列
        right_col = outer_row.column()
        right_col.label(text="右侧列内容")
        right_col.operator("object.select_all", text="全选物体").action = 'SELECT'

        # 内层盒子
        inner_box = outer_box.box()
        inner_box.label(text="内层盒子内容")
        inner_box.operator("object.select_all", text="再次全选物体").action = 'SELECT'


        ''' 
        2. 使用循环生成 UI 元素
        如果需要创建多个相似的 UI 元素，例如一系列的按钮或输入框，
        可以使用循环来动态生成这些元素。这样可以减少代码的重复，
        并且方便根据数据动态调整 UI。
        '''
        # 创建一个循环
        num_buttons = 3
        # 创建一个列布局
        col = layout.column()
        for i in range(num_buttons):
            col.operator("object.select_all", text=f"按钮 {i + 1}").action = 'SELECT'


        ''' 
        3. 动态显示和隐藏 UI 元素
        根据不同的条件或用户操作，动态地显示或隐藏某些 UI 元素，
        可以实现更加灵活的界面交互。例如，
        根据某个属性的值来决定是否显示特定的输入框或按钮。
        '''
        # 显示一个布尔属性的 UI 控件
        layout.prop(scene, "show_extra_content", text="显示额外内容")

        if scene.show_extra_content:
            # 如果布尔属性为 True，则显示额外内容
            layout.label(text="这是额外内容")
            layout.operator("object.select_all", text="全选物体").action = 'SELECT'


        ''' 
        4. 分组和标签页
        可以使用 row 和 column 
        结合标签来创建分组和标签页的效果，
        让界面更加模块化，便于用户操作。
        '''
        # 创建标签行
        tab_row = layout.row()
        tab_row.prop_enum(scene, "selected_tab", 'TAB1', text="标签 1")
        tab_row.prop_enum(scene, "selected_tab", 'TAB2', text="标签 2")

        if scene.selected_tab == 'TAB1':
            # 标签 1 的内容
            layout.label(text="这是标签 1 的内容")
            layout.operator("object.select_all", text="全选物体").action = 'SELECT'
        elif scene.selected_tab == 'TAB2':
            # 标签 2 的内容
            layout.label(text="这是标签 2 的内容")
            layout.prop(scene, "my_float_property", text="输入一个浮点数")
