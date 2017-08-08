# coding=utf-8
"""
Created on 下午3:36 17-8-8
假定box宽高变化不大，选取最大的宽高来分割 全图，依次贴图
1. 先贴大图，再贴小图

@author: zyl
"""
from PIL import Image
import numpy as np
out_size = (1920, 1080)


def paste_by_size(out_size, imgs):
    """
    1. 按照imgs大小排序
    2. 依次处理

    :param out_size: 输出图像的size
    :param imgs: 输入的所有box
    :return:
    """
    areas = [{i: im.size[0] * im.size[1]} for i, im in enumerate(imgs)]  # idx: area

    asc_ares = sorted(areas, key=lambda x:x.values())  # 按照面积大小排序 升序
    new_img = Image.new('RGB', out_size)
    tmp_x, tmp_y = 0, 0
    # todo 图片拼接核心功能
    # 按行拼接
    # 记录每一行第一个图的坐标 ，便于下次计算
    pass



def paste_fixed_windows(out_size, imgs):
    # 固定窗口大小
    #     h = imgs[2] - imgs[0]
    #     w = imgs[3] - imgs[1]
    #     m_h, m_w = max(h), max(w)
    m_h, m_w = 328, 462
    num = 0
    new_img = Image.new('RGB', out_size)
    for x_i in range(0, out_size[1], m_h):
        for y_i in range(0, out_size[0], m_w):

            if len(imgs) > num and (1920 - y_i) > m_w and (1080 - x_i) > m_h:
                print((x_i, y_i))
                new_img.paste(imgs[num], (y_i, x_i))  # box: (y_i, x_i)
                num += 1
            else:
                pass
    return new_img




def main():
    im_2 = Image.open('test_images/test.png')
    imgs = [im_2, im_2, im_2, im_2, im_2, im_2, im_2, im_2, im_2, im_2]
    paste_fixed_windows(out_size, imgs).show()

main()

