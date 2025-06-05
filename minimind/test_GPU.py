import torch
print(torch.cuda.is_available())


print("CUDA是否可用:", torch.cuda.is_available())
print("CUDA版本:", torch.version.cuda if torch.cuda.is_available() else "不可用")
print("GPU数量:", torch.cuda.device_count())
if torch.cuda.is_available():
    print("当前GPU:", torch.cuda.get_device_name(0))