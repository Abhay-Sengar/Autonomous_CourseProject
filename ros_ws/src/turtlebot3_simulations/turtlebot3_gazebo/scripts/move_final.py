# #!/usr/bin/env python3

# import rospy
# from geometry_msgs.msg import Twist
# from nav_msgs.msg import Path
# from geometry_msgs.msg import PoseStamped
# import math

# def calculate_average(point1, point2):
#     return ((point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2)

# def generate_intermediate_points(point1, point2, num_points):
#     intermediate_points = []
#     for i in range(1, num_points + 1):
#         x = point1[0] + (point2[0] - point1[0]) * (i / (num_points + 1))
#         y = point1[1] + (point2[1] - point1[1]) * (i / (num_points + 1))
#         intermediate_points.append((x, y))
#     return intermediate_points

# def generate_path(coordinates, num_intermediate_points):
#     path = []
#     for i in range(0, len(coordinates) - 1, 2):
#         start = coordinates[i]
#         end = coordinates[i + 1]
#         average = calculate_average(start, end)
#         intermediate_points = generate_intermediate_points(start, end, num_intermediate_points)
#         path.extend(intermediate_points)
#         path.append(end)
#     return path

# def publish_path(path_points):
#     rospy.init_node('move_turtlebot', anonymous=True)
#     path_pub = rospy.Publisher('/path', Path, queue_size=10)
#     rate = rospy.Rate(1)  # Publish at 1Hz

#     while not rospy.is_shutdown():
#         path_msg = Path()
#         path_msg.header.stamp = rospy.Time.now()
#         path_msg.header.frame_id = 'map'

#         for point in path_points:
#             pose = PoseStamped()
#             pose.pose.position.x = point[0]
#             pose.pose.position.y = point[1]
#             pose.pose.orientation.w = 1  # Assuming orientation is not important for now
#             path_msg.poses.append(pose)

#         path_pub.publish(path_msg)
#         rate.sleep()

# if __name__ == '__main__':
#     # Coordinates for the path
#     coordinates = [
#         (-1.692532, 1.332115),(0.842878, 1.734334),
#         (-1.769300, 2.622560),(0.764455, 2.790548),
#         (-1.797779, 4.651069), (0.654387, 4.125747),
#         (-2.474552, 16.901815), (-0.253607, 17.065682),
#         (-2.559997, 20.144867),(-0.490302, 20.307751),
#         (-2.702207, 21.858159), (-0.390476, 22.053707),
#         (-0.883531, 27.789717), (1.464111, 28.004511),
#         (1.688054, 35.037535), (4.040378, 34.969680),
#         (2.5050610,37.182738), (4.658815, 36.740781),
#         (3.121913,38.628931), (5.529262, 38.560974),
#         (5.687191, 44.511974), (7.954768, 44.451004),
#         (9.188579, 53.373150), (11.105843, 52.792646),
#         (9.615917, 57.918851), (11.569015, 57.036502),
#         (9.857019, 79.209601),(11.761967, 78.837462),
#         (9.656191, 87.138443), (11.654459, 87.697128),
#         (9.481932, 95.392532), (11.582266, 95.313172),
#         (10.733526, 101.960448), (12.961380, 102.340482),
#         (20.622720, 127.246245), (22.776048, 126.951720),
#         (27.717867, 140.627711), (29.739610, 139.906729),
#         (29.670853, 144.925047), (31.945065, 144.757087),
#         (32.515902, 151.442093), (34.727159, 150.731613),
#         (32.370835, 152.173457), (33.024631, 154.281436),
#         (24.021516, 155.589865), (25.139362, 157.504814),
#         (18.688517, 157.150096), (18.883884, 159.391280),
#         (18.395054, 160.008823), (20.339431, 159.698624),
#         (19.118401, 164.118771),(21.287996, 163.489371),
#     ]
#     num_intermediate_points = 10

#     # Generate path
#     path_points = generate_path(coordinates, num_intermediate_points)

#     try:
#         publish_path(path_points)
#     except rospy.ROSInterruptException:
#         pass

#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
import math

# Global variables
current_index = 0
path_points = [(-1.692532, 1.332115),(0.842878, 1.734334)]

def calculate_distance(point1, point2):
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

def calculate_heading(point1, point2):
    return math.atan2(point2[1] - point1[1], point2[0] - point1[0])

def update_current_index(current_pos):
    global current_index, path_points
    min_distance = float('inf')
    for i, point in enumerate(path_points):
        distance = calculate_distance(current_pos, point)
        if distance < min_distance:
            min_distance = distance
            current_index = i

def publish_velocity_cmd():
    global current_index, path_points
    if current_index < len(path_points) - 1:
        current_pos = path_points[current_index]
        next_pos = path_points[current_index + 1]
        distance = calculate_distance(current_pos, next_pos)
        heading = calculate_heading(current_pos, next_pos)

        twist_msg = Twist()
        twist_msg.linear.x = 0.2 # Constant linear velocity for simplicity
        twist_msg.angular.z = 0.2 * (heading - 0)  # Proportional control for angular velocity

        cmd_vel_pub.publish(twist_msg)

def path_callback(path_msg):
    global path_points
    path_points = [(pose.pose.position.x, pose.pose.position.y) for pose in path_msg.poses]

def move_turtlebot():
    rospy.init_node('move_turtlebot', anonymous=True)
    rospy.Subscriber('/path', Path, path_callback)
    rate = rospy.Rate(10)  # 10 Hz

    while not rospy.is_shutdown():
        if path_points:
            publish_velocity_cmd()
        rate.sleep()

if __name__ == '__main__':
    try:
        cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        move_turtlebot()
    except rospy.ROSInterruptException:
        pass
