#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist

rospy.init_node('move_robot')
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=20)
rate = rospy.Rate(20)
move=Twist()
move.linear.x=2
move.angular.z=0
#distance = 1
current_distance = 0

PI = 3.14
rotate=Twist()
rotate.linear.x=0
rotate.angular.z=0.5
current_angle=0
'''while not rospy.is_shutdown():
    pub.publish(move)
    rate.sleep()'''
while not rospy.is_shutdown():
    i=0
    while i<4:
        #pub.publish(move)
        #rate.sleep()
        #current_distance = 0
        t0 = rospy.Time.now().to_sec()
        while current_distance<1:
            pub.publish(move)
            t1 = rospy.Time.now().to_sec()
            current_distance = move.linear.x *(t1-t0)
            #rate.sleep()

        move.linear.x=0
        pub.publish(move)
        #rate.sleep()
    
        t2 = rospy.Time.now().to_sec()
        while current_angle<= PI/4:
            pub.publish(rotate)
            t3 = rospy.Time.now().to_sec()
            current_angle = rotate.angular.z *(t3-t2)
            #rate.sleep()
    
        rotate.angular.z=0
        pub.publish(rotate)
        #rate.sleep()
        i +=1
    
