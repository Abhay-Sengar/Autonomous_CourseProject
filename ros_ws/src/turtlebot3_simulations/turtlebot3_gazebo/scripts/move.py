#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion

rospy.init_node('move_turtlebot', anonymous=True)
print("started")

current_x = 0.0
current_y = 0.0
current_yaw = 0.0

def get_yaw_from_quaternion(quaternion):
	"""
	Convert quaternion to yaw angle (in radians)
	"""
	orientation_list = [quaternion.x, quaternion.y, quaternion.z, quaternion.w]
	roll, pitch, yaw = euler_from_quaternion(orientation_list)
	return yaw

def odom_callback(msg):
	"""
	Callback function for the odometry subscriber
	"""
	global current_x, current_y, current_yaw
	current_x = msg.pose.pose.position.x
	current_y = msg.pose.pose.position.y
	current_yaw = get_yaw_from_quaternion(msg.pose.pose.orientation)

# Subscribe to the odometry topic
rospy.Subscriber("/odom", Odometry, odom_callback)

velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
vel_msg = Twist()

coordinates = [
         (-1.692532, 1.332115),(0.842878, 1.734334),
         (-1.769300, 2.622560),(0.764455, 2.790548),
         (-1.797779, 4.651069), (0.654387, 4.125747),
        (-2.474552, 16.901815), (-0.253607, 17.065682),
         (-2.559997, 20.144867),(-0.490302, 20.307751),
         (-2.702207, 21.858159), (-0.390476, 22.053707),
        (-0.883531, 27.789717), (1.464111, 28.004511),
        (1.688054, 35.037535), (4.040378, 34.969680),
        (2.5050610,37.182738), (4.658815, 36.740781),
         (3.121913,38.628931), (5.529262, 38.560974),
         (5.687191, 44.511974), (7.954768, 44.451004),
         (9.188579, 53.373150), (11.105843, 52.792646),
         (9.615917, 57.918851), (11.569015, 57.036502),
         (9.857019, 79.209601),(11.761967, 78.837462),
         (9.656191, 87.138443), (11.654459, 87.697128),
        (9.481932, 95.392532), (11.582266, 95.313172),
         (10.733526, 101.960448), (12.961380, 102.340482),
         (20.622720, 127.246245), (22.776048, 126.951720),
         (27.717867, 140.627711), (29.739610, 139.906729),
         (29.670853, 144.925047), (31.945065, 144.757087),
         (32.515902, 151.442093), (34.727159, 150.731613),
         (32.370835, 152.173457), (33.024631, 154.281436),
         (24.021516, 155.589865), (25.139362, 157.504814),
         (18.688517, 157.150096), (18.883884, 159.391280),
         (18.395054, 160.008823), (20.339431, 159.698624),
         (19.118401, 164.118771),(21.287996, 163.489371),
     ]
path_list = []

for i in range(0, len(coordinates), 2):
	start = coordinates[i]
	end = coordinates[i + 1]
	print(f"Start: {start}, End: {end}")

	average = ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2)
	# path_list.append(average)

	# Set the target position
	target_x = average[0]
	target_y = average[1]	
	target_z = 0

	# Proportional control constants
	linear_velocity_x = 1.5
	linear_velocity_y = 1.5
	linear_velocity_z = 0.0

	# Rate at which to publish velocity commands
	rate = rospy.Rate(10)

	while not rospy.is_shutdown():
		# Calculate errors
		print(f"Current X: {current_x}, Current_Y: {current_y}")
		error_x = target_x - current_x
		error_y = target_y - current_y

	#	if current_x < 0:
	#		vel_msg.linear.x = -0.5
	#		vel_msg.linear.y = 1
	#		vel_msg.linear.z = 0

		vel_msg.linear.x = 0.9
		vel_msg.linear.y = 0.9
		vel_msg.angular.z = 0

		# Publish the velocity commands
		velocity_publisher.publish(vel_msg)
		print(f"Error X: {error_x}, Error Y: {error_y}")

		if (abs(error_y) < 0.5 and abs(error_x) < 0.5):
			rospy.loginfo("TurtleBot reached the target position!")
			current_x = average[0]
			current_y = average[1]
			current_yaw = 0.0
	
			break

		rate.sleep()

vel_msg.linear.x = 0
vel_msg.linear.y = 0
vel_msg.angular.z = 0
velocity_publisher.publish(vel_msg)
