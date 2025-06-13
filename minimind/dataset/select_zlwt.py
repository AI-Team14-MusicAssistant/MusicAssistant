# 该脚本筛选周林王陶
import json
import os

def filter_singer_content(input_file, output_file):
    """
    过滤JSONL文件，仅保留包含指定歌手名字的条目
    
    Args:
        input_file (str): 输入JSONL文件路径
        output_file (str): 输出JSONL文件路径
    """
    # 要查找的歌手列表
    target_singers = ["周杰伦", "林俊杰", "陶喆", "王力宏"]
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
                # 检查整个对话内容中是否包含目标歌手名字
                content_to_check = ""
                
                # 拼接所有对话内容
                if 'conversations' in data and isinstance(data['conversations'], list):
                    for msg in data['conversations']:
                        if isinstance(msg.get('content'), str):
                            content_to_check += msg['content'] + "\n"
                
                # 检查是否包含任一目标歌手
                if any(singer in content_to_check for singer in target_singers):
                    outfile.write(line)
                    kept_count += 1
                    
            except json.JSONDecodeError:
                print(f"警告: 跳过第 {total_count} 行，无效的JSON格式")
                continue
    
    print(f"处理完成！共处理 {total_count} 条数据，保留了 {kept_count} 条包含目标歌手的条目。")
    print(f"目标歌手: {', '.join(target_singers)}")
    print(f"结果已保存到: {output_path}")

if __name__ == '__main__':
    # 使用相对路径（假设文件与脚本同目录）
    input_file = 'music_data4_raw.jsonl'  # 确保文件名拼写正确
    output_file = 'music_data5.jsonl'
    
    # 或者使用绝对路径（更可靠）
    # input_file = r'E:\FR\Study\大二下\人工智能原理\Music_Assistant\minimind\identify_data.jsonl'
    # output_file = r'E:\FR\Study\大二下\人工智能原理\Music_Assistant\minimind\filtered_singers.jsonl'
    
    filter_singer_content(input_file, output_file)