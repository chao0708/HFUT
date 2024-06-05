# -*- coding: utf-8 -*-
import flask
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import Encode
import hashlib
import Decode
import time
import new_SM3
from flask import Flask, render_template, request
import torch
import os
import shutil
import zipfile
import py7zr
import tarfile
import Whitemark

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

whitespaces = [0x00A0, 0x2000, 0x2001, 0x2002, 0x2003, 0x2004, 0x2005, 0x2006,
               0x2007, 0x2008, 0x2009, 0x200A, 0x202F, 0x205F, 0x200B, 0x2060]

type_hash = {"MD5": 32, "SHA1": 40, "SHA256": 64, "SHA512": 128, "SM3": 64}

original_path = "/Users/wangchao/Desktop/2021211950/upload/"

file_extensions = [".txt", ".c", ".cpp", ".go", ".java", ".js", ".php", ".py"]

# 指定本地模型文件夹路径
model_folder_path = "/Users/wangchao/Desktop/2021211950/text-classification"

# 加载本地tokenizer
loaded_tokenizer = AutoTokenizer.from_pretrained(model_folder_path)

# 加载本地模型
loaded_model = AutoModelForSequenceClassification.from_pretrained(model_folder_path)


def encode_msg(data1, msg):
    # 初始化计时器
    begin = time.time()

    # 计算哈希值
    if data1 == "MD5":
        Hash = hashlib.md5(msg.encode()).hexdigest().lower()
    elif data1 == "SM3":
        Hash = new_SM3.sm3_hash(msg)
    elif data1 == "SHA1":
        Hash = hashlib.sha1(msg.encode()).hexdigest()
    elif data1 == "SHA256":
        Hash = hashlib.sha256(msg.encode()).hexdigest()
    else:
        Hash = hashlib.sha512(msg.encode()).hexdigest()

    # 计算哈希时间
    hash_time = (time.time() - begin) * 1000
    print(new_SM3.sm3_hash(msg))
    # 分割消息
    msg_lst = msg.split('\n')

    inputs = loaded_tokenizer(msg, return_tensors="pt", truncation=True)

    with torch.no_grad():
        logits = loaded_model(**inputs).logits
    predicted_class_id = logits.argmax().item()
    code_type = loaded_model.config.id2label[predicted_class_id]
    print(loaded_model.config.id2label[predicted_class_id])

    # 编码消息
    begin = time.time()

    if code_type == "Python":
        new_msg_lst, bits = Encode.python_en(msg_lst, Hash)
    elif code_type == "C":
        new_msg_lst, bits = Encode.c_en(msg_lst, Hash)
    elif code_type == "C++":
        new_msg_lst, bits = Encode.cpp_en(msg_lst, Hash)
    elif code_type == "Java":
        new_msg_lst, bits = Encode.java_en(msg_lst, Hash)
    elif code_type == "JavaScript":
        new_msg_lst, bits = Encode.javascript_en(msg_lst, Hash)
    elif code_type == "PHP":
        new_msg_lst, bits = Encode.php_en(msg_lst, Hash)
    elif code_type == "Go":
        new_msg_lst, bits = Encode.go_en(msg_lst, Hash)
    elif code_type == "Html":
        new_msg_lst, bits = Encode.html_en(msg_lst, Hash)

    encode_time = (time.time() - begin) * 1000

    # 重构新消息
    new_msg = "\n".join(new_msg_lst)

    return {
        "bits": bits * 4,
        "hash_time": round(hash_time, 2),
        "encode_time": round(encode_time, 2),
        "new_msg": new_msg
    }


def decode_msg(data1, msg):
    length = type_hash[data1]
    msg_lst = msg.split('\n')

    # 解码消息
    begin = time.time()
    new_msg_lst, decode_message = Decode.decode(msg_lst, length)
    decode_time = (time.time() - begin) * 1000

    # 重构新消息
    new_msg = "\n".join(new_msg_lst)

    # 计算哈希值
    begin = time.time()
    if data1 == "MD5":
        Hash = hashlib.md5(new_msg.encode()).hexdigest().lower()
    elif data1 == "SM3":
        Hash = new_SM3.sm3_hash(new_msg)
    elif data1 == "SHA1":
        Hash = hashlib.sha1(new_msg.encode()).hexdigest()
    elif data1 == "SHA256":
        Hash = hashlib.sha256(new_msg.encode()).hexdigest()
    else:
        Hash = hashlib.sha512(new_msg.encode()).hexdigest()
    hash_time = (time.time() - begin) * 1000

    # 计算比特数
    bits = len(decode_message) * 4

    # 检查解码结果与哈希值是否匹配
    print(decode_message)
    print(Hash[:len(decode_message):])
    result = 1 if decode_message == Hash[:len(decode_message):] and len(decode_message) != 0 else 0

    return {
        "decode_time": round(decode_time, 2),
        "bits": bits,
        "hash_time": round(hash_time, 2),
        "new_msg": new_msg,
        "result": result
    }


def get_name_and_type(path):
    lst = path.split('.')
    return lst[0], "." + lst[1]


# def extract_zip(folder_path):
#     # 获取zip文件所在的文件夹路径
#     zip_dir = os.path.dirname(folder_path)
#
#     # 创建一个ZipFile对象
#     with zipfile.ZipFile(folder_path, 'r') as zip_ref:
#         # 解压zip文件到所在文件夹
#         zip_ref.extractall(zip_dir)
#
#     # 删除原zip文件
#     os.remove(folder_path)

