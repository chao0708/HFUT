import zipfile
import os
import Encode
import Decode
import main
import os
import shutil
import rarfile
import zipfile
import py7zr
import tarfile


def get_name_and_type(path):
    filename = os.listdir(path)[1]
    name = os.path.splitext(filename)[0]
    type = os.path.splitext(filename)[1]
    return name, type


def extract_zip(folder_path):
    # 获取zip文件所在的文件夹路径
    zip_dir = os.path.dirname(folder_path)

    # 创建一个ZipFile对象
    with zipfile.ZipFile(folder_path, 'r') as zip_ref:
        # 解压zip文件到所在文件夹
        zip_ref.extractall(zip_dir)

    # 删除原zip文件
    os.remove(folder_path)


def rewrite_files_en(folder_path, target_extension):
    all_bits, all_hash_time, all_encode_time = 0, 0, 0

    # 遍历文件夹中的所有文件和子文件夹
    for root, dirs, files in os.walk(folder_path):
        for file in files:

            # 获取文件的完整路径
            file_path = os.path.join(root, file)

            # 检查文件后缀是否匹配目标后缀列表中的任何一个
            if any(file.endswith(ext) for ext in target_extension):
                with open(file_path, 'r', encoding='utf-8') as file:
                    msg = file.read()

                # 假设这里是你的 main.encode_msg 函数
                back_dict = main.encode_msg("SM3", msg)
                msg = back_dict["new_msg"]
                all_bits += back_dict["bits"]
                all_hash_time += back_dict["hash_time"]
                all_encode_time += back_dict["encode_time"]

                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(msg)

    # 将结果作为元组返回
    return all_bits, all_hash_time, all_encode_time


def rewrite_files_de(folder_path, target_extension, data1):
    all_bits, all_hash_time, all_encode_time, warm, all_judge = 0, 0, 0, "", True

    # 遍历文件夹中的所有文件和子文件夹
    for root, dirs, files in os.walk(folder_path):
        for file in files:

            # 获取文件的完整路径
            file_path = os.path.join(root, file)

            # 检查文件后缀是否匹配目标后缀列表中的任何一个
            if any(file.endswith(ext) for ext in target_extension):
                with open(file_path, 'r', encoding='utf-8') as file:
                    msg = file.read()

                # 假设这里是你的 main.encode_msg 函数
                back_dict = main.decode_msg(data1, msg)
                msg = back_dict["new_msg"]
                all_bits += back_dict["bits"]
                all_hash_time += back_dict["hash_time"]
                all_encode_time += back_dict["decode_time"]
                print(back_dict["result"])
                if back_dict["result"] == 0:
                    all_judge = False
                    warm += file_path + '\n'

                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(msg)

    # 将结果作为元组返回
    if all_bits == True:
        warm = "提取完成，验证成功！"
    else:
        warm = "验证失败！错误文件路径如下：" + "\n" + warm

    return all_bits, all_hash_time, all_encode_time, warm, all_judge


def compress_folder(folder_path, target_name, target_extension):
    # 创建压缩文件

    if target_extension == '.zip':
        with zipfile.ZipFile(target_name + '.zip', 'w') as archive:
            for folder_name, sub_folders, file_names in os.walk(folder_path):
                for file_name in file_names:
                    file_path = os.path.join(folder_name, file_name)
                    archive.write(file_path, os.path.relpath(file_path, folder_path))
    elif target_extension == '.7z':
        with py7zr.SevenZipFile(target_name + '.7z', 'w') as archive:
            archive.writeall(folder_path, os.path.basename(folder_path))
    elif target_extension == '.tar':
        with tarfile.open(target_name + '.tar', 'w') as archive:
            archive.add(folder_path, arcname=os.path.basename(folder_path))


if __name__ == '__main__':
    original_path = "/Users/wangchao/Desktop/2021211950/upload/"
    name, type = get_name_and_type(original_path)
    print(name, type)

    extract_zip(original_path + name + type)
    file_extensions = [".txt", ".c", ".cpp", ".go", ".java", ".js", ".php", ".py"]

    all_bits, all_hash_time, all_encode_time, warm, all_judge = rewrite_files_de(original_path + name, file_extensions,
                                                                                 "SM3")
    print(all_bits, all_judge, all_hash_time, all_encode_time, warm)
    folder_to_compress = original_path + "123"
    target_name = '123'
    target_extension = '.zip'  # Change to 'zip', 'rar', '7z', or 'tar' as needed
    compress_folder(folder_to_compress, target_name, target_extension)
