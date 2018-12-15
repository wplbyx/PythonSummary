#!/usr/bin/env python
# -*- coding: utf-8 -*-


def pop_sort(array):
    # 冒泡排序: 相邻的两个元素比较
    for i in range(len(array)):
        for j in range(len(array) - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
    return array


def select_sort(array):
    # 选择排序: 顾名思义，按顺序将对应的值放到指定的下标位置
    for i in range(len(array)):
        for j in range(len(array) - i):
            if array[i] > array[i + j]:
                array[i], array[i + j] = array[i + j], array[i]
    return array


def quick_sort(array):
    # 快速排序: 递归+分置 思想
    less = []; greater = []
    if len(array) <= 1:
        return array
    mid = array.pop() # 锚点值
    for x in array:
        if x <= mid: less.append(x)
        else: greater.append(x)
    return quick_sort(less) + [mid] + quick_sort(greater)


def insert_sort(array):
    # 插入排序: 将待排数据按其大小插入到已经排序的数据中的适当位置
    #         该排序分成两部分，前段部分是有序列表，后段部分是无序的 简要插入的值
    for i in range(1, len(array)):
        for j in range(i):
            if array[i] < array[j]:
                array.insert(j, array[i])
                array.pop(i + 1)
                break
    return array


def shell_sort(array):
    # 希尔排序: 一种增强的插入排序！
    #         依次将列表分组，对每一组进行插入排序，(多了分组概念)
    step = int(len(array) / 2)
    while step > 0:  # 根据步长分组
        for i in range(step, len(array)):  # 每一组进行 '插入排序'
            # 类似插入排序, 当前值(i) 与指定步长之前的值比较, 符合条件则交换位置
            while i >= step and array[i - step] > array[i]:
                array[i], array[i - step] = array[i - step], array[i]
                i -= step 
        step = int(step / 2)
    return array


def merge_sort(array):
    # 归并排序: 递归简化问题，简化成两个元素之间的排序
    def recursive(array):
        if len(array) <= 1:
            return array
        mid_idx = int(len(array) / 2)
        left_lst = recursive(array[:mid_idx])
        right_lst = recursive(array[mid_idx:])
        return merge(left_lst, right_lst)

    def merge(left_lst, right_lst):
        result = []
        while left_lst and right_lst:
            result.append(left_lst.pop(0) if left_lst[0] < right_lst[0] else right_lst.pop(0))
        if left_lst:
            result += left_lst
        if right_lst:
            result += right_lst
        return result

    return recursive(array)


def heap_sort(array):
    # 堆排序: 每次出堆结构里的根元素，输出根元素后再调整堆 使得堆再次平衡
    # 最大化堆: 就是二叉树化(层先遍历)， 最大化就是根元素是最大元素
    def max_heap(array):
        """ 调整数组 使得整个二叉树化(堆) """
        heap_size = len(array)
        for i in range((heap_size - 2) // 2, -1, -1):
            max_heapify(array, heap_size, i)

    def max_heapify(array, heap_size, root_idx):
        """
        将变动了的数组调整为 二叉树(堆), 递归调整树
        heap_size  堆大小
        root_idx   根节点下标
        """
        left_idx = 2 * root_idx + 1  # 左子树下标
        right_idx = left_idx + 1  # 右子树下标
        large_idx = root_idx  # 堆最大元素下标
        if left_idx < heap_size and array[left_idx] > array[large_idx]:
            large_idx = left_idx
        if right_idx < heap_size and array[right_idx] > array[large_idx]:
            large_idx = right_idx
        if large_idx != root_idx:
            array[large_idx], array[root_idx] = array[root_idx], array[large_idx]
            max_heapify(array, heap_size, large_idx)

    max_heap(array)
    for idx in range(len(array)-1, -1, -1):  # 反向取下标, 依次找堆里的最大值
        array[0], array[idx] = array[idx], array[0]
        max_heapify(array, idx, 0)
    return array


if __name__ == '__main__':
    """ python sort  """
    array = [7, 9, 2, 0, 5, 7, 5, 6, 3, 6, 2, 8, 1, 5, 7]
    print('原始数据: ', array[:])
    print(pop_sort(array[:]))
    print(quick_sort(array[:]))
    print(select_sort(array[:]))
    print(insert_sort(array[:]))
    print(shell_sort(array[:]))
    print(merge_sort(array[:]))
    print(heap_sort(array[:]))