def extract_archive(archive_path):
    # 获取压缩文件所在的文件夹路径
    archive_dir = os.path.dirname(archive_path)

    # 解压缩文件
    shutil.unpack_archive(archive_path, archive_dir)

    # 删除原压缩文件
    os.remove(archive_path)


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

    shutil.rmtree(folder_path)


def rewrite_files_en(folder_path, target_extension, data1):
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
                back_dict = encode_msg(data1, msg)
                msg = back_dict["new_msg"]
                all_bits += back_dict["bits"]
                all_hash_time += back_dict["hash_time"]
                all_encode_time += back_dict["encode_time"]

                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(msg)

    # 将结果作为元组返回
    return all_bits, all_hash_time, all_encode_time


def rewrite_files_de(folder_path, target_extension, data1):
    all_bits, all_hash_time, all_encode_time, warm, all_judge = 0, 0, 0, "", 1
    # 遍历文件夹中的所有文件和子文件夹
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # 获取文件的完整路径
            file_path = os.path.join(root, file)
            # 检查文件后缀是否匹配目标后缀列表中的任何一个
            if any(file.endswith(ext) for ext in target_extension):
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    msg = file.read()

                # 假设这里是你的 main.encode_msg 函数
                back_dict = decode_msg(data1, msg)
                msg = back_dict["new_msg"]
                all_bits += back_dict["bits"]
                all_hash_time += back_dict["hash_time"]
                all_encode_time += back_dict["decode_time"]
                print(back_dict["result"])
                if back_dict["result"] == 0:
                    all_judge = 0
                    warm += file_path + '\n'

                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(msg)

    # 将结果作为元组返回
    if all_judge == 1:
        warm = "提取完成，验证成功！"
    else:
        warm = "验证失败！错误文件路径如下：" + "\n" + warm

    return all_bits, all_hash_time, all_encode_time, warm, all_judge


def encode_pkg(data1, data3):
    name, type = get_name_and_type(data3)
    print(name)
    print(type)

    extract_archive(original_path + name + type)

    all_bits, all_hash_time, all_encode_time = rewrite_files_en(original_path + name, file_extensions, data1)

    folder_to_compress = original_path + name
    target_name = name
    target_extension = type

    compress_folder(folder_to_compress, target_name, target_extension)

    return {
        "bits": all_bits,
        "hash_time": all_hash_time,
        "encode_time": all_encode_time,
        "new_msg": "嵌入完成！请下载文件"
    }


def decode_pkg(data1, data3):
    name, type = get_name_and_type(data3)

    extract_archive(original_path + name + type)

    all_bits, all_hash_time, all_encode_time, warm, all_judge = rewrite_files_de(original_path, file_extensions,
                                                                                 data1)

    # folder_to_compress = original_path
    # print(folder_to_compress)
    # target_name = name
    # target_extension = type
    # print(type)

    compress_folder(original_path, name, type)
    os.mkdir(original_path)

    return {
        "bits": all_bits,
        "hash_time": all_hash_time,
        "decode_time": all_encode_time,
        "result": all_judge,
        "new_msg": warm
    }


@app.route("/embed", methods=["POST"])
def embed():
    data1 = request.form['Hash']
    data2 = request.form.get("msg")
    data3 = request.form.get("filename")

    if data3 is None:
        ans = encode_msg(data1, data2)
    elif data3.split('.')[1] in ["tar", "zip", "7z"]:
        ans = encode_pkg(data1, data3)
    else:
        ans = encode_msg(data1, data2)
    return {
        "bits": ans["bits"],
        "hash_time": round(ans["hash_time"], 2),
        "encode_time": round(ans["encode_time"], 2),
        "new_msg": ans["new_msg"]
    }


@app.route("/embed-text", methods=["POST"])
def embed_text():
    data = request.form.get("msg")
    msg = Whitemark.add_watermark(data)
    return {
        "new_msg": msg,
    }


@app.route("/extract", methods=["POST"])
def extract():
    data1 = request.form.get("Hash")
    data2 = request.form.get("msg")
    data3 = request.form.get("filename")

    if data3 is None:
        ans = decode_msg(data1, data2)
    elif data3.split('.')[1] in ["tar", "zip", "7z"]:
        ans = decode_pkg(data1, data3)
    else:
        ans = decode_msg(data1, data2)
    print(data1)
    return {
        "result": ans["result"],
        "bits": ans["bits"],
        "hash_time": round(ans["hash_time"], 2),
        "decode_time": round(ans["decode_time"], 2),
        "new_msg": ans["new_msg"]
    }


@app.route("/extract-text", methods=["POST"])
def extract_text():
    data = request.form.get("msg")
    result = Whitemark.detect_watermark(data)
    if result:
        judge = "文本包含水印！"
    else:
        judge = "文本不包含水印！"
    return {
        "result": judge,
    }


@app.route("/postFile", methods=["POST"])
def upload():
    data = request.files.get("file")
    filename = "upload/" + data.filename
    data.save(filename)
    if data.filename.split(".")[1] in ["tar", "zip", "7z"]:
        return {"content": "这是一个压缩包！"}
    else:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        return {"content": content}


@app.route("/download", methods=["POST"])
def download():
    data = request.form.get("filename")
    print(data)
    return flask.send_file(data)


@app.route("/index.html")
def index():
    return render_template("index.html")


@app.route("/text.html")
def text():
    return render_template("text.html")


@app.route("/hello")
def hello1():
    return render_template("hello.html")


@app.route("/hello.html")
def hello2():
    return render_template("hello.html")


@app.route("/")
def hello0():
    return render_template("hello.html")


if __name__ == '__main__':
    app.run("127.0.0.1", 12345)
