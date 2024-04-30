#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
 
def straight():
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.init_node('move_robot')
    rate = rospy.Rate(10) # 10hz
    move=Twist()
    move.linear.x=0.5
    #move.linear.y=0
    #move.linear.z=0
    #move.angular.x=0
    #move.angular.y=0
    move.angular.z=0
    current_distance=0

    while not rospy.is_shutdown():
        t0 = rospy.Time.now().to_sec()
        while current_distance<1:
            pub.publish(move)
            t1 = rospy.Time.now().to_sec()
            current_distance = move.linear.x *(t1-t0)
            rate.sleep()

        move.linear.x=0
        pub.publish(move)
        rate.sleep()
        
        
        
if __name__ == '__main__':
    try:
        straight()
    except rospy.ROSInterruptException:
        pass
