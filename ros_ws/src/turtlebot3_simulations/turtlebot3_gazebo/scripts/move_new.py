#! /usr/bin/env python3
import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from math import atan2, sqrt

x = 0.0
y = 0.0
theta = 0.0

def newOdom(msg):
    global x
    global y
    global theta

    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y

    rot_q = msg.pose.pose.orientation
    (roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])

rospy.init_node("move_turtlebot", anonymous=True)

sub = rospy.Subscriber("/odometry/filtered", Odometry, newOdom)
pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
speed = Twist()

r = rospy.Rate(4)

path_list = [(4.307522, 133.194772)]
point_index = 0
goal = Point()

while not rospy.is_shutdown():
    if point_index < len(path_list):
        goal.x = path_list[point_index][0]
        goal.y = path_list[point_index][1]
    else:
        break

    # Calculate the difference between the current position and the goal
    inc_x = goal.x - x
    inc_y = goal.y - y

    # Calculate the distance to the goal
    distance_to_goal = sqrt(inc_x**2 + inc_y**2)

    # Calculate the angle to the goal
    angle_to_goal = atan2(inc_y, inc_x)

    # Ensure the angle is within -pi to pi range for proper comparison
    angle_difference = angle_to_goal - theta
    if angle_difference > 3.14159:
        angle_difference -= 2 * 3.14159
    elif angle_difference < -3.14159:
        angle_difference += 2 * 3.14159

    # If the distance to the goal is significant, adjust the velocities
    if distance_to_goal >= 0.3:
        if abs(angle_difference) > 0.2:
            # If the angle difference is significant, turn in place
            speed.linear.x = 0.0
            speed.angular.z = 0.9 if angle_difference > 0 else -0.9
        else:
            # Move forward
            speed.linear.x = 0.8
            speed.angular.z = 0.0
    else:
        # If close to the goal, move to the next point
        point_index += 1

    # Publish the velocity command
    pub.publish(speed)

    # Sleep to maintain the desired rate
    r.sleep()
