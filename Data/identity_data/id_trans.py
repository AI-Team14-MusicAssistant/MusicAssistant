import json
import os

def filter_assistant_content(input_file, output_file, keyword="张晟凡"):
    """
    过滤JSONL文件，仅保留assistant内容中包含指定关键字的条目
    
    Args:
        input_file (str): 输入JSONL文件路径
        output_file (str): 输出JSONL文件路径
        keyword (str): 要过滤的关键词，默认为"张晟凡"
    """
    kept_count = 0
    total_count = 0
    
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 构建完整文件路径
    input_path = os.path.join(script_dir, input_file)
    output_path = os.path.join(script_dir, output_file)
    
    with open(input_path, 'r', encoding='utf-8') as infile, \
         open(output_path, 'w', encoding='utf-8') as outfile:
        
        for line in infile:
            total_count += 1
            try:
                data = json.loads(line.strip())
                if 'conversations' in data and isinstance(data['conversations'], list):
                    assistant_contents = [
                        msg['content'] for msg in data['conversations'] 
                        if msg['role'] == 'assistant' and isinstance(msg.get('content'), str)
                    ]
                    if any(keyword in content for content in assistant_contents):
                        outfile.write(line)
                        kept_count += 1
            except json.JSONDecodeError:
                print(f"警告: 跳过第 {total_count} 行，无效的JSON格式")
                continue
    
    print(f"处理完成！共处理 {total_count} 条数据，保留了 {kept_count} 条包含'{keyword}'的条目。")
    print(f"结果已保存到: {output_path}")

if __name__ == '__main__':
    # 使用相对路径（假设文件与脚本同目录）
    input_file = 'identity_data.jsonl'  # 确保文件名拼写正确
    output_file = 'filtered_output.jsonl'
    
    # 或者使用绝对路径（更可靠）
    # input_file = r'E:\FR\Study\大二下\人工智能原理\Music_Assistant\minimind\identify_data.jsonl'
    # output_file = r'E:\FR\Study\大二下\人工智能原理\Music_Assistant\minimind\filtered_output.jsonl'
    
    filter_assistant_content(input_file, output_file)