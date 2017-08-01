# coding=utf-8
"""
Created on 下午3:27 17-7-24
python2.7
@author: zyl
"""
import cv2
import numpy as np
# from matplotlib import pyplot as plt

print("cv2__version__", cv2.__version__)

person_path = "person.png"

def is_inside(o, i):
    """
    判断某个矩阵是否完全包含另外一个矩阵
    :param o: 外层矩阵
    :param i: 内层矩阵
    :return:
    """
    ox, oy, ow, oh = o
    ix, iy, iw, ih = i
    return ox > ix and oy > iy and ow > iw and oh > ih


def draw_person(image, person):
    x, y, w, h = person
    cv2.rectangle(image, (x,y), (x+w, y+h), (0, 0, 255), 2)

img = cv2.imread(person_path)

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

found, w = hog.detectMultiScale(img,  winStride=(8,8), padding=(32,32), scale=1.05)

found_filtered = []
for ri, r in enumerate(found):
    for qi, q in enumerate(found):
        if ri != qi and is_inside(r, q):
            break
        else:
            found_filtered.append(r)

for person in found_filtered:
    draw_person(img, person)

cv2.imshow("people detection", img)
cv2.imwrite("people-detection.png", img)
cv2.waitKey(0)
cv2.destroyAllWindows()