# coding=utf-8
"""
Created on 下午3:50 17-7-27

@author: zyl
"""
import numpy as np
import cv2
from matplotlib import pyplot as plt

img1 = cv2.imread("images/img1.png", 0)
img2 = cv2.imread("images/img2.png", 0)

# ORB算法调用
orb = cv2.ORB_create()

kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(img2, None)

bf = cv2.BFMatcher()
matches = bf.knnMatch(des1, des2, k=2)
# matches = sorted(matches, key=lambda x:x.distance)
img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, matches,
                      img2, flags=2)
plt.imshow(img3)
plt.imsave('images/knnMatch_img3.png', img3)
plt.show()