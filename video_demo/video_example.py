# coding=utf-8
"""
Created on 上午10:18 17-7-27

@author: zyl
"""
import cv2

video_path = "b.mp4"
video_output_path = "b_output.avi"

# 初始化视频读取的方法
videoCapture = cv2.VideoCapture(video_path)
# 读取视频的帧速率 和 帧大小
fps = videoCapture.get(cv2.CAP_PROP_FPS)
size = (int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))

# 写入视频 需要设置 视频的帧和大小
videoWriter = cv2.VideoWriter(
    video_output_path, cv2.VideoWriter_fourcc('P', 'I', 'M', '1'),
    fps, size
    )

# 按帧读取
# frame： 矩阵数据
sucess, frame = videoCapture.read()
num = 0
while sucess:
    # print("sucess:{sucess}, frame: {frame}".format(sucess=sucess, frame=frame))
    cv2.imwrite('./images/%d.png'%num, frame)
    num += 1
    videoWriter.write(frame)  # 将每一帧图像写入文件
    # cv2.imshow('test', frame)

    sucess, frame = videoCapture.read()

