#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

def odom_callback(msg):
    current_x = msg.pose.pose.position.x
    current_y = msg.pose.pose.position.y
    rospy.loginfo(f"Current position: ({current_x}, {current_y})")

rospy.init_node('move_turtlebot', anonymous=True)
print("started")

current_x = 0.0
current_y = 0.0

def move_to_target(target_x, target_y):
    global current_x, current_y

    # Proportional control constants
    linear_velocity_x = 0.5  # Adjust the linear velocity as needed
    linear_velocity_y = 0.75  # Adjust the linear velocity as needed
    # Rate at which to publish velocity commands
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        # Calculate errors
        rospy.Subscriber("/odom", Odometry, odom_callback)

        error_x = target_x - current_x
        error_y = target_y - current_y

            # Create a Twist message to publish velocity commands
        vel_msg = Twist()
        vel_msg.linear.x = linear_velocity_x 
        vel_msg.linear.y = linear_velocity_y 
        vel_msg.angular.z = 0.0

        if target_x > 0 and current_x < 0:
            vel_msg.linear.x = -0.5
            vel_msg.linear.y = 1
            vel_msg.linear.z = 0
            
            velocity_publisher.publish(vel_msg)
        
        if target_y > 0 and current_y < 0:
            vel_msg.linear.x = 1
            vel_msg.linear.y = -0.5
            vel_msg.linear.z = 0
            
            velocity_publisher.publish(vel_msg)
    
        print(vel_msg.linear.x, vel_msg.linear.y)

        # Publish the velocity commands
        velocity_publisher.publish(vel_msg)

        # Check if the target position is reached
        if abs(error_x) < 0.1 and abs(error_y) < 0.1:
            rospy.loginfo("TurtleBot reached the target position!")
            current_x = target_x
            current_y = target_y
            break

        rate.sleep()

velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

coordinates = [
    (-1.692532, 1.332115), (0.842878, 1.734334),
    (-1.769300, 2.622560), (0.764455, 2.790548),
    (-1.797779, 4.651069), (0.654387, 4.125747),
    (-2.474552, 16.901815), (-0.253607, 17.065682),
    (-2.559997, 20.144867), (-0.490302, 20.307751),
    (-2.702207, 21.858159), (-0.390476, 22.053707),
    (-0.883531, 27.789717), (1.464111, 28.004511),
    (1.688054, 35.037535), (4.040378, 34.969680),
    (2.5050610, 37.182738), (4.658815, 36.740781),
    (3.121913, 38.628931), (5.529262, 38.560974),
    (5.687191, 44.511974), (7.954768, 44.451004),
    (9.188579, 53.373150), (11.105843, 52.792646),
    (9.615917, 57.918851), (11.569015, 57.036502),
    (9.857019, 79.209601), (11.761967, 78.837462),
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
    (19.118401, 164.118771), (21.287996, 163.489371),
]
#for i in range(len(coordinates)):
 #   coordinates[i] = (-1*coordinates[i][0], coordinates[i][1])

for i in range(0, len(coordinates), 2):
    start = coordinates[i]
    end = coordinates[i + 1]

    # Calculate the average point
    average_x = (start[0] + end[0]) / 2
    average_y = (start[1] + end[1]) / 2

    print(average_x, average_y)
    # Move to the average point
    move_to_target(average_x, average_y)

# Stop the robot after reaching the last point
stop_msg = Twist()
velocity_publisher.publish(stop_msg)
