# coding=utf-8
"""
Created on 下午3:24 17-7-26
非最大抑制，消除重叠窗口
思想： 得到一些列的矩阵，并对这些矩阵按评分进行排序。从评分最高的矩阵开始，消除所有重叠超过一定阀值的矩阵，消除的规则是计算相交的区域，并
看这些相交区域是否大于某个阀值。
@author: zyl
"""
import numpy as np


def non_max_suppression_fast(boxes, overlapThresh=0.5):
    # 如果没有boxes窗口，返回空
    if len(boxes) == 0:
        return []

    # 如果boxes中数值是整数转为float，因为后面需要进行除的运算
    if boxes.dtype.kind == "i":
        boxes = boxes.astype("float")

    # 初始化处理索引 indexes
    pick = []

    # 划分除对应的坐标
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]
    scores = boxes[:, 4]  # 窗口的得分值，实际上是svm分类的概率值

    # 计算区域面积进行排序 向量之间的运算
    area = (x2 - x1 +1) * (y2 - y1 + 1)

    idxs = np.argsort(scores)  # scores的索引按照值的大小排序
    # print(idxs)
    # 循环处理所有框
    while len(idxs) > 0:

        last = len(idxs) - 1  # 最后一个的索引值，-> 最大值对应的下标
        i = idxs[last]
        pick.append(i)

        # 求交叉面积，当前最大 与从1到次大的面积进行依次计算
        # 左上角相交点
        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        # 右下角相交点
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])

        # 计算重叠区域的面积
        w = np.maximum(0, xx2-xx1+1)
        h = np.maximum(0, yy2-yy1+1)

        # 计算重叠比例
        overlap = (w*h)/area[idxs[:last]]
        # tmp = np.where(overlap > overlapThresh)[0]
        idxs = np.delete(idxs, np.concatenate(([last],
                                               np.where(overlap > overlapThresh)[0])))
        print(idxs)
        # 返回picked中的边界框

    return boxes[pick].astype("int")


if __name__ == '__main__':
    boxes = np.array([[1,1,1,1,0.8], [2,2,3,3,0.1]])
    print (non_max_suppression_fast(boxes))
