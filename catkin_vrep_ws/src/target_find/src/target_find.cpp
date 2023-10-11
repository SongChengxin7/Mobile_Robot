#include "ros/ros.h"
#include "nav_msgs/OccupancyGrid.h"
#include "geometry_msgs/PoseStamped.h"
#include "visualization_msgs/Marker.h"



int cell2id(int cell_x, int cell_y, int cell_height)
{
    return cell_x + cell_y * cell_height;
}



std::vector<geometry_msgs::Point> findTarget(nav_msgs::OccupancyGrid& msg)
{
    std::vector<geometry_msgs::Point> pts;
    geometry_msgs::Point fist_pt;
    const float ori_x = msg.info.origin.position.x;
    const float ori_y = msg.info.origin.position.x;
    const int cell_height = msg.info.width;
    const int cell_width = msg.info.height;
    const float resolution = msg.info.resolution;
    const int delta_add = 1;
    // find first left pt
    int cell_init_x = (int)(-ori_x/resolution);
    int cell_init_y = (int)(-ori_y/resolution);
    int id = cell2id(cell_init_x, cell_init_y, cell_height);
    int delta = delta_add;

    std::vector<bool> found;
    found.resize(cell_height*cell_width, false);
    while (true)
    {
        if ( (msg.data.at(id + delta) == -1 &&
             msg.data.at(id + delta + 4) == -1 &&
                msg.data.at(id + delta + 8) == -1 )
        || (cell_init_y+delta_add) > cell_width)
        {
            fist_pt.x = (float)(cell_init_x + delta) * resolution + ori_x;
            fist_pt.y = (float)(cell_init_y) * resolution + ori_y;
            fist_pt.z = 0;
            pts.emplace_back(fist_pt);
            //found.at(id + delta*cell_height) = true;
            break;
        }
        delta += delta_add;
    }
    geometry_msgs::Point pt;
    pt.x = (float)cell_height*resolution + ori_x - 0.2;
    pt.y = fist_pt.y;
    pt.z = fist_pt.z;
    pts.emplace_back(pt);
    // find last pt
    const int search_index_x[32] = {-4, -4, -4, -4, -4, -3, -2, -1,  0,  1,  2,  3,  4,  4,  4,  4,  4,  4,  4,  4,  4, 3, 2, 1, 0, -1, -2, -3, -4, -4, -4, -4};
    const int search_index_y[32] = { 0, -1, -2, -3, -4, -4, -4, -4, -4, -4, -4, -4, -4, -3, -2, -1,  0,  1,  2,  3,  4, 4, 4, 4, 4,  4,  4,  4,  4,  3,  2,  1};

    int last_cell_x = cell_init_x, last_cell_y = cell_init_y + delta;
    int last_search_id = 10;
    bool find = false;

    /*
    while (!find)
    {
        geometry_msgs::Point pt;
        bool find_next = false;
        // find next x y
        for (int i = 1;i < 28; i++)
        {
            int search_id = (last_search_id + i) % 32;

            int cur_id = cell2id(last_cell_x + search_index_x[search_id],
                                 last_cell_y + search_index_y[search_id],
                                 cell_height);
            if (found.at(cur_id))
                continue;

            int new_cell_x = last_cell_x + search_index_x[search_id];
            int new_cell_y = last_cell_y + search_index_y[search_id];
            pt.x = (float)new_cell_x * resolution + ori_x;
            pt.y = (float)new_cell_y * resolution + ori_y;
            pt.z = 0;

            if(msg.data.at(cur_id) == 100)
            {

                last_search_id = (search_id + 24) % 32;
                last_cell_x = new_cell_x;
                last_cell_y = new_cell_y;

                for(int dx=-1;dx<=1;dx++)
                {
                    for (int dy=-1;dy<=1;dy++)
                    {
                        found.at(cur_id + dx + dy * cell_height) = true;
                    }
                }

                find_next = true;
                break;
            }
        }
        if(!find_next)
        {
            static int rand = 0;
            bool un_find = false;
            for (int iter = 0; iter < 5; iter ++)
            {
                int k = (int)(0.8f * (float)(iter + 1));
                for (int i = 0; i < 32;i ++)
                {
                    int search_id = (last_search_id + 8 + i)%32;
                    int cur_id = cell2id(last_cell_x + search_index_x[search_id]*k,
                                         last_cell_y + search_index_y[search_id]*k,
                                         cell_height);
                    if(msg.data.at(cur_id) == -1)
                    {
                        pt.x = (float)(last_cell_x + search_index_x[search_id]*k) * resolution + ori_x;
                        pt.y = (float)(last_cell_y + search_index_y[search_id]*k) * resolution + ori_y;
                        pt.z = 0;
                        un_find = true;
                        break;
                    }
                }
            }

            if (!un_find)
            {
                int search_id = (last_search_id + 8 + rand)%32;
                pt.x = (float)(last_cell_x + search_index_x[search_id]*4) * resolution + ori_x;
                pt.y = (float)(last_cell_y + search_index_y[search_id]*4) * resolution + ori_y;
                pt.z = 0;
            }
            rand ++;
            if (rand > 3200000)
                rand = 0;
            find = true;
        }
        pts.emplace_back(pt);
        if(pts.size() > 500)
        {
            break;
        }
    }
     */
    return pts;
}

ros::Publisher publisher;
ros::Publisher visualization_publisher;
void mapCallback(nav_msgs::OccupancyGrid msg)
{
    geometry_msgs::PoseStamped target;
    visualization_msgs::Marker marker;
    marker.header.frame_id = "map";
    marker.id = 0;
    marker.header.stamp = ros::Time::now();
    marker.ns = "target";
    marker.type = visualization_msgs::Marker::CUBE_LIST;
    marker.action = visualization_msgs::Marker::ADD;
    marker.color.a = 1;marker.color.r = 0;marker.color.g = 1;marker.color.b = 0;
    marker.pose.orientation.x=0;marker.pose.orientation.y=0;marker.pose.orientation.z=0;marker.pose.orientation.w=1;
    marker.scale.x=0.2;marker.scale.y=0.2;marker.scale.z=0.2;

    auto points = findTarget(msg);
    target.header.frame_id = "map";
    target.header.stamp = ros::Time::now();
    target.pose.position.x = (points.end() - 1)->x;
    target.pose.position.y = (points.end() - 1)->y;
    target.pose.position.z = (points.end() - 1)->z;
    target.pose.orientation.w = 1;
    // pub target
    for (auto& pt:points)
        marker.points.push_back(pt);
    visualization_publisher.publish(marker);
    publisher.publish(target);
}
    
int main(int argc, char** argv)
{
    //初始化ROS节点
	ros::init(argc, argv, "target_find");									
    ros::NodeHandle nh;

    publisher = nh.advertise<geometry_msgs::PoseStamped>("/move_base_simple/goal", 1000);
    visualization_publisher = nh.advertise<visualization_msgs::Marker>("target", 10);
    ros::Subscriber sub = nh.subscribe("map", 1, mapCallback);
    //循环运行
    ros::Rate loop_rate(50);
	while (ros::ok()) 
    {
		ros::spinOnce();
		loop_rate.sleep();
	}
	return 0;
}

