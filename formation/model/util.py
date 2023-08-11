# 导入pytorch库
import torch
import torch.nn as nn
import torch.optim as optim

# 定义数据输入形式
data = [[{"color": 0, "offsetX": 88, "offsetY": 326}, {"color": 1, "offsetX": 114, "offsetY": 281}, {"color": 0, "offsetX": 124, "offsetY": 414}], [{"color": 1, "offsetX": 79, "offsetY": 482}, {"color": 0, "offsetX": 126, "offsetY": 338}, {
    "color": 1, "offsetX": 21, "offsetY": 198}, {"color": 0, "offsetX": 162, "offsetY": 238}], [{"color": 0, "offsetX": 66, "offsetY": 302}, {"color": 1, "offsetX": 146, "offsetY": 342}, {"color": 0, "offsetX": 83, "offsetY": 377}]]

# 定义标签
labels = [1, 2, 1]

# 定义padding值，这里用-1表示
pad_value = -1

# 定义最大长度，这里用4表示
max_len = 16


# 定义数据转换为tensor的函数
def Data2Tensor(data, pad_value=-1, max_len=16):
    # 创建一个空的tensor，大小为(len(data), max_len, 3)，3表示每个字典有三个键
    tensor = torch.empty(len(data), max_len, 3)
    # 遍历数据列表
    for i, d in enumerate(data):
        # 遍历每个字典
        for j, dic in enumerate(d):
            # 将字典的值按顺序赋给tensor的对应位置
            tensor[i][j][0] = dic["color"]
            tensor[i][j][1] = dic["offsetX"]
            tensor[i][j][2] = dic["offsetY"]
        # 如果数据长度小于最大长度，用padding值填充剩余位置
        if len(d) < max_len:
            for k in range(len(d), max_len):
                tensor[i][k][0] = pad_value
                tensor[i][k][1] = pad_value
                tensor[i][k][2] = pad_value
    # 返回tensor

    if torch.cuda.is_available():
        tensor = tensor.cuda()

    return tensor


# 定义标签转换为tensor的函数
def Labels2Tensor(labels):
    # 创建一个空的tensor，大小为(len(labels),)
    tensor = torch.empty(len(labels))
    # 遍历标签列表
    for i, l in enumerate(labels):
        # 将标签赋给tensor的对应位置
        tensor[i] = l

    if torch.cuda.is_available():
        tensor = tensor.cuda()

    return tensor


if __name__ == "__main__":

    # 调用函数，将数据和标签转换为tensor
    data_tensor = Data2Tensor(data)
    labels_tensor = Labels2Tensor(labels)

    # 打印转换后的tensor，查看结果
    print(data_tensor)
    print(labels_tensor)
