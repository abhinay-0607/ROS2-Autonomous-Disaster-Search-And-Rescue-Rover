# import math

# import rclpy
# from rclpy.node import Node

# from std_msgs.msg import String
# from std_msgs.msg import Bool

# from geometry_msgs.msg import Twist
# from geometry_msgs.msg import PoseStamped

# from nav_msgs.msg import Odometry

# from tf_transformations import euler_from_quaternion


# class VictimApproach(Node):

#     def __init__(self):

#         super().__init__('victim_approach')

#         self.state = ""

#         self.victim_detected = False
#         self.obstacle_detected = False

#         self.robot_x = 0.0
#         self.robot_y = 0.0
#         self.robot_yaw = 0.0

#         self.victim_x = 0.0
#         self.victim_y = 0.0

#         self.create_subscription(
#             String,
#             '/mission_state',
#             self.state_callback,
#             10)

#         self.create_subscription(
#             Bool,
#             '/victim_detected',
#             self.victim_detected_callback,
#             10)

#         self.create_subscription(
#             Bool,
#             '/obstacle_detected',
#             self.obstacle_detected_callback,
#             10)    

#         self.create_subscription(
#             PoseStamped,
#             '/victim_pose',
#             self.pose_callback,
#             10)

#         self.create_subscription(
#             Odometry,
#             '/odom',
#             self.odom_callback,
#             10)

#         self.cmd_pub = self.create_publisher(
#             Twist,
#             '/cmd_vel',
#             10)

#         self.victim_reached_pub = self.create_publisher(
#             Bool,
#             '/victim_reached',
#             10)

#         self.timer = self.create_timer(
#             0.1,
#             self.control_loop)

#     def state_callback(self, msg):

#         self.state = msg.data

#     def obstacle_detected_callback(self, msg):    
#         self.obstacle_detected = msg.data

#     def victim_detected_callback(self, msg):

#         self.victim_detected = msg.data

#     def pose_callback(self, msg):

#         self.victim_x = msg.pose.position.x
#         self.victim_y = msg.pose.position.y

#     def odom_callback(self, msg):

#         self.robot_x = msg.pose.pose.position.x
#         self.robot_y = msg.pose.pose.position.y

#         q = msg.pose.pose.orientation

#         _, _, self.robot_yaw = euler_from_quaternion(
#             [
#                 q.x,
#                 q.y,
#                 q.z,
#                 q.w
#             ]
#         )

#     def control_loop(self):

#         if self.state != "APPROACH_VICTIM":
#             return

#         if not self.victim_detected:
#             return

#         if self.obstacle_detected:
#              cmd = Twist()
#              cmd.linear.x = 0.0
#              cmd.angular.z = 0.6
#              self.cmd_pub.publish(cmd)    
#              return

#         dx = self.victim_x - self.robot_x
#         dy = self.victim_y - self.robot_y

#         distance = math.sqrt(
#             dx * dx +
#             dy * dy
#         )

#         desired_yaw = math.atan2(
#             dy,
#             dx
#         )

#         yaw_error = desired_yaw - self.robot_yaw

#         while yaw_error > math.pi:
#             yaw_error -= 2.0 * math.pi

#         while yaw_error < -math.pi:
#             yaw_error += 2.0 * math.pi

#         cmd = Twist()

#         if distance < 1.0:

#             self.cmd_pub.publish(
#                 Twist()
#             )

#             reached = Bool()
#             reached.data = True

#             self.victim_reached_pub.publish(
#                 reached
#             )

#             self.get_logger().info(
#                 "Victim reached"
#             )

#             return

#         if abs(yaw_error) > 0.2:

#             if yaw_error > 0:

#                 cmd.angular.z = 0.5

#             else:

#                 cmd.angular.z = -0.5

#         else:

#             cmd.linear.x = 0.4

#         self.cmd_pub.publish(
#             cmd
#         )

