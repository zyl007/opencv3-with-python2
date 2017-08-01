# coding=utf-8
"""
Created on 下午3:02 17-7-27

@author: zyl
"""
import cv2
import sys
import numpy as np

# imgpath = sys.argv[1]
imgpath = "images/city-of-varese2.jpg"
img = cv2.imread(imgpath)
alg = "SURF"
thresh = 4000

def fd(algorithm):
    if algorithm == "SIFT":
        return cv2.xfeatures2d.SIFT_create()
    if algorithm == "SURF":
        return cv2.xfeatures2d.SURF_create(float(thresh))


gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

fd_alg = fd(alg)
keypoints, descriptor = fd_alg.detectAndCompute(gray, None)

img = cv2.drawKeypoints(image=img, outImage=img, keypoints=keypoints,
                        flags=4, color=(51, 163, 236))

cv2.imshow('keypoints', img)
cv2.imwrite('images/SURF.jpg', img)
while True:
    if cv2.waitKey(1000/12) & 0xff==ord("q"):
        break

cv2.destroyAllWindows()
