#!/usr/bin/env python
# -*- coding: UTF-8 -*-
 
###################################################################################
# 在地图上指定6个坐标点作为巡逻点,可以在这些点之间进行不断的巡逻,也可以指定巡逻的圈数,
# 当到达指定的圈数后就会停止运行.该patrol_nav_node,是通过向MoveBaseGoal的
# target_pose中发布目标位姿来达到巡航的目的,根据move_base的action状态来判断机器人是否到达了目标位置.
# 当到达了目标位置后取出下一个目标位姿进行导航.直到字典存储的所有目标位姿都到达后,就认为巡航一圈结束了.


import rospy
import random
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
 
class PatrolNav():
 
    def __init__(self):
        rospy.init_node('patrol_nav_node', anonymous=False)
        rospy.on_shutdown(self.shutdown)
 
        # From launch file get parameters
        self.rest_time     = rospy.get_param("~rest_time", 5)
        self.keep_patrol   = rospy.get_param("~keep_patrol",   False)
        self.random_patrol = rospy.get_param("~random_patrol", False)
        self.patrol_type   = rospy.get_param("~patrol_type", 0)
        self.patrol_loop   = rospy.get_param("~patrol_loop", 2)
        self.patrol_time   = rospy.get_param("~patrol_time", 10)
 
        #set all navigation target pose
        self.locations = dict()
        self.locations["point 1"] = Pose(Point(1.9702, -0.1436, 0.0000), Quaternion(0.0000, 0.0000, -0.6996, 0.7145))
        self.locations["point 2"] = Pose(Point(4.4388, -1.1878, 0.0000), Quaternion(0.0000, 0.0000, -0.1684,  0.9879))
        self.locations["point 3"] = Pose(Point(7.7530, -0.0289, 0.0000), Quaternion(0.0000, 0.0000, -0.3859, 0.9226))
        self.locations["point 4"] = Pose(Point(8.8368, -2.6860, 0.0000), Quaternion(0.0000, 0.0000, 0.9913, -0.1316))
        self.locations["point 5"] = Pose(Point(4.1289, -3.7512, 0.0000), Quaternion(0.0000, 0.0000, 0.8281, 0.5606))
        self.locations["point 6"] = Pose(Point(0.8853, -2.9089, 0.0000), Quaternion(0.0000, 0.0000, 0.9778, 0.2099))
 
        # Goal state return values
        goal_states = ['PENDING', 'ACTIVE', 'PREEMPTED', 'SUCCEEDED', 'ABORTED',
                       'REJECTED', 'PREEMPTING', 'RECALLING', 'RECALLED', 'LOST']
 
        # 订阅move_base服务
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)  # 获取move_base在导航过程中的状态反馈，根据反馈的状态来决定何时发送下一个目标点的坐标
        rospy.loginfo("Waiting for move_base action server...")
        self.move_base.wait_for_server(rospy.Duration(30)) # 等待30秒
        rospy.loginfo("Connected to move base server!")
 
        loop_cnt = 0
        n_goals  = 0
        n_successes  = 0
        target_num   = 0
        running_time = 0
        location   = ""
        locations_cnt = len(self.locations)
        sequeue = ["point 1", "point 2", "point 3", "point 4","point 5","point 6"]
 
        rospy.loginfo("Starting position navigation!")
        start_time = rospy.Time.now()

        while not rospy.is_shutdown():
            if self.keep_patrol == False:
                if self.patrol_type == 0:
                    if target_num == locations_cnt :
                      if loop_cnt < self.patrol_loop-1:
                        target_num = 0
                        loop_cnt  += 1
                        rospy.logwarn("Left patrol loop cnt: %d", self.patrol_loop-loop_cnt)
                      else:
                        rospy.logwarn("Patrol loop over, back to the original position...")
                        self.send_goal("point 1")                        
                        rospy.signal_shutdown('Quit')
                        break
            else:
                if self.random_patrol == False:
                    if target_num == locations_cnt:
                        target_num = 0
                else:
                    target_num = random.randint(0, locations_cnt-1)
 
            location = sequeue[target_num]
            rospy.loginfo("Going to: " + str(location))
            self.send_goal(location)
            print("The robot is running to the target location...")
 
            target_num += 1
            n_goals    += 1
 
            finished_within_time = self.move_base.wait_for_result(rospy.Duration(600))
            if not finished_within_time:
                self.move_base.cancel_goal()
                rospy.logwarn("WARN:Timed out achieving goal")
            else:
                state = self.move_base.get_state()
                if state == GoalStatus.SUCCEEDED:
                    n_successes += 1
                    rospy.loginfo("Goal succeeded!")
                else:
                    rospy.logerr("Goal failed with error code:"+str(goal_states[state]))
 
            running_time = rospy.Time.now() - start_time
            running_time = running_time.secs/60.0
 
            rospy.loginfo("Success: " + str(n_successes) + "/" +
                          str(n_goals) + " = " +
                          str(100 * n_successes/n_goals) + "%")
            rospy.loginfo("Running time: " + str(self.trunc(running_time, 1)) + " min")
            rospy.sleep(self.rest_time)
 
            if self.keep_patrol == False and self.patrol_type == 1: #use patrol_time
                if running_time >= self.patrol_time:
                    rospy.logwarn("Now reach patrol_time, back to original position...")
                    self.send_goal("point 1")
                    rospy.signal_shutdown('Quit')
 
    def send_goal(self, locate):
        self.goal = MoveBaseGoal()
        self.goal.target_pose.pose = self.locations[locate]
        self.goal.target_pose.header.frame_id = 'map'
        self.goal.target_pose.header.stamp = rospy.Time.now()
        self.move_base.send_goal(self.goal) #send goal to move_base
 
    def trunc(self, f, n):
        # Truncates/pads a float f to n decimal places without rounding
        slen = len('%.*f' % (n, f))
        return float(str(f)[:slen])
 
    def shutdown(self):
        rospy.logwarn("Stopping the patrol...")
 
if __name__ == '__main__':
    try:
        PatrolNav()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.logwarn("patrol navigation exception finished.")
