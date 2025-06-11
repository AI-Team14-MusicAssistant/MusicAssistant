import torch
# 检测当前电脑是否可用GPU

if torch.cuda.is_available():
        print("当前使用GPU训练") 
else:
        print("使用CPU训练")