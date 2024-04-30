#!/usr/bin/python3
import rospy
from geometry_msgs.msg import Twist

# Starts a new node
rospy.init_node('robot_cleaner', anonymous=True)
velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
rate=rospy.Rate(2)
vel_msg = Twist()
vel_msg.linear.x = 20
vel_msg.angular.z = 0

while not rospy.is_shutdown():
    velocity_publisher.publish(vel_msg)
    rate.sleep()

