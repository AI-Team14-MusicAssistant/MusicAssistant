import json

# 此文件用于将开源数据集 KdConv 中的知识三元组转换为可以进行 LORA 微调的数据格式。

def convert_kdconv_knowledge_to_lora_fixed(input_path, output_path, min_attrvalue_len=20):
    """
    Converts knowledge triples from KdConv dataset to LORA fine-tuning format.
    User's question is formed from 'name' and 'attrname'.
    Assistant's answer is 'attrvalue'.
    This version fixes the bug where 'attrs' field was mistaken for 'knowledge'.

    Args:
        input_path (str): Path to the input KdConv JSON file (e.g., train.json).
        output_path (str): Path to the output JSONL file.
        min_attrvalue_len (int): Minimum length for attrvalue to be included.
    """
    processed_count = 0
    skipped_due_to_filter_or_format = 0 # Renamed for clarity
    dialogues_without_attrs = 0
    messages_without_attrs = 0
    flag = 0

    try:
        with open(input_path, 'r', encoding='utf-8') as infile, \
             open(output_path, 'w', encoding='utf-8') as outfile:
            
            original_data = json.load(infile) # This is a list of dialogues
            
            for dialogue_session in original_data:
                if 'messages' not in dialogue_session:
                    dialogues_without_attrs +=1
                    continue
                
                for message in dialogue_session['messages']:
                    # Corrected: Check for 'attrs' instead of 'knowledge'
                    if 'attrs' not in message or not isinstance(message['attrs'], list):
                        messages_without_attrs +=1
                        continue
                        
                    # Corrected: Iterate over message['attrs']
                    for triple in message['attrs']: 
                        if not isinstance(triple, dict):
                            skipped_due_to_filter_or_format +=1
                            continue

                        name = triple.get('name')
                        attrname = triple.get('attrname')
                        attrvalue = triple.get('attrvalue')
                        
                        # Ensure all necessary parts exist and attrvalue is a string
                        if not all([name, attrname, attrvalue]) or not isinstance(attrvalue, str):
                            skipped_due_to_filter_or_format +=1
                            continue
                        
                        # Filter by length of attrvalue and check for placeholders
                        if len(attrvalue) >= min_attrvalue_len and "UNK" not in str(name) and "UNK" not in str(attrname):
                            # Formulate a more natural question
                            if attrname == "Information":
                                flag = 1 # 标志是否是信息类
                                user_contents = [
                                    f"请问{name}是？",
                                    f"请为我介绍{name}的相关信息。",
                                    f"你知道{name}吗？",
                                ]

                            else:
                                flag = 0
                                user_content = f"请问{name}的{attrname}是什么？"
                            # You can also try other phrasings, e.g.:
                            # user_content = f"告诉我关于{name}的{attrname}。"
                            # user_content = f"{name}的{attrname}具体指什么？"
                            
                            assistant_content = attrvalue

                            if flag == 0:    
                                conversation_entry = {
                                    "conversations": [
                                        {"role": "user", "content": user_content},
                                        {"role": "assistant", "content": assistant_content}
                                    ]
                                }
                                outfile.write(json.dumps(conversation_entry, ensure_ascii=False) + '\n')
                                processed_count += 1
                            else:
                                for i in range(0, 3):
                                    user_content = user_contents[i]
                                    conversation_entry = {
                                        "conversations": [
                                            {"role": "user", "content": user_content},
                                            {"role": "assistant", "content": assistant_content}
                                        ]
                                    }
                                    outfile.write(json.dumps(conversation_entry, ensure_ascii=False) + '\n')
                                    processed_count += 1

                        else:
                            skipped_due_to_filter_or_format +=1
                            
        print(f"处理完成！")
        print(f"从知识三元组中提取并转换了 {processed_count} 条对话。")
        print(f"因不满足长度条件、包含UNK或格式不完整而跳过了 {skipped_due_to_filter_or_format} 条三元组。")
        # print(f"跳过了 {dialogues_without_attrs} 个没有 'messages' 字段的对话。") # Might be too verbose
        # print(f"处理了消息但跳过了 {messages_without_attrs} 条没有 'attrs' 字段的消息。") # Might be too verbose
        print(f"输出文件已保存到: {output_path}")

    except FileNotFoundError:
        print(f"错误: 输入文件未找到于路径 {input_path}")
    except json.JSONDecodeError:
        print(f"错误: 输入文件 {input_path} 不是有效的 JSON 格式。")
    except Exception as e:
        print(f"发生未知错误: {e}")

if __name__ == '__main__':
    # 原始 KdConv 音乐数据集路径
    input_file_path = r'e:\FR\学业\大二下\人工智能原理\期末大作业\KdConv-master\data\music\train.json'
    
    # 新的输出文件路径，与您上次运行的输出路径一致
    output_file_path = r'e:\FR\学业\大二下\人工智能原理\期末大作业\minimind\dataset\music_data2.jsonl'
    
    # 您可以调整 attrvalue 的最小长度阈值
    min_length_attrvalue = 20 
    
    convert_kdconv_knowledge_to_lora_fixed(input_file_path, output_file_path, min_attrvalue_len=min_length_attrvalue)