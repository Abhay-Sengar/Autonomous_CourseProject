#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist

print("started")
rospy.init_node('move_turtlebot', anonymous=True)
velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
vel_msg = Twist()

# Set the target position
target_x = 10
target_y = 10
target_z = 0

# Proportional control constants
linear_velocity_x = 1
linear_velocity_y = 1
linear_velocity_z = 0

t1 = rospy.Time.now().to_sec()
print(t1)
# Rate at which to publish velocity commands
rate = rospy.Rate(10)

while not rospy.is_shutdown():
	# Calculate errors
	#error_x = target_x - current_x  # You'll need to replace current_x, current_y, and current_z with actual values
	#error_y = target_y - current_y
	#error_z = target_z - current_z

	# Set velocity commands
	vel_msg.linear.x = linear_velocity_x
	vel_msg.linear.y = linear_velocity_y
	vel_msg.angular.z = linear_velocity_z
	
	t2 = rospy.Time.now().to_sec() 
	#print(t2)
	# Publish the velocity commands
	velocity_publisher.publish(vel_msg)

	# Check if the TurtleBot has reached the target position
	#if abs(error_x) < 0.1 and abs(error_y) < 0.1 and abs(error_z) < 0.1:
	print(linear_velocity_x * (t2-t1), linear_velocity_y*(t2-t1))
	if linear_velocity_x * (t2-t1) == target_x and linear_velocity_y*(t2-t1) == target_y:
	    rospy.loginfo("TurtleBot reached the target position!")
	    vel_msg.linear.x = 0
	    vel_msg.linear.y = 0
	    vel_msg.angular.z = 0
	
	# Publish the velocity commands
	    velocity_publisher.publish(vel_msg)
	    break

	rate.sleep()

#if __name__ == '__main__':
 #   try:
  #  	print("engine_starting)
   #     move_turtlebot(5, 5, 0)  # Specify your target x, y, z position here
    #except rospy.ROSInterruptException:
     #   pass