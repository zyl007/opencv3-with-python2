# coding=utf-8
"""
Created on 下午3:26 17-7-26

@author: zyl
"""
import cv2
import numpy as np
from car_detector.detector import car_detector, bow_features
from car_detector.pyramid import pyramid
from car_detector.non_maximum import non_max_suppression_fast as nms
from car_detector.sliding_windows import sliding_window

def in_range(number, test, thresh=0.2):
    return abs(number-test) < thresh

test_image = "/home/knight/PycharmProjects/opencv3-with-python2/car_detection/CarData/TestImages_Scale/test-0.pgm"

svm, extractor = car_detector()
detect = cv2.xfeatures2d.SIFT_create()

w, h = 100, 40
img = cv2.imread(test_image)

# 参数设置
rectangles = []
counter = 1
scaleFactor = 1.25
scale = 1
font = cv2.FONT_HERSHEY_SIMPLEX

for resized in pyramid(img, scaleFactor):
    # 缩放比
    scale =float(img.shape[1]) / float(resized.shape[1])
    for (x, y, roi) in sliding_window(resized, 20, (w,h)):
        if roi.shape[1] != w or roi.shape[0] != h:
            continue
        try:
            bf = bow_features(roi, extractor, detect)
            result = svm.predict(bf)
            score = svm.predict_proba(bf)
            print("类别：%d 的得分值是： %f "%(result, score))
            if result == 1:
                if score < 1.0:
                    rx, ry, rx2, ry2 = int(x*scale), int(y*scale), int((x+w)*scale), int((y+h)*scale)

                    rectangles.append([rx, ry, rx2, ry2, abs(scale)])
        except:
            pass
        counter += 1

windows = np.array(rectangles)
boxes = nms(windows, 0.25)

for (x,y,x2,y2,score) in boxes:
    print(x,y,x2,y2,score)
    cv2.rectangle(img, (int(x), int(y)), (int(x2), int(y2)), (0, 255, 0), 1)
    cv2.putText(img, "%f"%score, (int(x), int(y)), font, 1, (0, 255,0))


cv2.imshow('img', img)
cv2.waitKey(0)
