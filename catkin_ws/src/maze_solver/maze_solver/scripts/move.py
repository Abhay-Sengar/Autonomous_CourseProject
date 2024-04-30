#! /usr/bin/env

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

def callback(msg):
  # write your algorithm here


rospy.init_node('laser_move')
pub=rospy.Publisher('/cmd_vel',Twist,queue_size=1)
twist=Twist()
sub=rospy.Subscriber('/scan',LaserScan,callback)

rospy.spin()