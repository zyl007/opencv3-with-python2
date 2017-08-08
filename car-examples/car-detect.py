# coding=utf-8
"""
Created on 上午11:39 17-7-25
汽车检测代码  python2 + opencv3
@author: zyl
"""
from sklearn import svm
import cv2
import numpy as np
from os.path import join

datapath = "./CarData/TrainImages/"

# neg-27.pgm
def path(cls, i):
    return "%s/%s%d.pgm"%(datapath, cls, i)

pos, neg = "pos-", "neg-"

detect = cv2.xfeatures2d.SIFT_create()  # SIFT特征
extract = cv2.xfeatures2d.SIFT_create()
# flann匹配算法
flann_params = dict(algorithm=1, trees=5)
flann = cv2.FlannBasedMatcher(flann_params, {})

# k均值聚类
bow_kmeans_trainer =cv2.BOWKMeansTrainer(40)
extract_bow = cv2.BOWImgDescriptorExtractor(extract, flann)

def extract_sift(fn):
    im = cv2.imread(fn, 0)  # 灰度值读取
    return extract.compute(im, detect.detect(im))[1]

for i in range(8):
    bow_kmeans_trainer.add(extract_sift(path(pos, i)))
    bow_kmeans_trainer.add(extract_sift(path(neg, i)))

voc = bow_kmeans_trainer.cluster()
extract_bow.setVocabulary(voc)

def bow_features(fn):
    im = cv2.imread(fn, 0)
    return extract_bow.compute(im, detect.detect(im))

# 构建训练集
traindata, trainlabels = [], []
for i in range(20):
    traindata.extend(bow_features(path(pos, i)))
    trainlabels.append(1)

    traindata.extend(bow_features(path(neg, i)))
    trainlabels.append(-1)

clf = svm.SVC(kernel='linear')
clf.fit(np.array(traindata), np.array(trainlabels))
svm = clf
# SVM分类器 use opencv3 ml
# svm = cv2.ml.SVM_create()
# svm.train(np.array(traindata), cv2.ml.ROW_SAMPLE, np.array(trainlabels))

# SVM预测
def predict(fn):
    f = bow_features(fn)
    p = svm.predict(f)
    print(p)


    # print(fn, "\t", p[0])
    return int(p[0])


car, notcar = "/home/knight/PycharmProjects/opencv3-with-python2/car-examples/CarData/TrainImages/pos-100.pgm", "/home/knight/PycharmProjects/opencv3-with-python2/car-examples/CarData/TrainImages/neg-13.pgm"
car_img = cv2.imread(car)
notcar_img = cv2.imread(notcar)

car_predict = predict(car)
not_car_predict = predict(notcar)

# 设置字体
font = cv2.FONT_HERSHEY_SIMPLEX

if (car_predict == 1):
    cv2.putText(car_img, "Detected", (10,20), font,
                1, (0,0,255), 2, cv2.LINE_AA)

if (not_car_predict == -1):
    cv2.putText(notcar_img, "not Detected", (10,20), font,
                1, (0,0,255), 2, cv2.LINE_AA)

cv2.imshow("BOW + SVM Success", car_img)
cv2.imshow("BOW + SVM Failure", notcar_img)
cv2.imwrite('car_img.jpg', car_img)
cv2.imwrite('not_car_img.jpg', notcar_img)
cv2.waitKey(0)
cv2.destroyAllWindows()