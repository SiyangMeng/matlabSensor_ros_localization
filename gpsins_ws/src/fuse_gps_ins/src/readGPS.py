# -*- coding: UTF-8 -*-
#!/usr/bin/env python

import rospy
import tf
import csv
from sensor_msgs.msg import NavSatFix
from geometry_msgs.msg import TwistWithCovarianceStamped, PoseWithCovarianceStamped,Twist, Pose,Quaternion
from std_msgs.msg import Header

def read_gps_data(file_path):
    gps_data = []
    with open(file_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            gps_data.append(row)
    return gps_data

def gps_publisher():
    rospy.init_node('gps_publisher', anonymous=True)
    gps_fix_pub = rospy.Publisher('/gps/fix', NavSatFix, queue_size=10)
    gps_twist_pub = rospy.Publisher('/gps/twist', TwistWithCovarianceStamped, queue_size=10)
    gps_pose_pub = rospy.Publisher('/gps/pose', PoseWithCovarianceStamped, queue_size=10)
    rate = rospy.Rate(1)  # 调整发布速率

    # 从CSV文件中加载数据
    gps_data = read_gps_data('/home/msy/Documents/matlabSensor_ros_localization/data/pos.csv')

    # 遍历数据并发布 NavSatFix 和 TwistWithCovarianceStamped 消息
    for gps_row in gps_data:
        # 创建 NavSatFix 消息
        gps_fix_msg = NavSatFix()
        gps_fix_msg.header = Header(stamp=rospy.Time(int(gps_row[0]), int(0)), frame_id='gps_frame')

        # 设置位置信息
        gps_fix_msg.latitude = float(gps_row[2])
        gps_fix_msg.longitude = float(gps_row[3])
        gps_fix_msg.altitude = float(gps_row[4])

        # 设置水平精度
        gps_fix_msg.position_covariance[0] = float(gps_row[7]) ** 2
        gps_fix_msg.position_covariance[4] = float(gps_row[7]) ** 2

        # Publish NavSatFix message
        gps_fix_pub.publish(gps_fix_msg)

        # 创建 TwistWithCovarianceStamped 消息
        gps_twist_msg = TwistWithCovarianceStamped()
        gps_twist_msg.header = Header(stamp=rospy.Time(int(gps_row[0]), int(0)), frame_id='gps_frame')

        # gps_twist_msg.header = Header(stamp=rospy.Time(int(gps_row[0]), int(gps_row[1])), frame_id='gps_frame')

        # 创建 Twist 消息
        gps_twist = Twist()
        gps_twist.linear.x = float(gps_row[5])  # 速度
        # 设置协方差矩阵
        gps_twist_msg.twist.covariance[0] = float(gps_row[7]) ** 2  # 水平速度的方差
        gps_twist_msg.twist.covariance[6] = 0.3*float(gps_row[7]) ** 2  # 水平速度的方差
        
        # Publish TwistWithCovarianceStamped message
        gps_twist_pub.publish(gps_twist_msg)


        gps_pose_msg = PoseWithCovarianceStamped()
        gps_pose_msg.header = Header(stamp=rospy.Time(int(gps_row[0]), int(0)), frame_id='gps_frame')
        course = float(gps_row[6])# 航向角
        quaternion = tf.transformations.quaternion_from_euler(0, 0, course)
        # 创建 geometry_msgs/Quaternion 对象
        gps_pose_msg.orientation = Quaternion(x=quaternion[0], y=quaternion[1], z=quaternion[2], w=quaternion[3])
        gps_pose_msg.orientation.covariance[35] = (float(gps_row[7])/float(gps_row[5])/57.3) ** 2  # 航向角速度的方差
        # Publish TwistWithCovarianceStamped message
        gps_pose_pub.publish(gps_pose_msg)

        # Sleep to control the publishing rate
        rate.sleep()

if __name__ == '__main__':
    try:
        gps_publisher()
    except rospy.ROSInterruptException:
        pass
