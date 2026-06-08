# import math
# import rclpy
# from rclpy.node import Node
# from std_msgs.msg import Bool
# from geometry_msgs.msg import PoseStamped
# from nav_msgs.msg import Odometry

# class VictimDetector(Node):
#     def __init__(self):
#         super().__init__('victim_detector')
#         self.robot_x = 0.0
#         self.robot_y = 0.0

#         self.victims = [
#             ("survivor_person_1", -23.5, 21.5),
#             ("survivor_person_2", 24.5, -19.0),
#             ("survivor_person_3", 0.8, 27.5),
#         ]    

#         self.create_subscription(Odometry, '/odom', self.odom_callback, 10)
#         self.detected_pub = self.create_publisher(Bool, '/victim_detected', 10)
#         self.pose_pub = self.create_publisher(PoseStamped, '/victim_pose', 10)
#         self.timer = self.create_timer(0.2, self.detect_victims)
    
#     def odom_callback(self, msg):
#         self.robot_x = msg.pose.pose.position.x
#         self.robot_y = msg.pose.pose.position.y

#     def detect_victims(self):
#         nearest_name = None
#         nearest_x = 0.0
#         nearest_y = 0.0    
#         nearest_distance = 999999.0
#         for name, x, y in self.victims:
#             distance = math.sqrt((x - self.robot_x) ** 2 + (y - self.robot_y) ** 2)
#             if distance < nearest_distance:
#                 nearest_name = name
#                 nearest_x = x
#                 nearest_y = y
#                 nearest_distance = distance
#         detected = Bool()
#         if nearest_distance < 10.0:
#             detected.data = True
#             self.detected_pub.publish(detected)
#             pose = PoseStamped()
#             pose.header.frame_id = "odom"
#             pose.pose.position.x = nearest_x
#             pose.pose.position.y = nearest_y
#             pose.pose.position.z = 0.0 
#             self.pose_pub.publish(pose)

#             self.get_logger().info(f"Victim detected: {nearest_name} at distance {nearest_distance:.2f} m")
#             self.get_logger().info(
#             f"Robot ({self.robot_x:.2f}, {self.robot_y:.2f}) "
#             f"Victim ({nearest_x:.2f}, {nearest_y:.2f}) "
#             f"Distance {nearest_distance:.2f}",
#             throttle_duration_sec=2.0
#             )
#         else:
#             detected.data = False
#             self.detected_pub.publish(detected)  

# def main(args=None):
#     rclpy.init(args=args)
#     victim_detector = VictimDetector()
#     rclpy.spin(victim_detector)
#     victim_detector.destroy_node()
#     rclpy.shutdown()

# if __name__ == '__main__':
#     main()                

import math

import rclpy
from rclpy.node import Node

from std_msgs.msg import Bool
from geometry_msgs.msg import PoseStamped

import tf2_ros


class VictimDetector(Node):

    def __init__(self):
        super().__init__('victim_detector')

        self.victims = [
            ("survivor_person_1", -66, -66),
            ("survivor_person_2", 24.5, -19.0),
            ("survivor_person_3", 0.8, 27.5),
        ]

        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(
            self.tf_buffer,
            self
        )

        self.detected_pub = self.create_publisher(
            Bool,
            '/victim_detected',
            10
        )

        self.pose_pub = self.create_publisher(
            PoseStamped,
            '/victim_pose',
            10
        )

        self.timer = self.create_timer(
            0.2,
            self.detect_victims
        )

    def get_robot_pose(self):

        try:

            transform = self.tf_buffer.lookup_transform(
                'map',
                'base_link',
                rclpy.time.Time()
            )

            x = transform.transform.translation.x
            y = transform.transform.translation.y

            return x, y

        except Exception:
            return None

    def detect_victims(self):

        pose = self.get_robot_pose()

        if pose is None:
            return

        robot_x, robot_y = pose

        nearest_name = None
        nearest_x = 0.0
        nearest_y = 0.0
        nearest_distance = float('inf')

        for name, x, y in self.victims:

            distance = math.sqrt(
                (x - robot_x) ** 2 +
                (y - robot_y) ** 2
            )

            if distance < nearest_distance:
                nearest_name = name
                nearest_x = x
                nearest_y = y
                nearest_distance = distance

        detected = Bool()

        if nearest_distance < 10.0:

            detected.data = True
            self.detected_pub.publish(detected)

            victim_pose = PoseStamped()

            victim_pose.header.stamp = self.get_clock().now().to_msg()
            victim_pose.header.frame_id = "map"

            victim_pose.pose.position.x = nearest_x
            victim_pose.pose.position.y = nearest_y
            victim_pose.pose.position.z = 0.0

            victim_pose.pose.orientation.w = 1.0

            self.pose_pub.publish(victim_pose)

            self.get_logger().info(
                f"Victim detected: {nearest_name} "
                f"distance={nearest_distance:.2f}m",
                throttle_duration_sec=2.0
            )

            self.get_logger().info(
                f"Robot ({robot_x:.2f}, {robot_y:.2f}) "
                f"Victim ({nearest_x:.2f}, {nearest_y:.2f})",
                throttle_duration_sec=2.0
            )

        else:

            detected.data = False
            self.detected_pub.publish(detected)


def main(args=None):

    rclpy.init(args=args)

    node = VictimDetector()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()