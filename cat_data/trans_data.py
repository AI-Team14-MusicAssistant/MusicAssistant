import json
import os

# 获取当前文件所在目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))

# 读取源文件
with open(os.path.join(current_dir, 'cat.json'), 'r', encoding='utf-8') as f:
    cat_data = json.load(f)

# 转换格式
converted_data = []
for item in cat_data:
    converted_item = {
        "conversations": [
            {
                "role": "user",
                "content": item["instruction"]
            },
            {
                "role": "assistant",
                "content": item["output"]
            }
        ]
    }
    converted_data.append(converted_item)

# 写入新文件
with open('cat_converted.jsonl', 'w', encoding='utf-8') as f:
    for item in converted_data:
        json.dump(item, f, ensure_ascii=False)
        f.write('\n')

print("转换完成！输出文件: cat_converted.jsonl")