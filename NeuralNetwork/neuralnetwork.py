#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import scipy.special
import matplotlib.pyplot


class NeuralNetwork(object):
    def __init__(self, inputnodes, hiddennodes, outputnodes, learningrate):
        """ 初始化 神经网络 关键参数
        inputnodes:   输入层节点数
        hiddennodes:  隐藏层节点数
        outputnodes:  输出层节点数
        learningrate: 神经网络学习率
        """
        self.inodes = inputnodes
        self.hnodes = hiddennodes
        self.onodes = outputnodes
        self.learn = learningrate

        # 初始化 输入层和隐藏层, 隐藏层和输出层 之间的链接权重 [-0.5, 0.5]
        self.wih = self.init_weight(typ='input')
        self.who = self.init_weight(typ='output')

        # 初始化激化函数: 调用 scipy.special 库里的 expit() 函数
        self.active_function = lambda x: scipy.special.expit(x)

    def train(self, inputs_list, targets_list):
        """ 训练神经网络链接权重
        训练网络分两步:
            1. 计算输出
            2. 根据误差调整权重
        """
        # 1. 计算输出
        inputs = np.array(inputs_list, ndmin=2).T  # 对角翻折矩阵 计算输入矩阵
        targets = np.array(targets_list, ndmin=2).T

        hidden_inputs = np.dot(self.wih, inputs)  # 计算每个输入进过加权运输之后 到达隐藏层每个节点的输入总值
        hidden_outputs = self.active_function(hidden_inputs)  # 隐藏层输出
        final_inputs = np.dot(self.who, hidden_outputs)  # 矩阵运算 隐藏层映射到输出层节点
        final_outputs = self.active_function(final_inputs)  # 调用激化函数，输出结果

        # 2. 根据误差调整权重
        output_error = targets - final_outputs
        # Error_hidden = Weights_hidden_output.T * Error_output
        hidden_errors = np.dot(self.who.T, output_error)  # 计算得到隐藏层输出误差

        # 调整 隐藏层到输出层 之间链接权重误差
        hoe_mete = np.dot(output_error * final_outputs * (1.0 - final_outputs), np.transpose(hidden_outputs))
        self.who += self.learn * hoe_mete

        # 调整 输入层到隐藏层 之间链接权重误差
        ihe_mete = np.dot(hidden_errors * hidden_outputs * (1.0 - hidden_outputs), np.transpose(inputs))
        self.wih += self.learn * ihe_mete

    def query(self, inputs_list):
        """ 通过训练好的神经网络来预测或查询需要的数据 """
        inputs = np.array(inputs_list, ndmin=2).T  # 对角翻折矩阵 计算输入矩阵
        hidden_inputs = np.dot(self.wih, inputs)  # 计算每个输入进过加权运输之后 到达隐藏层每个节点的输入总值
        hidden_outputs = self.active_function(hidden_inputs)  # 隐藏层输出
        outputs = np.dot(self.who, hidden_outputs)  # 矩阵运算 隐藏层映射到输出层节点
        return self.active_function(outputs)  # 调用激化函数，输出结果

    def init_weight(self, typ='input'):
        """  """
        if typ == 'input':
            try:
                return np.load('./wih_file.npy')
            except:
                # return (np.random.rand(self.hnodes, self.inodes) - 0.5)  # 随机式
                return np.random.normal(0.0, pow(self.hnodes, -0.5), (self.hnodes, self.inodes))  # 正态分布式
        elif typ == 'output':
            try:
                return np.load('./who_file.npy')
            except:
                # return (np.random.rand(self.onodes, self.hnodes) - 0.5)  # 随机式
                return np.random.normal(0.0, pow(self.onodes, -0.5), (self.onodes, self.hnodes))  # 正态分布式

    def save_weight(self, success):
        """  """
        old_success = None
        with open('./success.txt', 'r') as fp:
            try:
                for row in fp:
                    data = [i.strip() for i in row.split('=')]
                    old_success = float(data[1])
            except:
                if type(old_success) is not float:
                    old_success = -1.0
        if old_success is None or success >= old_success:
            wih_file = './wih_file.npy'  # 输出层到隐藏层 权重文件
            who_file = './who_file.npy'  # 隐藏层到输出层 权重文件
            np.save(wih_file, self.wih)
            np.save(who_file, self.who)
            with open('./success.txt', 'w') as fp:
                data = 'data={}'.format(success)
                fp.write(data)


def network_train():
    input_nodes = 784
    hidden_nodes = 200
    output_nodes = 10
    learning_rate = 0.1

    # 实例化 NeuralNetwork 神经网络对象: network
    network = NeuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)

    # 读取 train_data.csv 文件, 开始训练 神经网络
    print('Start train ...')
    with open('./numbers/mnist_train.csv', 'r') as fp:
        for idx, row in enumerate(fp):
            all_data_values = row.split(',')
            scaled_img_input = (np.asfarray(all_data_values[1:]) / 255.0 * 0.99) + 0.01  # (缩小)格式化图像数据
            targets = np.zeros(output_nodes) + 0.1  # 初始化 target 数据
            targets[int(all_data_values[0])] = 0.99  #
            network.train(scaled_img_input, targets)
    print('End of train!')

    # 测试训练后的 神经网络
    query_data = []
    count_data = 0
    with open('./numbers/mnist_test.csv', 'r') as fp:
        for idx, row in enumerate(fp):
            print('==' * 10)
            all_data_values = row.split(',')
            corrent_label = all_data_values[0]
            print('当前测试数据是: {:>6}'.format(corrent_label))

            inputs = (np.asfarray(all_data_values[1:]) / 255.0 * 0.99) + 0.01
            output = network.query(inputs)
            anser = np.argmax(output)
            print('神经网络预测数据: {:>4}'.format(anser))

            count_data += 1
            if int(corrent_label) == int(anser):
                query_data.append(anser)

    print('成功率: {}'.format(len(query_data) / count_data))
    network.save_weight(len(query_data) / count_data)


def data_img():
    with open('./numbers/train_data.csv', 'r') as fp:
        for idx, row in enumerate(fp):
            all_data_values = row.split(',')
            img_array = np.asfarray(all_data_values[1:]).reshape((28, 28))
            matplotlib.pyplot.imshow(img_array, cmap='Greys', interpolation='None')


if __name__ == '__main__':
    """ hello world """
    network_train()
    # data_img()
