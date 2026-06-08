# import math

# import rclpy
# from rclpy.node import Node

# from std_msgs.msg import String
# from std_msgs.msg import Bool
# from sensor_msgs.msg import LaserScan

# from geometry_msgs.msg import Twist

# from nav_msgs.msg import Odometry

# from tf_transformations import euler_from_quaternion


# class AmbulanceReacher(Node):

#     def __init__(self):

#         super().__init__('ambulance_reacher')

#         self.state = ""

#         self.robot_x = 0.0
#         self.robot_y = 0.0
#         self.robot_yaw = 0.0

#         #
#         # Ambulance position
#         #

#         self.ambulance_x = -5.0
#         self.ambulance_y = -25.0
#         self.obstacle = False

#         self.mission_done = False

#         self.create_subscription(
#             String,
#             '/mission_state',
#             self.state_callback,
#             10)

#         self.create_subscription(
#         Bool,
#         '/obstacle_detected',
#         self.obstacle_callback,
#         10)   

#         self.create_subscription(
#             Odometry,
#             '/odom',
#             self.odom_callback,
#             10)

#         self.cmd_pub = self.create_publisher(
#             Twist,
#             '/cmd_vel',
#             10)

#         self.ambulance_reached_pub = self.create_publisher(
#             Bool,
#             '/ambulance_reached',
#             10)

#         self.backpack_attached_pub = self.create_publisher(
#             Bool,
#             '/backpack_attached',
#             10)

#         self.timer = self.create_timer(
#             0.1,
#             self.control_loop)

#     def obstacle_callback(self, msg):
#         self.obstacle = msg.data
                

#     def state_callback(self, msg):

#         self.state = msg.data

#         if self.state != "GO_TO_AMBULANCE":

#             self.mission_done = False

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

#         if self.state != "GO_TO_AMBULANCE":
#             return

#         if self.mission_done:
#             return

#         if self.obstacle:
#             cmd = Twist()
#             cmd.linear.x = 0.0
#             cmd.angular.z = 0.6
#             self.cmd_pub.publish(cmd)
#             return

#         dx = self.ambulance_x - self.robot_x
#         dy = self.ambulance_y - self.robot_y

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

#         #
#         # Arrived at ambulance
#         #

#         if distance < 1.0:

#             self.cmd_pub.publish(
#                 Twist()
#             )

#             #
#             # Drop backpack
#             #

#             attached = Bool()
#             attached.data = False

#             self.backpack_attached_pub.publish(
#                 attached
#             )

#             #
#             # Notify mission manager
#             #

#             reached = Bool()
#             reached.data = True

#             self.ambulance_reached_pub.publish(
#                 reached
#             )

#             self.get_logger().info(
#                 "Backpack delivered to ambulance"
#             )

#             self.mission_done = True

#             return

#         #
#         # Rotate toward ambulance
#         #

#         if abs(yaw_error) > 0.2:

#             if yaw_error > 0:

#                 cmd.angular.z = 0.5

#             else:

#                 cmd.angular.z = -0.5

#         #
#         # Drive forward
#         #

#         else:

#             cmd.linear.x = 0.4

#         self.cmd_pub.publish(
#             cmd
#         )


# def main(args=None):

#     rclpy.init(args=args)

#     node = AmbulanceReacher()

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

from tf_transformations import euler_from_quaternion

import tf2_ros


class AmbulanceReacher(Node):

    def __init__(self):

        super().__init__('ambulance_reacher')

        self.state = ""

        self.ambulance_x = -5.0
        self.ambulance_y = -25.0

        self.obstacle = False
        self.mission_done = False

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
            '/obstacle_detected',
            self.obstacle_callback,
            10)

        self.cmd_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10)

        self.ambulance_reached_pub = self.create_publisher(
            Bool,
            '/ambulance_reached',
            10)

        self.backpack_attached_pub = self.create_publisher(
            Bool,
            '/backpack_attached',
            10)

        self.timer = self.create_timer(
            0.1,
            self.control_loop)

    def state_callback(self, msg):

        self.state = msg.data

        if self.state != "GO_TO_AMBULANCE":
            self.mission_done = False

    def obstacle_callback(self, msg):

        self.obstacle = msg.data

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

        if self.state != "GO_TO_AMBULANCE":
            return

        if self.mission_done:
            return

        pose = self.get_robot_pose()

        if pose is None:
            return

        robot_x, robot_y, robot_yaw = pose

        if self.obstacle:

            cmd = Twist()
            cmd.linear.x = 0.0
            cmd.angular.z = 0.6

            self.cmd_pub.publish(cmd)

            return

        dx = self.ambulance_x - robot_x
        dy = self.ambulance_y - robot_y

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

            attached = Bool()
            attached.data = False

            self.backpack_attached_pub.publish(
                attached
            )

            reached = Bool()
            reached.data = True

            self.ambulance_reached_pub.publish(
                reached
            )

            self.get_logger().info(
                "Backpack delivered to ambulance"
            )

            self.mission_done = True

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
            f"Ambulance ({self.ambulance_x:.2f}, {self.ambulance_y:.2f}) "
            f"Robot ({robot_x:.2f}, {robot_y:.2f}) "
            f"Distance {distance:.2f}",
            throttle_duration_sec=1.0
        )


def main(args=None):

    rclpy.init(args=args)

    node = AmbulanceReacher()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':

    main()

