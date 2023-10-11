#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 在地图上指定6个坐标点作为巡逻点，可以在这些点之间进行不断的巡逻，也可以指定巡逻的圈数，当到达
# 指定的圈数后就会停止运行。该patrol_nav_node，是通过向MoveBaseGoal的target_pose中发布目标位
# 姿来达到巡航的目的，根据move_base的action状态来判断机器人是否到达了目标位置。当到达了目标位
# 置后取出下一个目标位姿进行导航。直到字典存储的所有目标位姿都到达后,就认为巡航一圈结束了。

# 导入库
import rospy
import random
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion, Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_msgs.msg import Bool, Float64

target_num = 0
sequeue = []
traffic_light_state_flag = 1
cancel_goal_flag = 1
buffer_goal_flag = 1
buffer_goal_num = 1

class PatrolNav():

    def __init__(self):
        # 初始化节点
        rospy.init_node("patrol_nav_node", anonymous=False)
        rospy.on_shutdown(self.shutdown)


        # 配置各个属性默认值
        self.rest_time     = rospy.get_param("~rest_time", 5)  # 到达目标点后原地等待时间
        self.keep_patrol   = rospy.get_param("~keep_patrol",   False)  # 有限导航/无限巡航
        self.random_patrol = rospy.get_param("~random_patrol", False)  # 随机导航/顺序巡航
        self.patrol_type   = rospy.get_param("~patrol_type", False)  # 巡航模式
        self.patrol_loop   = rospy.get_param("~patrol_loop", 2)   # 巡航次数
        self.patrol_time   = rospy.get_param("~patrol_time", 10)  # 巡航限定时长

        # 定义巡航点
        self.locations = dict()
        self.locations["point 1"] = Pose(Point(1.9702, -0.1436, 0.0000), Quaternion(0.0000, 0.0000, -0.6996, 0.7145))
        self.locations["point 2"] = Pose(Point(4.4388, -1.1878, 0.0000), Quaternion(0.0000, 0.0000, -0.1684,  0.9879))
        self.locations["point 3"] = Pose(Point(7.7530, -0.0289, 0.0000), Quaternion(0.0000, 0.0000, -0.3859, 0.9226))
        self.locations["point 4"] = Pose(Point(8.8368, -2.6860, 0.0000), Quaternion(0.0000, 0.0000, 0.9913, -0.1316))
        self.locations["point 5"] = Pose(Point(4.1289, -3.7512, 0.0000), Quaternion(0.0000, 0.0000, 0.8281, 0.5606))
        self.locations["point 6"] = Pose(Point(0.8853, -2.9089, 0.0000), Quaternion(0.0000, 0.0000, 0.9778, 0.2099))
        self.locations["point origin"] = Pose(Point(0.0, 0.0, 0.0), Quaternion(0.0, 0.0, 0.0, 0.0))

        # 状态列表
        goal_states = ['PENDING', 'ACTIVE', 'PREEMPTED', 'SUCCEEDED', 'ABORTED',
                       'REJECTED', 'PREEMPTING', 'RECALLING', 'RECALLED', 'LOST']

        # 订阅move_base服务
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)  # 获取move_base在导航过程中的状态反馈，根据反馈的状态来决定何时发送下一个目标点的坐标
        rospy.loginfo("Waiting for move_base action server...")
        self.move_base.wait_for_server(rospy.Duration(30)) # 等待30秒
        rospy.loginfo("Connected to move base server!")

        # 初始化变量，用于打印成功率、巡航点和巡航圈数计数
        global sequeue, target_num
        loop_cnt = 0  # 圈数
        n_goals  = 0  # 巡航点个数
        n_successes  = 0  # 成功次数
        target_num   = 0  # 目标号
        running_time = 0  # 巡航运行时间
        location   = ""
        locations_cnt = len(self.locations) - 1  # 给定巡航点个数，默认为7，需要去除最后一个origin点
        sequeue = ["point 1", "point 2", "point 3", "point 4","point 5","point 6"]

        start_time = rospy.Time.now()
        rospy.loginfo("Starting patrol navigation!")
        
        # 设定ros发送消息频率，1hz
        rate = rospy.Rate(1)
        # 主循环逻辑
        while not rospy.is_shutdown():
            global traffic_light_state_flag  # traffic_light_state_flag->信号灯类型标识符，traffic_light_state_flag=1为绿灯，traffic_light_state_flag=0为红灯
            self.sub_light_info = rospy.Subscriber("/traffic_light_node/light_State", Bool, self.traffic_light_callback, queue_size=10)  # 订阅信号灯类型话题
            if traffic_light_state_flag:
                rospy.logdebug("当前信号灯类型：绿灯(" + str(traffic_light_state_flag) + ")")
            else:
                rospy.logdebug("当前信号灯类型：红灯(" + str(traffic_light_state_flag) + ")")
            rospy.logdebug("target_num = " + str(target_num))
            rospy.logdebug("loop_cnt = " + str(loop_cnt))

            if traffic_light_state_flag:  # 减少计算量，只有绿灯的情况下才会进入多点巡航模式，并且重新判断当前巡航模式是否改变
                # 未开启检测/绿灯，可巡航
                if not self.keep_patrol: 
                    # 有限巡航模式
                    rospy.logdebug("有限巡航模式")
                    if not self.patrol_type:
                        # 巡航进入圈数模式
                        rospy.logdebug("圈数模式")
                        if target_num == locations_cnt:
                            # 巡航点已经计数到最后一个点，需要判断是否继续下一个循环
                            rospy.logdebug("到达最后巡航点")
                            if loop_cnt < int(self.patrol_loop) - 1:  
                                # 未到达给定圈数，继续巡航
                                rospy.logdebug("loop_cnt = ", loop_cnt)
                                rospy.logdebug(self.patrol_loop-1)
                                target_num = 0  # 开始新一轮循环
                                loop_cnt  += 1  # 巡航圈数计数+1
                                rospy.loginfo("Left patrol loop cnt: %d", self.patrol_loop-loop_cnt)  # 输出剩余巡航圈数
                            else:
                                # 到达给定循环圈数，停止巡航，返回出发点
                                rospy.loginfo("PATROL OVER!")
                                self.send_goal("point origin")  # 回到初始点
                                rospy.signal_shutdown("Quit")
                                break
                else:
                    if not self.random_patrol:  # 无限巡航
                        if target_num == locations_cnt:
                            target_num = 0
                    else:
                        target_num = random.randint(0, locations_cnt-1)  # 随机目标点巡航

                rospy.logdebug("当前缓存目标点：" + str(sequeue[target_num]))
                # 取出坐标点向move_base发送
                location = sequeue[target_num]
                rospy.loginfo("---------------------------")
                rospy.loginfo("Now going to: " + str(location))
                self.send_goal(location)  # send_goal发送当前坐标点
                rospy.loginfo("The robot is running to the goal location...")


                # test_new
                finished_within_time = self.move_base.wait_for_result(rospy.Duration(600))
                if not finished_within_time:
                    self.move_base.cancel_goal()
                    rospy.logwarn("WARN:Timed out achieving goal")
                else:
                    state = self.move_base.get_state()
                    if state == GoalStatus.SUCCEEDED:
                        rospy.loginfo("Target navigation successful!")
                        n_successes += 1  # 导航成功次数计数
                        target_num += 1
                        n_goals += 1
                        self.cal_info(start_time, n_successes, n_goals)
                        rospy.loginfo("停留巡查...")
                        rospy.sleep(self.rest_time)  # 到达巡航点之后原地停留默认时长.
                        rospy.loginfo("继续导航!")
                    else:
                        rospy.logwarn("Goal failed with error code:"+str(goal_states[state]))


                # self.move_base.wait_for_result()  # 等待move_base的反馈
                # state = self.move_base.get_state()
                # if state == GoalStatus.SUCCEEDED:
                #     rospy.loginfo("Target navigation successful!")
                #     n_successes += 1  # 导航成功次数计数
                #     target_num += 1
                #     n_goals += 1
                #     self.cal_info(start_time, n_successes, n_goals)
                #     rospy.loginfo("停留巡查...")
                #     rospy.sleep(self.rest_time)  # 到达巡航点之后原地停留默认时长.
                #     rospy.loginfo("继续导航!")

                if (not self.keep_patrol) and self.patrol_type: # 有限巡航 & 时间模式
                    if running_time >= self.patrol_time:
                        rospy.loginfo("Now reach patrol_time, back to original position!")
                        self.send_goal("point origin")  # 回到初始巡航点
                        rospy.signal_shutdown("Quit")
            else:
                # 红灯，停车
                print("********")
                print("红灯!")
                print("********")
            
            rate.sleep()


    # 信号灯识别检测
    def traffic_light_callback(self, msg):
        rospy.logdebug("callback")
        global traffic_light_state_flag, cancel_goal_flag, buffer_goal_flag, buffer_goal_num
        if not msg.data:
            traffic_light_state_flag = 0 # 标识符置0, 检测到红灯
            rospy.logdebug(msg.data)
            rospy.logdebug("检测到红灯，需要停车!")
            # 通过标识符保证cancel_goal只执行一遍
            if cancel_goal_flag:
                self.move_base.cancel_goal()
                if self.move_base.get_state() == 1:
                    buffer_goal_num = sequeue[target_num]
                cancel_goal_flag = 0
                rospy.loginfo("CANCEL GOAL SUCCESSFULLY!")
                buffer_goal_flag = 1
        else:
            traffic_light_state_flag = 1
            rospy.logdebug("检测到绿灯，继续行驶!")
            rospy.logdebug(buffer_goal_num)
            if buffer_goal_flag:
                self.send_goal(buffer_goal_num)
                buffer_goal_flag = 0
            cancel_goal_flag = 1


    # 发送导航目标
    def send_goal(self, locate):
        self.goal = MoveBaseGoal()
        self.goal.target_pose.pose = self.locations[locate]  # 导航坐标点
        self.goal.target_pose.header.frame_id = "map"  # 全局坐标系名称
        self.goal.target_pose.header.stamp = rospy.Time.now()  # 当前时间戳
        self.move_base.send_goal(self.goal)  # send goal to move_base，将当前MoveBaseGoal对象中的各参数发送global_planner进行路径规划
        rospy.loginfo("Goal location is sent successfully!")

    # 计算巡航相关信息
    def cal_info(self, start_time, n_successes, n_goals):
        running_time = rospy.Time.now() - start_time  # 计算当前巡航执行的总时间
        running_time = running_time.secs/60.0  # 转换成分钟
        rospy.loginfo("Success rate: " + str(n_successes) + "/" +
                    str(n_goals) + " = " +
                    str(100 * n_successes/n_goals) + "%")  # 打印巡航成功率
        rospy.loginfo("Running time: " + str(self.trunc(running_time, 2)) + " min")  # 打印运行时间（两位小数，分钟为单位）


    # 保留n位小数
    def trunc(self, f, n):
        # Truncates/pads a float f to n decimal places without rounding
        slen = len("%.*f" % (n, f))
        return float(str(f)[:slen])

    # 退出函数
    def shutdown(self):
        self.move_base.cancel_goal()
        rospy.loginfo("Stopping the patrol!")

if __name__ == "__main__":
    try:
        PatrolNav()  # 调用PatrolNav类 
        rospy.spin()  # 循环节点
    except rospy.ROSInterruptException:
        rospy.logwarn("Patrol navigation exception finished.")