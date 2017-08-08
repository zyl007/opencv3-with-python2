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
    print(type(imgs), imgs[0])
    areas = [(i, im.size[0] * im.size[1]) for i, im in enumerate(imgs)]  # idx: area
    w, h = out_size
    print(areas)
    areas = sorted(areas, key = lambda x:x[1], reverse=True)  # 按照面积大小排序 降序
    new_img = Image.new('RGB', out_size)
    frist_x, frist_y = 0, 0
    tmp_x, tmp_y = 0,0
    # todo 图片拼接核心功能
    # 按行拼接
    # 记录每一行第一个图的坐标 ，便于下次计算
    num = 0
    while num < len(areas):
        idx, _ = areas[num]
        t_w, t_h = imgs[idx].size  # box宽高
        if (w-t_w-tmp_y) >= 0:

            new_img.paste(imgs[idx], (tmp_y, tmp_x))  # 指定位置paste图片
            tmp_y += t_w
            frist_x = max(frist_x, tmp_x + t_h)

        elif(h-t_h-tmp_x) >=0:
            tmp_x = frist_x
            tmp_y = 0

            new_img.paste(imgs[idx], (tmp_y, tmp_x))
            tmp_y += t_w
            frist_x = max(frist_x, tmp_x + t_h)
        else:
            # new_img.save('new_img_%d.jpg'%num)
            new_img.show()
            print('new picture')
            new_img = Image.new('RGB', out_size)
            frist_x, frist_y = 0, 0
            tmp_x, tmp_y = 0, 0
        num += 1

    return new_img





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

def main_test():
    im_2 = Image.open('test_images/test.png')
    imgs = [im_2.resize((930,500)), im_2, im_2, im_2.resize((800,300)), im_2, im_2, im_2.resize((250,300)), im_2.resize((250,295)), \
            im_2, im_2, im_2, im_2, im_2, im_2,im_2,im_2,im_2]
    paste_by_size(out_size, imgs).show()


def main():
    im_2 = Image.open('test_images/test.png')
    imgs = [im_2, im_2, im_2, im_2, im_2, im_2, im_2, im_2, im_2, im_2]
    paste_fixed_windows(out_size, imgs).show()

main_test()
# main()

