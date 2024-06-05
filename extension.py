import os

def change_file_extension(folder_path, old_ext, new_ext):
    # 遍历指定文件夹中的所有文件
    for filename in os.listdir(folder_path):
        # 检查文件的扩展名是否为指定的旧扩展名
        if filename.endswith(old_ext):
            # 构建新的文件名，保持前缀不变，只改变扩展名
            new_filename = os.path.splitext(filename)[0] + new_ext
            # 拼接完整的文件路径
            old_filepath = os.path.join(folder_path, filename)
            new_filepath = os.path.join(folder_path, new_filename)
            # 重命名文件
            os.rename(old_filepath, new_filepath)

# 示例用法
folder_path = "/Users/wangchao/Desktop/2021211950/code_database/Python"  # 替换为你的文件夹路径
old_extension = ".js"  # 旧扩展名
new_extension = ".py"  # 新扩展名

change_file_extension(folder_path, old_extension, new_extension)
