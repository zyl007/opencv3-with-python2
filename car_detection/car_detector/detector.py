# coding=utf-8
"""
Created on 下午3:23 17-7-26

@author: zyl
"""

import cv2
import numpy as np
from sklearn import svm

datapath = "/home/knight/PycharmProjects/opencv3-with-python2/car_detection/CarData/TrainImages"
SAMPLES = 400

def path(cls, i):
    return "%s/%s%d.pgm" % (datapath, cls, i)

def get_flann_matcher():
    """
    近邻特征匹配
    :return:
    """
    flann_params = dict(algorithm=1, trees=5)
    return cv2.FlannBasedMatcher(flann_params, {})

def get_bow_extractor(extract, flann):
    return cv2.BOWImgDescriptorExtractor(extract, flann)

def get_extract_detect():
    return cv2.xfeatures2d.SIFT_create(), cv2.xfeatures2d.SIFT_create()

def extract_sift(fn, extractor, detector):
    im = cv2.imread(fn, 0)
    return extractor.compute(im, detector.detect(im))[1]

def bow_features(img, extractor_bow, detector):
    """
    返回BOW特征值
    :param img:
    :param extractor_bow: 设置好的视觉词典
    :param detector:  提取视觉词典特征
    :return:
    """
    return extractor_bow.compute(img, detector.detect(img))

def car_detector():
    """
    返回训练好的分类器和视觉词表
    :return:
    """

    pos, neg = "pos-", "neg-"
    detect, extract = get_extract_detect()
    matcher = get_flann_matcher()  # 特征匹配，用于填入bow
    print("---利用k-means构建视觉图像词汇---")
    bow_kmeans_trainer = cv2.BOWKMeansTrainer(1000)  # 取 1000维的图像词汇特征
    extract_bow = cv2.BOWImgDescriptorExtractor(extract, matcher)

    print(" bow训练器中添加特征")
    for i in range(120):
        print(i)
        bow_kmeans_trainer.add(extract_sift(path(pos, i), extract, detect))
        bow_kmeans_trainer.add(extract_sift(path(neg, i), extract, detect))

    # 聚类降维 输出应该是 1000d
    voc = bow_kmeans_trainer.cluster()
    extract_bow.setVocabulary(voc)

    # 构建训练数据
    train_data, train_labels = [], []
    print("添加训练数据")
    for i in range(SAMPLES):
        print(i)
        # 正例
        train_data.extend(bow_features(cv2.imread(path(pos, i), 0), extract_bow, detect))
        train_labels.append(1)
        # 负例
        train_data.extend(bow_features(cv2.imwrite(path(neg, i), 0), extract_bow, detect))
        train_labels.append(-1)

    clf = svm.SVC(gamma=0.5, C=30)
    clf.fit(np.array(train_data), np.array(train_labels))

    return clf, extract_bow

