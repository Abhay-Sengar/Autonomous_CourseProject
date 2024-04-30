#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist

rospy.init_node('move_robot')
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
rate = rospy.Rate(2)
move=Twist()
#move.linear.x=1   initial values
#move.angular.z=0.5

#move.linear.x=0.5   almost correct values
#move.angular.z = 0.3

move.linear.x=0.5
move.angular.z = 0.5

while not rospy.is_shutdown():
    pub.publish(move)
    rate.sleep()