import os
import time


def find_file(directory):
    # 获取指定目录下的所有文件和子目录
    files = os.listdir(directory)

    # 如果只有一个文件，则返回文件名
    if len(files) == 1 and os.path.isfile(os.path.join(directory, files[0])):
        return os.path.join(directory, files[0])
    else:
        return "目录中不止一个文件或者没有文件"


# 指定目录 存放用户上传文件的目录
def file_to_message(directory):
    # 查找文件
    file_name = find_file(directory)

    with open(file_name, 'r', encoding='utf-8') as file:
        content = file.read()
        return content


if __name__ == '__main__':
    begin = time.time()
    a = file_to_message("Demo")
    end = time.time()
    print((end - begin) * 1000)

# 测试用哪段代码速度更快 对于长文件和不同的文件类型
"""
def file_to_message(directory):
    # 使用 os.scandir() 获取目录中的条目，提升性能
    with os.scandir(directory) as entries:
        for entry in entries:
            if entry.is_file():
                # 读取第一个找到的文件的内容并返回
                with open(entry.path, 'r', encoding='utf-8') as file:
                    return file.read()

    # 如果没有找到文件，则返回一条消息
    return "目录中没有文件"
"""