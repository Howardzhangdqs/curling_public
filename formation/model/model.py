import torch.nn as nn


# 定义卷积神经网络模型类
class net(nn.Module):

    def __init__(self):
        super(net, self).__init__()
        # 定义第一个卷积层，输入通道数为3（color, offsetX, offsetY）
        self.conv1 = nn.Conv2d(3, 16, 3, 1, 1)
        self.conv2 = nn.Conv2d(16, 32, 3, 1, 1)
        self.fc = nn.Linear(32, 8)
        self.relu = nn.ReLU()

    # 定义forward方法
    def forward(self, x):
        x = self.conv1(x)
        x = self.relu(x)
        x = self.conv2(x)
        x = self.relu(x)

        # 将输出x的形状变为(batch_size, 32x1x1)，方便输入全连接层
        x = x.view(-1, 32)

        x = self.fc(x)
        return x