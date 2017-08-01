# coding=utf-8
"""
Created on 下午3:24 17-7-26

@author: zyl
"""
import cv2


# 按照比例缩放
def resize(img, scaleFactor):
    return cv2.resize(img, (int(img.shape[1] * (1 / scaleFactor)),
                            int(img.shape[0] * (1 / scaleFactor))),
                      interpolation=cv2.INTER_AREA)


# 图像金字塔

def pyramid(image, scale=1.5, minSize=(200, 80)):
    yield image

    while True:
        image = resize(image, scaleFactor=scale)
        if image.shape[0] < minSize[1] or image.shape[1] < minSize[0]:
            break
        yield image