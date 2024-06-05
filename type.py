import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# 指定本地模型文件夹路径
model_folder_path = "/Users/wangchao/Desktop/2021211950/text-classification"

# 加载本地tokenizer
loaded_tokenizer = AutoTokenizer.from_pretrained(model_folder_path)

# 加载本地模型
loaded_model = AutoModelForSequenceClassification.from_pretrained(model_folder_path)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 定义文件夹路径
folder_path = '/Users/wangchao/Desktop/2021211950/code_database/Python'

# 列出文件夹中的文件，并按名称排序
files = sorted(os.listdir(folder_path))

# 指定要读取的文件后缀
valid_extensions = ['.py']

# 遍历每个文件，并读取内容
for file_name in files:
    # 获取文件扩展名
    _, extension = os.path.splitext(file_name)

    # 检查文件是否为有效的代码文件
    if extension in valid_extensions:
        # 构建完整文件路径
        file_path = os.path.join(folder_path, file_name)

        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            msg = file.read()
            inputs = loaded_tokenizer(msg, return_tensors="pt", truncation=True)

            with torch.no_grad():
                logits = loaded_model(**inputs).logits

            predicted_class_id = logits.argmax().item()
            print(loaded_model.config.id2label[predicted_class_id], end="  ")
