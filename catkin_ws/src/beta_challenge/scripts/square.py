#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist

rospy.init_node('move_robot')
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
rate = rospy.Rate(10)
move=Twist()

PI = 3.1415926535897
     
while not rospy.is_shutdown():   
    
    move.linear.x=0
    move.angular.z=0.07
    t2 = rospy.Time.now().to_sec()
    current_angle = 0
    while current_angle< PI/2:
        
        pub.publish(move)
        t3 = rospy.Time.now().to_sec()
        current_angle = move.angular.z *(t3-t2)
        rate.sleep()
       
    
    move.angular.z=0
    pub.publish(move)
    rate.sleep() 
    
    move.linear.x = 0.07
    move.angular.z = 0
    t0 = rospy.Time.now().to_sec()
    current_distance = 0
    while current_distance<=1:
       
        pub.publish(move)
        t1 = rospy.Time.now().to_sec()
        current_distance = move.linear.x *(t1-t0)
        rate.sleep()

    move.linear.x=0
    pub.publish(move)
    rate.sleep()
     
    
    
    
    
     
'''import rospy 
from geometry_msgs.msg import Twist

rospy.init_node('move_robot')
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
rate = rospy.Rate(2)
move=Twist()
move.linear.x=
    
import rospy
from geometry_msgs.msg import Twist

def move():
     # Starts a new node
     rospy.init_node('move_robot', anonymous=True)
     velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
     vel_msg = Twist()

     #Receiveing the user's input
     #print("Let's move your robot")
     speed = 1
     distance = 1
     #isForward = input("Foward?: ")#True or False 
  
     #Checking if the movement is forward or backwards
         vel_msg.linear.x = abs(speed)
     else:
         vel_msg.linear.x = -abs(speed)
     #Since we are moving just in x-axis
     vel_msg.linear.x = speed
     vel_msg.linear.y = 0
     vel_msg.linear.z = 0
     vel_msg.angular.x = 0
     vel_msg.angular.y = 0
     vel_msg.angular.z = 0
 
     while not rospy.is_shutdown():
 
         #Setting the current time for distance calculus
         t0 = rospy.Time.now().to_sec()
         current_distance = 0
 
         #Loop to move the turtle in an specified distance
         while(current_distance < distance):
             #Publish the velocity
             velocity_publisher.publish(vel_msg)
             #Takes actual time to velocity calculus
             t1=rospy.Time.now().to_sec()
             #Calculates distancePoseStamped
             current_distance= speed*(t1-t0)
         #After the loop, stops the robot
         vel_msg.linear.x = 0
         #Force the robot to stop
         velocity_publisher.publish(vel_msg)
 
if __name__ == '__main__':
     try:
         #Testing our function
         move()
     except rospy.ROSInterruptException: pass'''

