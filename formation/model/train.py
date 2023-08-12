import torch
import torch.nn as nn
import torch.optim as optim
from model import net
from util import Data2Tensor, Labels2Tensor
from data import data, labels

from rich import print

# 创建一个模型的实例
model = net()

if torch.cuda.is_available():
    model = model.cuda()

# 定义损失函数，使用交叉熵损失
criterion = nn.CrossEntropyLoss()
# 定义优化器，使用随机梯度下降优化器
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)


# 定义训练集和测试集的大小，这里假设训练集有100个样本，测试集有20个样本
train_size = 40
test_size = 7

# 定义批次的大小，这里假设每个批次有10个样本
batch_size = 10

train_data = Data2Tensor(data[:train_size])
train_labels = Labels2Tensor(labels[:train_size])
test_data = Data2Tensor(data[test_size:])
test_labels = Labels2Tensor(labels[test_size:])


# 定义训练和测试的函数
def train_and_test(model, criterion, optimizer, train_data, train_labels, test_data, test_labels, batch_size):

    # 训练是否继续
    keep_training = True

    # 训练的迭代次数
    epoch = 0

    # 训练的最大迭代次数，这里假设是10
    max_epoch = 10

    # 训练的目标准确率，这里假设是0.9
    target_accuracy = 0.9

    # 使用一个while循环，当训练继续时执行
    while keep_training:
        # 将模型设置为训练模式
        model.train()
        # 定义一个变量，表示训练集的总损失
        train_loss = 0.0
        # 定义一个变量，表示训练集的总准确数
        train_correct = 0
        # 使用一个for循环，遍历训练集的每个批次

        for i in range(0, len(train_data), batch_size):
            # 获取当前批次的数据和标签
            inputs = train_data[i:i+batch_size]
            labels = train_labels[i:i+batch_size]
            # 将数据和标签转换为适合卷积神经网络输入的形状，即(batch_size, channel, height, width)
            # 在第二个维度上增加一个维度，使得输入张量变为四维的张量
            inputs = inputs.unsqueeze(1)
            # 交换第二个维度和第四个维度，使得输入张量变为三个通道
            inputs = inputs.permute(0, 3, 2, 1)
            print(inputs, inputs.size())

            # 将优化器的梯度清零
            optimizer.zero_grad()
            # 用模型对当前批次的数据进行预测，得到输出
            outputs = model(inputs)
            # 计算输出和标签之间的损失函数
            print(outputs.view(10, -1), outputs.view(10, -1).size())
            loss = criterion(outputs.view(10, -1).type(torch.FloatTensor), labels.type(torch.FloatTensor))
            # 反向传播损失函数，计算梯度
            loss.backward()
            # 用优化器更新模型的参数
            optimizer.step()
            # 累加当前批次的损失到总损失中
            train_loss += loss.item()*data.size(0)
            # 获取输出中最大值的索引，作为预测的类别
            _, preds = torch.max(outputs, 1)
            # 比较预测的类别和真实的标签，计算正确的个数
            train_correct += torch.sum(preds == labels.long())

        # 计算训练集的平均损失
        train_loss = train_loss / len(train_data)
        # 计算训练集的准确率
        train_accuracy = train_correct / len(train_data)
        # 打印训练集的平均损失和准确率
        print(
            f'Epoch {epoch}, Train loss: {train_loss:.4f}, Train accuracy: {train_accuracy:.4f}')

        # 将模型设置为评估模式
        model.eval()
        test_loss = 0.0
        test_correct = 0

        for i in range(0, len(test_data), batch_size):
            inputs = test_data[i:i+batch_size]
            labels = test_labels[i:i+batch_size]
            inputs = inputs.permute(0, 3, 1, 2)

            outputs = model(inputs)
            loss = criterion(outputs, labels.long())
            test_loss += loss.item()
            _, preds = torch.max(outputs, 1)
            test_correct += torch.sum(preds == labels.long())
            
        test_loss = test_loss / len(test_data)
        
        test_accuracy = test_correct / len(test_data)
        
        print(
            f'Epoch {epoch}, Test loss: {test_loss:.4f}, Test accuracy: {test_accuracy:.4f}')


        if test_accuracy >= target_accuracy or epoch >= max_epoch:
            keep_training = False
        else:
            epoch += 1


train_and_test(model, criterion, optimizer, train_data,
               train_labels, test_data, test_labels, batch_size)
