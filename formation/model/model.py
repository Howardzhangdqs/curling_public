import torch.nn as nn


# 定义卷积神经网络模型类
class net(nn.Module):

    def __init__(self):
        super(net, self).__init__()
        # 定义第一个卷积层，输入通道数为3（color, offsetX, offsetY），输出通道数为16，卷积核大小为3x3，步长为1，填充为1
        self.conv1 = nn.Conv2d(3, 16, 3, 1, 1)
        # 定义第一个池化层，使用最大池化，池化核大小为2x2，步长为2
        self.pool1 = nn.MaxPool2d(2, 1)
        # 定义第二个卷积层，输入通道数为16，输出通道数为32，卷积核大小为3x3，步长为1，填充为1
        self.conv2 = nn.Conv2d(16, 32, 3, 1, 1)
        # 定义第二个池化层，使用最大池化，池化核大小为2x2，步长为2
        self.pool2 = nn.MaxPool2d(2, 2)
        # 定义一个全连接层，输入特征数为32x1x1，输出特征数为8（分类的类别数）
        self.fc = nn.Linear(32, 8)
        # 定义一个激活函数，使用ReLU
        self.relu = nn.ReLU()

    # 定义forward方法
    def forward(self, x):
        x = self.conv1(x)
        x = self.relu(x)
        # x = self.pool1(x)
        x = self.conv2(x)
        x = self.relu(x)
        # x = self.pool2(x)
        # 将输出x的形状变为(batch_size, 32x1x1)，方便输入全连接层
        x = x.view(-1, 32)
        x = self.fc(x)
        return x