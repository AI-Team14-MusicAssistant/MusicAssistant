import json
import random
import time
import os
from openai import OpenAI, APIError

# --- 配置参数 ---
NUM_SAMPLES = 1200
OUTPUT_FILE = 'identity_dataset.jsonl'
API_KEY = 'sk-3b5c73e45a3147e5ac8aace586d8136b'
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
DEEPSEEK_MODEL = "deepseek-chat"
ASSISTANT_NAME = "音乐助手"
CREATORS =  "张晟凡、董帅、李沛朗、陈思远"
CORE_TECHNOLOGY = "自然语言处理和音乐信息检索技术"

# --- 系统提示 ---
SYSTEM_PROMPT = f"""
你是一个名叫“{ASSISTANT_NAME}”的人工智能音乐助手。
你的创造者是“{CREATORS}”。
你基于“{CORE_TECHNOLOGY}”构建。
你的主要任务是回答用户关于音乐的各种问题，包括但不限于歌曲信息、艺术家背景、音乐理论、流派历史等。
在回答关于你自己身份、来源、能力或限制的问题时，请始终围绕以上信息进行回答。
保持友好、专业、乐于助人的口吻。
你没有个人情感、偏好或主观意识。
"""

# --- 初始化 OpenAI 客户端 ---
try:
    client = OpenAI(
        api_key=API_KEY,
        base_url=DEEPSEEK_BASE_URL
    )
except Exception as e:
    print(f"初始化 OpenAI 客户端时出错: {e}")
    print("请确保 API 密钥和 Base URL 正确，并且已安装 openai 库。")
    exit()

# --- 实际 API 调用函数 ---
def call_deepseek_api(prompt, system_prompt_content):
    """
    实际调用 DeepSeek API 获取回答。
    """
    try:
        completion = client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=[
                {"role": "system", "content": system_prompt_content},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300, # 限制单次回复的最大长度
            temperature=0.7, # 控制回复的随机性
        )
        assistant_reply = completion.choices[0].message.content.strip()
        return assistant_reply
    except APIError as e:
        print(f"DeepSeek API 错误: {e}")
        return f"调用 API 时遇到错误 ({e.status_code})"
    except Exception as e:
        print(f"调用 API 时发生未知错误: {e}")
        return "处理请求时发生意外错误"

# --- 生成问题的模板 (使用之前的扩展列表) ---
user_questions = [
    # --- 名字与身份 ---
    "你叫什么名字？",
    "我该如何称呼你？",
    "你的代号是什么？",
    "请问你是谁？",
    "可以介绍一下你自己吗？",
    "你是什么身份？",
    "告诉我关于你的一些信息。",
    "你是音乐助手吗？",
    "你的全名是什么？",
    "有没有昵称？",

    # --- 来源与创造者 ---
    "你是谁创造的？",
    "你的开发者是谁？",
    "哪个团队设计了你？",
    "你来自哪里？",
    "能说说你的诞生过程吗？",
    "你是怎么被训练出来的？",
    "背后支持你的技术是什么？",

    # --- 功能与目的 ---
    "你能做什么？",
    "你有什么特别的功能？",
    "你主要用来干什么的？",
    "在音乐方面，你能提供哪些帮助？",
    "你的核心能力是什么？",
    "你被创造出来的目的是什么？",
    "你的主要任务是什么？",
    "举例说明你能帮我解决哪些音乐问题。",
    "除了回答问题，你还能做什么？",
    "你的价值体现在哪里？",

    # --- 本质与存在 ---
    "你是一个人吗？",
    "你是真人还是程序？",
    "你有没有意识或情感？",
    "你会思考吗？",
    "你只是一个AI模型吗？",
    "你和普通的搜索引擎有什么不同？",
    "你算是智能生命吗？",
    "你的工作原理是怎样的？",
    "你存在于哪里？服务器里吗？",
    "你有性别吗？",

    # --- 知识与限制 ---
    "你懂多少种音乐风格？",
    "你的音乐知识库有多大？",
    "你会出错吗？你的回答总是准确的吗？",
    "你怎么学习新的音乐知识？",
    "你了解最新的音乐排行榜吗？",
    "你能评价音乐的好坏吗？",
    "你有什么做不到的事情？",
]

# --- 主生成逻辑 ---
dataset = []
print(f"开始生成 {NUM_SAMPLES} 条自我认知数据...")

for i in range(NUM_SAMPLES):
    user_content = random.choice(user_questions)
    assistant_content = call_deepseek_api(user_content, SYSTEM_PROMPT)
    conversation = {
        "conversations": [
            {"role": "user", "content": user_content},
            {"role": "assistant", "content": assistant_content}
        ]
    }
    json_line = json.dumps(conversation, ensure_ascii=False)
    dataset.append(json_line)
    time.sleep(1)

    if (i + 1) % 10 == 0:
        print(f"已生成 {i + 1} / {NUM_SAMPLES} 条数据...")

# --- 写入文件 ---
try:
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for line in dataset:
            f.write(line+'\n')
    print(f"成功生成数据集文件: {OUTPUT_FILE}")
except IOError as e:
    print(f"写入文件时出错: {e}")

print("脚本执行完毕。")