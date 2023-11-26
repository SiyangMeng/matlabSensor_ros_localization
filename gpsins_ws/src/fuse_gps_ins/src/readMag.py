# -*- coding: UTF-8 -*-
#!/usr/bin/env python

import rospy
import csv
from sensor_msgs.msg import MagneticField
from std_msgs.msg import Header

def read_mag_data(file_path):
    mag_data = []
    with open(file_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            mag_data.append(row)
    return mag_data

def mag_publisher():
    rospy.init_node('mag_publisher', anonymous=True)
    mag_pub = rospy.Publisher('/mag/data', MagneticField, queue_size=10)
    rate = rospy.Rate(100)  # 调整发布速率

    # 从CSV文件中加载数据
    mag_data = read_mag_data('/home/msy/Documents/matlabSensor_ros_localization/data/mag.csv')

    # 遍历数据并发布 MagneticField 消息
    for mag_row in mag_data:
        # 创建 MagneticField 消息
        mag_msg = MagneticField()
        mag_msg.header = Header(stamp=rospy.Time(int(mag_row[0]), int(mag_row[1])), frame_id='base_link')

        # 设置磁场强度
        mag_msg.magnetic_field.x = float(mag_row[2])
        mag_msg.magnetic_field.y = float(mag_row[3])
        mag_msg.magnetic_field.z = float(mag_row[4])

        # Publish MagneticField message
        mag_pub.publish(mag_msg)

        # Sleep to control the publishing rate
        rate.sleep()

if __name__ == '__main__':
    try:
        mag_publisher()
    except rospy.ROSInterruptException:
        pass
