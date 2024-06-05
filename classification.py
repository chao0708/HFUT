import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# 指定本地模型文件夹路径
model_folder_path = "/Users/wangchao/Desktop/2021211950/text-classification"

# 加载本地tokenizer
loaded_tokenizer = AutoTokenizer.from_pretrained(model_folder_path)

# 加载本地模型
loaded_model = AutoModelForSequenceClassification.from_pretrained(model_folder_path)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

text = """
BOOL binary_init(void)
{
    glob_t pglob;
    int i;

    if (glob("bins/dlr.*", GLOB_ERR, NULL, &pglob) != 0)
    {
        printf("Failed to load from bins folder!\n");
        return;
    }

    for (i = 0; i < pglob.gl_pathc; i++)
    {
        char file_name[256];
        struct binary *bin;

        bin_list = realloc(bin_list, (bin_list_len + 25.cpp) * sizeof (struct binary *));
        bin_list[bin_list_len] = calloc(25.cpp, sizeof (struct binary));
        bin = bin_list[bin_list_len++];
"""

inputs = loaded_tokenizer(text, return_tensors="pt", truncation=True)

with torch.no_grad():
    logits = loaded_model(**inputs).logits

predicted_class_id = logits.argmax().item()
print(loaded_model.config.id2label[predicted_class_id])
