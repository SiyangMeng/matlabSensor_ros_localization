# -*- coding: UTF-8 -*-
#!/usr/bin/env python

import rospy
import tf
import csv
from sensor_msgs.msg import Imu
from std_msgs.msg import Header
from geometry_msgs.msg import Quaternion

def read_csv(file_path):
    data = []
    with open(file_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            data.append(row)
    return data

def imu_publisher():
    rospy.init_node('imu_publisher', anonymous=True)
    imu_pub = rospy.Publisher('/imu/data', Imu, queue_size=10)
    rate = rospy.Rate(100)  # Adjust the rate as needed

    # Load data from CSV files
    acc_data = read_csv('/home/msy/Documents/matlabSensor_ros_localization/data/acc2.csv')
    att_data = read_csv('/home/msy/Documents/matlabSensor_ros_localization/data/att.csv')
    ang_data = read_csv('/home/msy/Documents/matlabSensor_ros_localization/data/ang.csv')

    # Iterate through the data and publish Imu messages
    for acc_row, att_row, ang_row in zip(acc_data, att_data, ang_data):
        # Create Imu message
        imu_msg = Imu()
        imu_msg.header = Header(stamp=rospy.Time(int(acc_row[0]), int(acc_row[1])), frame_id='base_link')

        # Set linear acceleration
        imu_msg.linear_acceleration.x = float(acc_row[2])
        imu_msg.linear_acceleration.y = float(acc_row[3])
        imu_msg.linear_acceleration.z = float(acc_row[4])

        # Set orientation (quaternion)
        # You may need to convert Euler angles to quaternion using a library like tf
        # For simplicity, assuming you already have the quaternion data in the CSV file
        roll, pitch, yaw = float(att_row[2]), float(att_row[3]), float(att_row[4])

        # 使用 tf.transformations 中的 quaternion_from_euler 函数将欧拉角转为四元数
        quaternion = tf.transformations.quaternion_from_euler(roll/57.3, pitch/57.3, yaw/57.3)
        # 创建 geometry_msgs/Quaternion 对象
        quaternion_msg = Quaternion(x=quaternion[0], y=quaternion[1], z=quaternion[2], w=quaternion[3])

        imu_msg.orientation.x = quaternion[0]
        imu_msg.orientation.y = quaternion[1]
        imu_msg.orientation.z = quaternion[2]
        imu_msg.orientation.w = quaternion[3]

        # Set angular velocity
        imu_msg.angular_velocity.x = float(ang_row[2])
        imu_msg.angular_velocity.y = float(ang_row[3])
        imu_msg.angular_velocity.z = float(ang_row[4])

        # Publish Imu message
        imu_pub.publish(imu_msg)

        # Sleep to control the publishing rate
        rate.sleep()

if __name__ == '__main__':
    try:
        imu_publisher()
    except rospy.ROSInterruptException:
        pass
