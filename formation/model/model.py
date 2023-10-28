import torch.nn as nn


# 生成块
def makeBlock(input_len, output_len, hidden_len=64):
    return nn.Sequential(
        nn.Linear(input_len, hidden_len),
        nn.ReLU(),
        nn.Linear(hidden_len, output_len),
        nn.ReLU(),
    )


# 定义卷积神经网络模型类
class net(nn.Module):

    def __init__(self):
        super(net, self).__init__()
        # 定义第一个全连接层，输入一个长度为20的序列，每个包含三个通道（color, offsetX, offsetY）
        self.block1 = makeBlock(3 * 20, 64)
        self.block2 = makeBlock(64, 32)
        self.block3 = makeBlock(32, 8)

    def forward(self, x):

        x = self.block1(x)
        x = self.block2(x)
        x = self.block3(x)

        return x


if __name__ == "__main__":
    # 测试
    model = net()
    print(model)
