# coding=utf-8
"""
Created on 下午2:26 17-7-27

@author: zyl
"""
import cv2
import numpy as np

img = cv2.imread('images/chess_board.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = np.float32(gray)
dst = cv2.cornerHarris(gray, 4, 23, 0.04)
img[dst>0.01*dst.max()] = [0,0,255]
cv2.imshow('corners', img)
cv2.imwrite('images/chess_board_corners.jpg', img)
cv2.waitKey()
# while True:
#     cv2.imshow('corners', img)
#     if cv2.waitKey(1000/12) & 0xff == ord("q"):
#         break
cv2.destroyAllWindows()