#         self.get_logger().info(
#         f"Target ({self.victim_x:.2f}, {self.victim_y:.2f}) "
#         f"Robot ({self.robot_x:.2f}, {self.robot_y:.2f})",
#         throttle_duration_sec=1.0
# )


# def main(args=None):

#     rclpy.init(args=args)

#     node = VictimApproach()

#     rclpy.spin(node)

#     node.destroy_node()

#     rclpy.shutdown()


# if __name__ == '__main__':

#     main()


import math

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from std_msgs.msg import Bool

from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseStamped

from tf_transformations import euler_from_quaternion

import tf2_ros


class VictimApproach(Node):

    def __init__(self):

        super().__init__('victim_approach')

        self.state = ""

        self.victim_detected = False
        self.obstacle_detected = False

        self.victim_x = 0.0
        self.victim_y = 0.0

        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(
            self.tf_buffer,
            self
        )

        self.create_subscription(
            String,
            '/mission_state',
            self.state_callback,
            10)

        self.create_subscription(
            Bool,
            '/victim_detected',
            self.victim_detected_callback,
            10)

        self.create_subscription(
            Bool,
            '/obstacle_detected',
            self.obstacle_detected_callback,
            10)

        self.create_subscription(
            PoseStamped,
            '/victim_pose',
            self.pose_callback,
            10)

        self.cmd_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10)

        self.victim_reached_pub = self.create_publisher(
            Bool,
            '/victim_reached',
            10)

        self.timer = self.create_timer(
            0.1,
            self.control_loop)

    def state_callback(self, msg):

        self.state = msg.data

    def obstacle_detected_callback(self, msg):

        self.obstacle_detected = msg.data

    def victim_detected_callback(self, msg):

        self.victim_detected = msg.data

    def pose_callback(self, msg):

        self.victim_x = msg.pose.position.x
        self.victim_y = msg.pose.position.y

    def get_robot_pose(self):

        try:

            transform = self.tf_buffer.lookup_transform(
                'map',
                'base_link',
                rclpy.time.Time()
            )

            x = transform.transform.translation.x
            y = transform.transform.translation.y

            q = transform.transform.rotation

            _, _, yaw = euler_from_quaternion(
                [
                    q.x,
                    q.y,
                    q.z,
                    q.w
                ]
            )

            return x, y, yaw

        except Exception:

            return None

    def control_loop(self):

        if self.state != "APPROACH_VICTIM":
            return

        if not self.victim_detected:
            return

        pose = self.get_robot_pose()

        if pose is None:
            return

        robot_x, robot_y, robot_yaw = pose

        if self.obstacle_detected:

            cmd = Twist()
            cmd.linear.x = 0.0
            cmd.angular.z = 0.6

            self.cmd_pub.publish(cmd)

            return

        dx = self.victim_x - robot_x
        dy = self.victim_y - robot_y

        distance = math.sqrt(
            dx * dx +
            dy * dy
        )

        desired_yaw = math.atan2(
            dy,
            dx
        )

        yaw_error = desired_yaw - robot_yaw

        while yaw_error > math.pi:
            yaw_error -= 2.0 * math.pi

        while yaw_error < -math.pi:
            yaw_error += 2.0 * math.pi

        cmd = Twist()

        if distance < 1.0:

            self.cmd_pub.publish(
                Twist()
            )

            reached = Bool()
            reached.data = True

            self.victim_reached_pub.publish(
                reached
            )

            self.get_logger().info(
                "Victim reached"
            )

            return

        if abs(yaw_error) > 0.2:

            if yaw_error > 0:
                cmd.angular.z = 0.5
            else:
                cmd.angular.z = -0.5

        else:

            cmd.linear.x = 0.4

        self.cmd_pub.publish(cmd)

        self.get_logger().info(
            f"Target ({self.victim_x:.2f}, {self.victim_y:.2f}) "
            f"Robot ({robot_x:.2f}, {robot_y:.2f}) "
            f"Distance {distance:.2f}",
            throttle_duration_sec=1.0
        )


def main(args=None):

    rclpy.init(args=args)

    node = VictimApproach()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':

    main()

