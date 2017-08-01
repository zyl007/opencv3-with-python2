# coding=utf-8
"""
Created on 下午2:42 17-7-27

@author: zyl
"""
import cv2
import numpy as np
import sys

# imgpath = sys.argv[1]
imgpath = "images/city-of-varese2.jpg"
img = cv2.imread(imgpath)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# sift特征
sift = cv2.xfeatures2d.SIFT_create()
keypoints, descriptor = sift.detectAndCompute(gray, None)

# 画出关键点
img = cv2.drawKeypoints(image=img, outImage=img, keypoints=keypoints, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS,
                        color=(51, 163, 236))

cv2.imshow("sift_keypoints", img)
cv2.imwrite('sift_keypoints.jpg', img)
while True:
    if cv2.waitKey(1000/12) & 0xff==ord("q"):
        break
cv2.destroyAllWindows()


