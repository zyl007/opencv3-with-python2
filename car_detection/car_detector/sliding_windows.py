# coding=utf-8
"""
Created on 下午3:41 17-7-26

@author: zyl
"""

def sliding_window(image, stepSize, windowSize):
    """
    滑动窗口实现
    :param image:
    :param stepSize: 步长
    :param windowSize:  窗口大小
    :return: 生成每一个滑动窗口
    """
    for y in xrange(0, image.shape[0], stepSize):
        for x in xrange(0, image.shape[1], stepSize):
            yield (x, y, image[y:y+windowSize[1], x:x+windowSize[0]])