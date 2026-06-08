# import math

# import rclpy
# from rclpy.node import Node

# from std_msgs.msg import String
# from std_msgs.msg import Bool

# from geometry_msgs.msg import Twist

# from nav_msgs.msg import Odometry

# from tf_transformations import euler_from_quaternion


# class BackpackApproach(Node):

#     def __init__(self):

#         super().__init__('backpack_approach')

#         self.state = ""

#         self.robot_x = 0.0
#         self.robot_y = 0.0
#         self.robot_yaw = 0.0

#         self.backpacks = [
#             (-24.0, 22.0),
#             (24.0, -20.0),
#             (0.0, 28.0)
#         ]

#         self.target_x = 0.0
#         self.target_y = 0.0

#         self.create_subscription(
#             String,
#             '/mission_state',
#             self.state_callback,
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

#         self.backpack_reached_pub = self.create_publisher(
#             Bool,
#             '/backpack_reached',
#             10)

#         self.timer = self.create_timer(
#             0.1,
#             self.control_loop)

#     def state_callback(self, msg):

#         self.state = msg.data

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

#         if self.state != "GO_TO_BACKPACK":
#             return

#         nearest_distance = float('inf')

#         for bx, by in self.backpacks:

#             d = math.sqrt(
#                 (bx - self.robot_x) ** 2 +
#                 (by - self.robot_y) ** 2
#             )

#             if d < nearest_distance:

#                 nearest_distance = d

#                 self.target_x = bx
#                 self.target_y = by

#         dx = self.target_x - self.robot_x
#         dy = self.target_y - self.robot_y

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

#         if distance < 0.75:

#             self.cmd_pub.publish(
#                 Twist()
#             )

#             reached = Bool()
#             reached.data = True

#             self.backpack_reached_pub.publish(
#                 reached
#             )

#             self.get_logger().info(
#                 "Backpack reached"
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


# def main(args=None):

#     rclpy.init(args=args)

#     node = BackpackApproach()

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


class BackpackApproach(Node):

    def __init__(self):

        super().__init__('backpack_approach')

        self.state = ""

        self.backpacks = [
            (-66, -66),
            (24.0, -20.0),
            (0.0, 28.0)
        ]

        self.target_x = 0.0
        self.target_y = 0.0

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

        self.cmd_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10)

        self.backpack_reached_pub = self.create_publisher(
            Bool,
            '/backpack_reached',
            10)

        self.timer = self.create_timer(
            0.1,
            self.control_loop)

    def state_callback(self, msg):

        self.state = msg.data

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

        if self.state != "GO_TO_BACKPACK":
            return

        pose = self.get_robot_pose()

        if pose is None:
            return

        robot_x, robot_y, robot_yaw = pose

        nearest_distance = float('inf')

        for bx, by in self.backpacks:

            d = math.sqrt(
                (bx - robot_x) ** 2 +
                (by - robot_y) ** 2
            )

            if d < nearest_distance:

                nearest_distance = d

                self.target_x = bx
                self.target_y = by

        dx = self.target_x - robot_x
        dy = self.target_y - robot_y

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

        if distance < 0.75:

            self.cmd_pub.publish(
                Twist()
            )

            reached = Bool()
            reached.data = True

            self.backpack_reached_pub.publish(
                reached
            )

            self.get_logger().info(
                "Backpack reached"
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
            f"Target ({self.target_x:.2f}, {self.target_y:.2f}) "
            f"Robot ({robot_x:.2f}, {robot_y:.2f}) "
            f"Distance {distance:.2f}",
            throttle_duration_sec=1.0
        )


def main(args=None):

    rclpy.init(args=args)

    node = BackpackApproach()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':

    main()

