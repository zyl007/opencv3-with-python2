# coding=utf-8
"""
Created on 上午11:48 17-7-27

@author: zyl
"""
import cv2

filename = "images/Vikings_2.png"

def detect(filename):
    face_cascade = cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_default.xml')
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for x, y, w, h in faces:
        img = cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0),2)

    cv2.namedWindow("Vikings Detected!")
    cv2.imshow("viking detected ", img)
    cv2.imwrite('./result_vikings.jpg', img)
    cv2.waitKey()
    cv2.destroyAllWindows()

detect(filename)