#! /usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
import sensor_msgs.msg 
from geometry_msgs.msg import Twist


pub = rospy.Publisher('/cmd_vel', Twist)
#pub = rospy.Publisher('/revised_scan', LaserScan, queue_size = 10)
scann = LaserScan()
move = Twist()

def callback(msg):
    #print(len(msg.ranges)) len is 2019 from 0-360
    current_time = rospy.Time.now()
    scann.header.stamp = current_time
    scann.header.frame_id = 'laser'
    scann.angle_min = -3.1415
    scann.angle_max = 3.1415
    scann.angle_increment = 0.00311202858575
    scann.time_increment = 4.99999987369e-05
    scann.range_min = 0.00999999977648
    scann.range_max = 32.0
    scann.ranges = msg.ranges[0:360]
    scann.intensities = msg.intensities[0:72]
    print(scann)
    #print(scann.ranges[0])
    #pub.publish(scann)
    #move.linear.x = 0.5
    move.angular.z = 0.0
    #pub.publish(move)
    for i in scann.ranges:
        #print(i)
        if i > 1:
            move.linear.x = 0.5
            move.angular.z = 0.0
            print("hello")
            
        else :
            move.linear.x = 0.0
            move.angular.z = 0.0
    pub.publish(move)
    


def listener():
    #pub.publish(move)
    rospy.init_node('revised_scan', anonymous=True)
    #sub = rospy.Subscriber('/scan', LaserScan, callback)
    pub = rospy.Publisher('/cmd_vel', Twist)
    move = Twist()
    rospy.spin()

if __name__ == '__main__':
    listener()

#If the distance to an obstacle in front of the robot is smaller than 1 meter, the robot will stop

