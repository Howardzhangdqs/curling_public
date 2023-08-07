import ctypes
import os
import sys
os.add_dll_directory(os.path.join(os.path.dirname(__file__), "bin"))
print(os.path.join(os.path.dirname(__file__), "bin"))

sys.path.append(os.path.join(os.path.dirname(__file__), "bin"))
sys.path.append(os.path.join(os.path.dirname(__file__)))
print(sys.path)

import ctypes.util
name = ctypes.util.find_library('smooth.so')
print(name)

# 加载so文件
lib = ctypes.cdll.LoadLibrary(os.getcwd() + "\\bin\\smooth.so")

# 定义函数的参数和返回类型
lib.myfunc.argtypes = [POINTER(ctypes.c_int), ctypes.c_int]
lib.myfunc.restype = POINTER(ctypes.c_int)

# 创建一个整数数组
arr = (ctypes.c_int * 5)(1, 2, 3, 4, 5)

# 调用函数并获取返回值
res = lib.myfunc(arr, 5)

# 打印返回值
for i in range(5):
    print(res[i])
