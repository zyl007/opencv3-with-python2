# coding=utf-8
"""
Created on 下午12:40 17-8-9

@author: zyl
"""
from PIL import Image
import cv2

def convert_BGR2GB(cv2_img):
    """
    将opencv图片转PIL处理
    :param cv2_img:
    :return:
    """
    im = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)  # 转换颜色通道
    return Image.fromarray(im)

def paste_by_size(out_size, imgs, savepath='output', frame='0'):
    """

    :param out_size: 输出的拼接图的size
    :param imgs: 输入的每一帧的box区域 dict: {box序号1:img1,box序号2:img2....}
    :param savepath: 保存路径
    :param frame: 当前帧数，用于文件命名
    :return: 返回box序号对应的新坐标  dict: {box1: <new_l_points, new_r_points>, 拼接图序号}
            保存文件格式 frame_{frame}_{num}.jpg
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
            # new_img.show()
            # print('new picture')
            new_img = Image.new('RGB', out_size)
            frist_x, frist_y = 0, 0
            tmp_x, tmp_y = 0, 0
        num += 1

    # print(u'new points', record)
    new_img.save(savepath + '/frame_{frame}_{num}.jpg'.format(frame=frame, num=pic_num))
    return record

def paste_by_size_test():
    out_size = 1920,1080
    im_2 = Image.open('test_images/test.png')
    im_3 = Image.open('test_images/3.png')
    imgs = {'1': im_2, '2':im_2,'21': im_2, '22':im_2,'1z': im_2, '2c':im_2,'cc1': im_2, '2nh':im_2,'1cr': im_2, '2':im_2, \
            '112': im_2, '2xd': im_2.resize((800,300)),'ad1': im_2, '2':im_2,'1': im_2, '2':im_2,'1': im_2, '2zfe':im_2,'1125': im_2.resize((800,300)), '2':im_2, \
            '1': im_2, '2a': im_2,'1': im_2, '31':im_2,'11': im_2, '434':im_2,'1': im_2, '2':im_2.resize((800,300)),'1': im_2, '2':im_2,}
    # imgs = [im_2.resize((730,400)), im_3, im_3, im_2.resize((800,300)), im_2, im_3, im_3.resize((450,300)), im_2.resize((750,295)), \
    #         im_2, im_3, im_2, im_2, im_2.resize((500,600)), im_2,im_2,im_2,im_3,im_2, im_2, im_2, im_3, \
    #         im_2.resize((700, 600)), im_3, im_3, im_2, im_3, im_2, im_2, im_2]
    print(paste_by_size(out_size, imgs))


def test():
    paste_by_size_test()

if __name__ == '__main__':
    test()