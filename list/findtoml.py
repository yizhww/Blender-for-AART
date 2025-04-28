import toml
from pathlib import Path

# 定义扩展根目录（包含多个扩展子目录）
EXTENSIONS_DIR = Path("../addon_release")


def check_paths_and_toml():
    # 检查 EXTENSIONS_DIR 是否存在
    if not EXTENSIONS_DIR.exists():
        print(f"指定的目录 {EXTENSIONS_DIR} 不存在。")
        return

    print(f"目录 {EXTENSIONS_DIR} 存在。")

    # 列出 EXTENSIONS_DIR 下的所有子目录
    sub_dirs = list(EXTENSIONS_DIR.glob("*"))
    if not sub_dirs:
        print(f"目录 {EXTENSIONS_DIR} 为空，没有子目录。")
        return

    print(f"目录 {EXTENSIONS_DIR} 下有 {len(sub_dirs)} 个子目录。")

    for ext_dir in sub_dirs:
        print(f"正在检查目录: {ext_dir}")
        toml_file = ext_dir / "blender_manifest.toml"
        if not toml_file.exists():
            print(f"目录 {ext_dir} 中没有 blender_manifest.toml 文件，跳过。")
            continue

        print(f"在目录 {ext_dir} 中找到了 blender_manifest.toml 文件。")

        try:
            # 读取 TOML 元数据
            toml.load(toml_file)
            print(f"成功读取 {toml_file} 文件。")
        except Exception as e:
            print(f"加载 {toml_file} 文件时出现异常：{e}")


if __name__ == "__main__":
    check_paths_and_toml()