import json
import random
import os

def shuffle_jsonl(input_file, output_file):
    # 读取所有行
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 解析每一行的 JSON 数据并存储到列表中
    data = []
    for line in lines:
        try:
            json_obj = json.loads(line.strip())
            data.append(json_obj)
        except json.JSONDecodeError as e:
            print(f"警告：跳过无效的 JSON 行: {e}")
            continue
    
    # 随机打乱数据
    random.shuffle(data)
    
    # 将打乱后的数据写入新文件
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in data:
            json_str = json.dumps(item, ensure_ascii=False)
            f.write(json_str + '\n')
    
    print(f"已成功处理 {len(data)} 条数据")
    print(f"输入文件：{input_file}")
    print(f"输出文件：{output_file}")

if __name__ == "__main__":
    # 获取脚本所在目录的绝对路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 设置输入输出文件的完整路径
    input_file = os.path.join(current_dir, "music_data3.jsonl")
    output_file = os.path.join(current_dir, "music_data3_shuffled.jsonl")
    
    # 可以设置随机种子以确保结果可复现（可选）
    # random.seed(42)
    
    # 执行打乱操作
    shuffle_jsonl(input_file, output_file)