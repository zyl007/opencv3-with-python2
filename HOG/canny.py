# coding=utf-8
"""
Created on 下午5:12 17-7-24

@author: zyl
"""
import cv2

path = "people.jpg"

img = cv2.imread(path, 0)
cv2.imwrite('canny.jpg', cv2.Canny(img, 200, 300))
cv2.imshow("canny", cv2.imread("canny.jpg"))
cv2.waitKey()
cv2.destroyAllWindows()