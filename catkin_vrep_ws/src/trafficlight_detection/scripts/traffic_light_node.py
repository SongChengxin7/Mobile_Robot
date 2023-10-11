#!/usr/bin/env python
# -*- coding: UTF-8 -*-

 
import rospy
import cv2
import numpy as np
import math
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Bool, Float64
from geometry_msgs.msg import PoseStamped
#from sensor_msgs.msg import Image, CompressedImage
 
cnt = 0

class TrafficLightNode():
    def __init__(self):
        rospy.init_node("traffic_light_node", anonymous=False )
        rospy.on_shutdown(self.shutdown)


        # 参数配置
        # 信号灯检测开启标识符，默认为开启
        self.detect_flag = rospy.get_param("~detect_flag", True)
        if self.detect_flag:
            rospy.loginfo("Detection flag: ON")
        else:
            rospy.loginfo("Detection flag: OFF")

        # 信号灯颜色类型，默认False为红色
        self.traffic_light_type = rospy.get_param("~traffic_light_type", True)
        rospy.loginfo(self.traffic_light_type)  # 打印信号灯类型

        # 有效点数量，默认为50
        self.min_point_count = rospy.get_param("~min_point_count", 50)
        ## 信号灯截取参数
        # self.crop_norm = rospy.get_param("~crop_norm")
        # 霍夫圆检测参数设置
        self.dp = rospy.get_param("~dp", 5)
        self.minDist = rospy.get_param("~minDist", 20)
        self.param1 = rospy.get_param("~param1", 200)
        self.param2 = rospy.get_param("~param2", 10)
        self.minRadius = rospy.get_param("~minRadius", 0)
        self.maxRadius = rospy.get_param("~maxRadius", 0)

        # 开启信号灯检测模式
        if self.detect_flag:
            rospy.loginfo("Start detect!")
            rospy.loginfo(str(self.traffic_light_type))  # 打印信号灯类型

            rate = rospy.Rate(1)
            while not rospy.is_shutdown():
                # 打印信号灯类型
                if not self.traffic_light_type:
                    rospy.loginfo("Light type is RED!")
                else:
                    rospy.loginfo("Light type is GREEN!")
                
                # 计数实现信号灯变换
                global cnt
                if  cnt < 20:
                    self.traffic_light_type = False
                    # rospy.set_param("~traffic_light_type", False)
                    cnt += 1
                else:
                    self.traffic_light_type = True
                    # rospy.set_param("~traffic_light_type", True)
                    cnt += 1
                    if cnt > 40:
                        cnt = 0
                print(cnt)

                # 加载信号灯图片
                if not self.traffic_light_type:
                    image = cv2.imread("/home/scx/catkin_vrep_ws/src/trafficlight_detection/pic/redCircle.png")
                    rospy.loginfo("RED_CIRCLE Loading In!")
                else:
                    image = cv2.imread("/home/scx/catkin_vrep_ws/src/trafficlight_detection/pic/greenCircle.png")
                    rospy.loginfo("GREEN_CIRCLE Loading In!")
                
                #发布信号灯类型话题
                self.pub_light_info = rospy.Publisher("~light_State", Bool, queue_size=10)
                print("LIGHT state is published!")
                #检测信号灯
                self.detect_image(image)

                rate.sleep()


    def detect_image(self, img):
        result = self.detect_circle(img)
        if result > 0:
            self.pub_light_info.publish(Bool(data=False))  # False->红灯
            rospy.logwarn("RED LIGHT!")
        elif result < 0:
            self.pub_light_info.publish(Bool(data=True))  # True->绿灯
            rospy.logwarn("GREEN LIGHT!")
        else:
            rospy.logwarn("reslut = 0!")


    # 检测圆形
    def detect_circle(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, self.dp, self.minDist, param1=self.param1, param2=self.param2, minRadius=self.minRadius, maxRadius=self.maxRadius)   #霍夫圆检测
        result = []
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for circle in circles[0,:]:
                if circle[0] < circle[2]: 
                    circle[0] = circle[2]
                if circle[1] < circle[2]:
                    circle[1] = circle[2]
                roi = img[(circle[1]-circle[2]):(circle[1]+circle[2]),(circle[0]-circle[2]):(circle[0]+circle[2])]  # 圆形区域
                cv2.imshow("111", roi)
                cv2.waitKey()
                color = self.detect_color(roi)
                result.append(color)
            return np.sum(result)
        else:
            return 0        


    # 检测颜色
    def detect_color(self, img_roi):
        hsv_img = cv2.cvtColor(img_roi, cv2.COLOR_BGR2HSV)
        red_min1 = np.array([0,43,46])
        red_max1 = np.array([10,255,255])
        red_min2 = np.array([156,43,46])
        red_max2 = np.array([180,255,255])
        green_min = np.array([35,43,46])
        green_max = np.array([77,255,255])
        red_thresh = cv2.inRange(hsv_img, red_min1, red_max1)+cv2.inRange(hsv_img, red_min2, red_max2)
        green_thresh = cv2.inRange(hsv_img, green_min, green_max)
        # 进行中值滤波
        red_blur = cv2.medianBlur(red_thresh,5)
        green_blur = cv2.medianBlur(green_thresh,5)
        # 计算红色和绿色的点的数量
        red = cv2.countNonZero(red_blur)
        green = cv2.countNonZero(green_blur)
        lightColor = max(red, green)
        # 有效颜色点是否超出设定阈值，去除细小（不为信号灯）的相同颜色区域
        if lightColor > self.min_point_count:
            if lightColor == red:
                # 红色为正值
                return 1
            elif lightColor == green:
                # 绿色为负值
                return -1
        else:
            return 0
 
     # 退出函数
    def shutdown(self):
        rospy.logwarn("Stopping the detecting!")


if __name__=="__main__":
    try:
        TrafficLightNode()  # 调用TrafficLightNode类 
        rospy.spin()  # 循环节点
    except rospy.ROSInterruptException:
        rospy.logwarn("Traffic lights detection exception finished!")