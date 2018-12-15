#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import scipy.special

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

		# 初始化 输入层和隐藏层 之间的链接权重 [-0.5, 0.5]
		# self.wih = (np.random.rand(self.hnodes, self.inodes) - 0.5)  # 随机式
		self.wih = np.random.normal(0.0, pow(self.hnodes, -0.5), (self.hnodes, self.inodes))  # 正态分布式

		# 初始化 隐藏层和输出层 之间的链接权重 [-0.5, 0.5]
		# self.who = (np.random.rand(self.onodes, self.hnodes) - 0.5)  # 随机式
		self.who = np.random.normal(0.0, pow(self.onodes, -0.5), (self.onodes, self.hnodes))  # 正态分布式

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
		hidden_inputs = np.dot(self.wih, inputs)  # 计算每个输入进过加权运输之后 到达隐藏层每个节点的输入总值
		hidden_outputs = self.active_function(hidden_inputs)  # 隐藏层输出
		outputs = np.dot(self.who, hidden_outputs)  # 矩阵运算 隐藏层映射到输出层节点
		final_outputs = self.active_function(outputs)  # 调用激化函数，输出结果

		# 2. 根据误差调整权重
		targets = np.array(targets_list, ndmin=3).T 
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



if __name__ == '__main__':
	""" hello world """
	input_nodes = 3
	hidden_nodes = 3
	output_nodes = 3
	learning_rate = 0.3

	# 实例化 NeuralNetwork 神经网络对象: network
	network = NeuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)
	ret = network.query([0.9, 0.375, -0.13])
	print(ret)


