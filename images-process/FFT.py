# coding=utf-8
"""
Created on 上午10:55 17-7-27
傅里叶变换示例  : 高通滤波器 低通滤波器
@author: zyl
"""
import cv2
import numpy as np
from scipy import ndimage

kernel_3X3 = np.array([[-1, -1, -1],
                       [-1, 8, -1],
                       [-1, -1, -1]])

kernel_5X5 = np.array([[-1, -1, -1, -1, -1],
                       [-1, 1, 2, 1, -1],
                       [-1, 2, 4, 2, -1],
                       [-1, 1, 2, 1, -1],
                       [-1, -1, -1, -1, -1]])


def high_pass_filter(img, kernel):
    return ndimage.convolve(img, kernel)

def test_high_pass_filter():
    img = cv2.imread('0.png', 0)
    k3 = high_pass_filter(img, kernel_3X3)
    k5 = high_pass_filter(img, kernel_5X5)
    blurred = cv2.GaussianBlur(img, (11, 11), 0)
    g_hpf = img - blurred
    cv2.imshow('3x3', k3)
    cv2.imwrite('3x3.png', k3)
    cv2.imshow('5x5', k5)
    cv2.imwrite('5x5.png', k5)
    cv2.imshow('g_hpf', g_hpf)
    cv2.imwrite('g_hpf.png', g_hpf)
    cv2.waitKey()
    cv2.destroyAllWindows()


def low_pass_filter(img, kernel):
    pass

if __name__ == '__main__':

    # test_high_pass_filter()
    pass