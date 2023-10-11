#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cv2
import numpy as np

# 滑动条的回调函数，获取滑动条位置处的值
def empty(a):
    h_min = cv2.getTrackbarPos("Hue_Min","HSV_TrackBars")
    h_max = cv2.getTrackbarPos("Hue_Max", "HSV_TrackBars")
    s_min = cv2.getTrackbarPos("Sat_Min", "HSV_TrackBars")
    s_max = cv2.getTrackbarPos("Sat_Max", "HSV_TrackBars")
    v_min = cv2.getTrackbarPos("Val_Min", "HSV_TrackBars")
    v_max = cv2.getTrackbarPos("Val_Max", "HSV_TrackBars")
    print(h_min, h_max, s_min, s_max, v_min, v_max)
    return h_min, h_max, s_min, s_max, v_min, v_max

# 创建一个窗口，放置6个滑动条
cv2.namedWindow("HSV_TrackBars")
cv2.resizeWindow("HSV_TrackBars",640,200)
cv2.createTrackbar("Hue_Min","HSV_TrackBars",0,180,empty)
cv2.createTrackbar("Hue_Max","HSV_TrackBars",180,180,empty)
cv2.createTrackbar("Sat_Min","HSV_TrackBars",0,255,empty)
cv2.createTrackbar("Sat_Max","HSV_TrackBars",255,255,empty)
cv2.createTrackbar("Val_Min","HSV_TrackBars",0,255,empty)
cv2.createTrackbar("Val_Max","HSV_TrackBars",255,255,empty)

print('请选择需要识别的颜色类型：红灯(0), 绿灯(1):')
light_type = int(input())

while(1):
    # 图片路径，默认0=红灯图片，1=绿灯图片，其他为多彩圆
    if light_type == 0:
        path = ("/home/scx/catkin_vrep_ws/src/trafficlight_detection/pic/red_light.png")
    elif light_type == 1:
        path = ("/home/scx/catkin_vrep_ws/src/trafficlight_detection/pic/greenCircle.png")
    else:
        print("Input WRONG!")
    
    img = cv2.imread(path)  # 打开图片
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)  # 将RGB转换成HSV

    # 设置 HSV 阈值为指定颜色范围。
    h_min, h_max, s_min, s_max, v_min, v_max = empty(0)
    lower_HSV = np.array([h_min, s_min, v_min])
    upper_HSV = np.array([h_max, s_max, v_max])

    # 设置阈值图像中只出现指定颜色范围的物件
    mask = cv2.inRange(imgHSV, lower_HSV, upper_HSV)  # 指定颜色范围内的掩码(掩膜)
    imgResult = cv2.bitwise_and(img, img, mask = mask)  # 对原图图像进行按位与操作，保留指定颜色范围内的区域

    imgResult2BGR = cv2.cvtColor(imgResult, cv2.COLOR_HSV2BGR)
    img2gray = cv2.cvtColor(imgResult2BGR, cv2.COLOR_BGR2GRAY)  # 将掩膜得到的图像进行灰度化操作(二值化)

    imgBlur =  cv2.GaussianBlur(img2gray, (3,3), 0)  # 对灰度图进行高斯滤波操作（高斯核3x3），去噪，可以选用中值滤波等去噪方法

    cimg = cv2.cvtColor(imgBlur, cv2.COLOR_GRAY2BGR)  # 将滤波后的灰度图转换回RGB图
    circles = cv2.HoughCircles(imgBlur, cv2.HOUGH_GRADIENT, 1, 20, param1=200, param2=10, minRadius=0, maxRadius=0)  # 霍夫梯度法进行圆检测（对噪声较敏感，所以需要先滤波）
    if circles is not None:  # circles包含(x, y, radius)
        for i in circles[0, 0:1]:
            cv2.circle(cimg, (int(i[0]), int(i[1])), int(i[2]), (255, 0, 0), 2)  # 绘制圆轮廓
            cv2.circle(cimg, (int(i[0]), int(i[1])), 1, (255, 0, 0), 2)  # 绘制圆心
        print (circles[0,0])

    cv2.imshow('imgOrigin', img)
    cv2.imshow('mask', mask)
    cv2.imshow('imgResult', imgResult)
    cv2.imshow('imgBlur', cimg)
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()

