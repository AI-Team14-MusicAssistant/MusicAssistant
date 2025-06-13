import json

def convert_kdconv_knowledge_to_lora_fixed(input_path, output_path, min_attrvalue_len=20):
    """
    Converts knowledge triples from KdConv dataset to LORA fine-tuning format.
    Only processes triples where attrname is "Information".
    Adds book title marks to name when attrvalue starts with them.

    Args:
        input_path (str): Path to the input KdConv JSON file (e.g., train.json).
        output_path (str): Path to the output JSONL file.
        min_attrvalue_len (int): Minimum length for attrvalue to be included.
    """
    processed_count = 0
    skipped_due_to_filter_or_format = 0
    dialogues_without_attrs = 0
    messages_without_attrs = 0

    try:
        with open(input_path, 'r', encoding='utf-8') as infile, \
             open(output_path, 'w', encoding='utf-8') as outfile:
            
            original_data = json.load(infile)
            
            for dialogue_session in original_data:
                if 'messages' not in dialogue_session:
                    dialogues_without_attrs += 1
                    continue
                
                for message in dialogue_session['messages']:
                    if 'attrs' not in message or not isinstance(message['attrs'], list):
                        messages_without_attrs += 1
                        continue
                        
                    for triple in message['attrs']: 
                        if not isinstance(triple, dict):
                            skipped_due_to_filter_or_format += 1
                            continue

                        attrname = triple.get('attrname')
                        # Only process if attrname is "Information"
                        if attrname != "Information":
                            skipped_due_to_filter_or_format += 1
                            continue
                            
                        name = triple.get('name')
                        attrvalue = triple.get('attrvalue')
                        
                        if not all([name, attrvalue]) or not isinstance(attrvalue, str):
                            skipped_due_to_filter_or_format += 1
                            continue
                        
                        # Check if attrvalue starts with name in book title marks
                        book_title_mark = f"《{name}》"
                        if attrvalue.startswith(book_title_mark):
                            display_name = book_title_mark
                        else:
                            display_name = name
                        
                        # Filter by length of attrvalue and check for placeholders
                        if len(attrvalue) >= min_attrvalue_len and "UNK" not in str(name):
                            # Generate three different question formulations
                            user_contents = [
                                f"请问{display_name}是？",
                                f"请为我介绍{display_name}的相关信息。",
                                f"你知道{display_name}吗？",
                                f"介绍{display_name}",
                                f"{display_name}"
                            ]
                            
                            assistant_content = attrvalue

                            for user_content in user_contents:
                                conversation_entry = {
                                    "conversations": [
                                        {"role": "user", "content": user_content},
                                        {"role": "assistant", "content": assistant_content}
                                    ]
                                }
                                outfile.write(json.dumps(conversation_entry, ensure_ascii=False) + '\n')
                                processed_count += 1
                        else:
                            skipped_due_to_filter_or_format += 1
                            
        print(f"处理完成！")
        print(f"从知识三元组中提取并转换了 {processed_count} 条对话。")
        print(f"因不满足长度条件、包含UNK或格式不完整而跳过了 {skipped_due_to_filter_or_format} 条三元组。")
        print(f"输出文件已保存到: {output_path}")

    except FileNotFoundError:
        print(f"错误: 输入文件未找到于路径 {input_path}")
    except json.JSONDecodeError:
        print(f"错误: 输入文件 {input_path} 不是有效的 JSON 格式。")
    except Exception as e:
        print(f"发生未知错误: {e}")

if __name__ == '__main__':
    # 原始 KdConv 音乐数据集路径
    input_file_path = r'e:\FR\Study\大二下\人工智能原理\Music_Assistant\Data\KdConv-data\data\music\train.json'
    
    # 新的输出文件路径
    output_file_path = r'e:\FR\Study\大二下\人工智能原理\Music_Assistant\Data\KdConv-data\data\music\music_data4.jsonl'
    
    # 您可以调整 attrvalue 的最小长度阈值
    min_length_attrvalue = 20 
    
    convert_kdconv_knowledge_to_lora_fixed(input_file_path, output_file_path, min_attrvalue_len=min_length_attrvalue)