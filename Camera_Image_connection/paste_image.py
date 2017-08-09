# coding=utf-8
"""
Created on 下午3:36 17-8-8
假定box宽高变化不大，选取最大的宽高来分割 全图，依次贴图
1. 先贴大图，再贴小图
9,1_1,359,188,423,269
<box编号> <相机编号_frame号> <points>

第一个9代表box编号，1_1   是图像名   ，前面1代表哪个相机，后面1代表该相机的第几帧，后面是左上右下

@author: zyl
"""
from PIL import Image
import numpy as np
import glob
import io
out_size = (1920, 1080)
txtfile = '/home/knight/PycharmProjects/opencv3-with-python2/Camera_Image_connection/data/boxs.txt'
path = '/home/knight/PycharmProjects/opencv3-with-python2/Camera_Image_connection/data/outImage/'

def load_imgs(txtfile, path):
    # 加载数据
    current_frame = 0
    files = io.open(txtfile, encoding='utf-8').readlines()
    box_file_location = {}
    for line in files:
        tmp = line.strip().split(',')
        box, file_name, points = tmp[0],tmp[1],tmp[2:]
        box_file_location[file_name] = box, points  # {文件名: (box序号, box坐标)}
    frame_names = glob.glob(path+'*_%d.jpg'%current_frame)
    while frame_names:
        for name in frame_names:
            file_name = name.split('/')[-1][:-4]
            print(file_name,box_file_location.get(file_name))
            if box_file_location.get(file_name):  # 有标记box才进行处理
                box, points = box_file_location(file_name)
                x_min, y_min, x_max, y_max = map(float, points)
                w, h = (y_max-y_min), (x_max-x_min)
                size = (w,h)
                label = (box, )
                pass
            print(name)
        print('##################')
        current_frame += 1
        frame_names = glob.glob(path + '*_%d.jpg' % current_frame)



def paste_by_size(out_size, imgs, savepath='output', frame='0'):
    """
    :param out_size: 输出的拼接图的size
    :param imgs: 输入的每一帧的box区域 dict: {box序号1:img1,box序号2:img2....}
    :return: 返回box序号对应的新坐标  dict: {box1: <new_l_points, new_r_points>, 拼接图序号}
    """
    record = {}
    pic_num = 0

    areas = [(box_num, img.size[0] * img.size[1]) for box_num, img in imgs.items()]  # idx: area
    w, h = out_size

    areas = sorted(areas, key = lambda x:(x[1],x[0]), reverse=True)  # 按照面积大小排序 降序

    new_img = Image.new('RGB', out_size)
    frist_x, frist_y = 0, 0
    tmp_x, tmp_y = 0,0
    # 按行拼接
    # 记录每一行第一个图的坐标 ，便于下次计算
    num = 0
    while num < len(areas):
        box_num, _ = areas[num]
        t_w, t_h = imgs[box_num].size  # box宽高
        if (w-t_w-tmp_y) >= 0 and (h-t_h-tmp_x) >=0:
            new_img.paste(imgs[box_num], (tmp_y, tmp_x))  # 指定位置paste图片
            l_x, l_y = tmp_x, tmp_y
            r_x, r_y = l_x + t_h, l_y + t_w
            record[box_num] = (l_x, l_y, r_x, r_y), pic_num
            tmp_y += t_w
            frist_x = max(frist_x, tmp_x + t_h)
        elif((w-t_w-tmp_y) < 0 and (h-t_h-frist_x) >=0):  # 跳转到下一行开始粘贴
            tmp_x = frist_x
            tmp_y = 0
            new_img.paste(imgs[box_num], (tmp_y, tmp_x))
            l_x, l_y = tmp_x, tmp_y
            r_x, r_y = l_x + t_h, l_y + t_w
            record[box_num] = (l_x, l_y, r_x, r_y), pic_num

            tmp_y += t_w
            frist_x = max(frist_x, tmp_x + t_h)
        else:

            new_img.save(savepath + '/frame_{frame}_{num}.jpg'.format(frame=frame, num=pic_num))
            pic_num += 1
            new_img.show()
            # print('new picture')
            new_img = Image.new('RGB', out_size)
            frist_x, frist_y = 0, 0
            tmp_x, tmp_y = 0, 0
        num += 1

    # print(u'new points', record)
    new_img.save(savepath + '/frame_{frame}_{num}.jpg'.format(frame=frame, num=pic_num))
    return record





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
    im_3 = Image.open('test_images/3.png')
    imgs = {'1': im_2, '2':im_2,'21': im_2, '22':im_2,'1z': im_2, '2c':im_2,'cc1': im_2, '2nh':im_2,'1cr': im_2, '2':im_2, \
            '112': im_2, '2xd': im_2.resize((800,300)),'ad1': im_2, '2':im_2,'1': im_2, '2':im_2,'1': im_2, '2zfe':im_2,'1125': im_2.resize((800,300)), '2':im_2, \
            '1': im_2, '2a': im_2,'1': im_2, '31':im_2,'11': im_2, '434':im_2,'1': im_2, '2':im_2.resize((800,300)),'1': im_2, '2':im_2,}
    # imgs = [im_2.resize((730,400)), im_3, im_3, im_2.resize((800,300)), im_2, im_3, im_3.resize((450,300)), im_2.resize((750,295)), \
    #         im_2, im_3, im_2, im_2, im_2.resize((500,600)), im_2,im_2,im_2,im_3,im_2, im_2, im_2, im_3, \
    #         im_2.resize((700, 600)), im_3, im_3, im_2, im_3, im_2, im_2, im_2]
    paste_by_size(out_size, imgs)


def main():
    im_2 = Image.open('test_images/test.png')
    imgs = [im_2, im_2, im_2, im_2, im_2, im_2, im_2, im_2, im_2, im_2]
    paste_fixed_windows(out_size, imgs)

main_test()
# main()
# load_imgs(txtfile, path)



