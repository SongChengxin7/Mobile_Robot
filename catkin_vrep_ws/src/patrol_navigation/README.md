# 需要安装的包
sudo apt-get install ros-melodic-nav*   // 导航包
sudo apt-get install ros-melodic-teb-local-planner
sudo apt-get install ros-melodic-teb-local-planner-tutorials
sudo apt-get install ros-melodic-teleop-twist-keyboard  // 键盘控制包

# 运行顺序
catkin_make
source devel/setup.bash

roscore
./ copperliasim.sh 
# 打开场景，开启仿真
roslaunch cartographer_gmapping_vrep-master gmapping_mapping.launch
#1  rosrun teleop_twist_keyboard teleop_twist_keyboard.py   // 键盘控制
#2  nav2dGoal   // 单击并拖住鼠标进行设置
#3  rosrun target_find target_find src/target_find/src/target_find.cpp  // 运行预设代码

# 多点巡航
rosrun patrol_navigation patrol_navigation_node.py

# 在多点巡航的基础上增加红绿灯识别，由于仿真中无法添加红绿灯，采用读取红绿灯图片来替代摄像头采集红绿灯数据
rosrun patrol_navigation patrol_navigation_detect.py
roslaunch trafficlight_detection detection.launch
