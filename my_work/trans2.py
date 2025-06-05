import json

def convert_dataset_format(input_path, output_path):
    """
    Converts the KdConv music dataset to the LORA fine-tuning format.

    Args:
        input_path (str): Path to the input JSON file (e.g., train.json).
        output_path (str): Path to the output JSONL file.
    """
    try:
        with open(input_path, 'r', encoding='utf-8') as infile, \
             open(output_path, 'w', encoding='utf-8') as outfile:
            
            original_data = json.load(infile) # This is a list of dialogues
            
            for dialogue_session in original_data:
                if "messages" not in dialogue_session:
                    print(f"Skipping entry without 'messages' key: {dialogue_session}")
                    continue

                original_messages = dialogue_session["messages"]
                formatted_conversations = []
                
                for i, msg_data in enumerate(original_messages):
                    if "message" not in msg_data:
                        print(f"Skipping message without 'message' key in session: {dialogue_session.get('name', 'Unknown')}")
                        continue

                    role = "user" if i % 2 == 0 else "assistant"
                    content = msg_data["message"]
                    
                    formatted_conversations.append({
                        "role": role,
                        "content": content
                    })
                
                if formatted_conversations: # Only write if there are valid conversations
                    output_entry = {"conversations": formatted_conversations}
                    # Write each JSON object as a new line, ensure_ascii=False for Chinese characters
                    outfile.write(json.dumps(output_entry, ensure_ascii=False) + '\n')
            
        print(f"转换完成！输出文件已保存到: {output_path}")

    except FileNotFoundError:
        print(f"错误: 输入文件未找到于路径 {input_path}")
    except json.JSONDecodeError:
        print(f"错误: 输入文件 {input_path} 不是有效的 JSON 格式。")
    except Exception as e:
        print(f"发生未知错误: {e}")

if __name__ == '__main__':
    # 请根据您的文件实际存放位置修改这里的路径
    input_file_path = r'e:\FR\学业\大二下\人工智能原理\期末大作业\KdConv-master\data\music\train.json'
    # 建议将输出文件存放在您的 LORA 微调项目的数据集目录下
    output_file_path = r'e:\FR\学业\大二下\人工智能原理\期末大作业\minimind\dataset\music_train_for_lora.jsonl'
    
    convert_dataset_format(input_file_path, output_file_path)