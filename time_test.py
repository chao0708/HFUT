import os
import time
import new_SM3
from gmssl import sm3

# 定义文件夹路径
folder_path = '/Users/wangchao/Desktop/2021211950/code_database/Python'

# 列出文件夹中的文件，并按名称排序
files = sorted(os.listdir(folder_path))

# 指定要读取的文件后缀
valid_extensions = ['.py']

# 初始化变量
total_time = 0
num_files_processed = 0

# 遍历每个文件，并读取内容
for file_name in files:
    # 获取文件扩展名
    _, extension = os.path.splitext(file_name)
    print(file_name)
    # 检查文件是否为有效的代码文件
    if extension in valid_extensions:
        # 构建完整文件路径
        file_path = os.path.join(folder_path, file_name)
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            num_files_processed += 1
            msg = file.read()
            begin = time.time()
            new_SM3.sm3_hash(msg)
            total_time += (time.time() - begin) * 1000

            # 每处理5个文件打印一次平均时间
            if num_files_processed % 5 == 0:
                print(f"Average time for last 5 files: {total_time / 5} milliseconds")
                total_time = 0

# 打印剩余文件的平均时间
if num_files_processed % 5 != 0:
    print(f"Average time for remaining files: {total_time / (num_files_processed % 5)} milliseconds")
