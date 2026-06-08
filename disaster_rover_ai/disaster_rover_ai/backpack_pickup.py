import time

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from std_msgs.msg import Bool
from std_msgs.msg import Float64


class BackpackPickup(Node):

    def __init__(self):

        super().__init__('backpack_pickup')

        self.state = ""

        self.done = False

        self.create_subscription(
            String,
            '/mission_state',
            self.state_callback,
            10
        )

        self.arm_base_pub = self.create_publisher(
            Float64,
            '/arm_base_joint/cmd_pos',
            10
        )

        self.shoulder_pub = self.create_publisher(
            Float64,
            '/shoulder_joint/cmd_pos',
            10
        )

        self.elbow_pub = self.create_publisher(
            Float64,
            '/elbow_joint/cmd_pos',
            10
        )

        self.wrist_pub = self.create_publisher(
            Float64,
            '/wrist_joint/cmd_pos',
            10
        )

        self.attached_pub = self.create_publisher(
            Bool,
            '/backpack_attached',
            10
        )

        self.timer = self.create_timer(
            0.1,
            self.control_loop
        )

    def state_callback(self, msg):

        self.state = msg.data

    def control_loop(self):

        if self.state != "PICKUP_BACKPACK":
            return

        if self.done:
            return

        arm = Float64()
        shoulder = Float64()
        elbow = Float64()
        wrist = Float64()

        #
        # Pickup pose
        #

        arm.data = 0.0
        shoulder.data = 0.8
        elbow.data = -1.4
        wrist.data = 0.5

        self.arm_base_pub.publish(arm)
        self.shoulder_pub.publish(shoulder)
        self.elbow_pub.publish(elbow)
        self.wrist_pub.publish(wrist)

        self.get_logger().info(
            "Moving arm to pickup pose..."
        )

        time.sleep(4.0)

        attached = Bool()
        attached.data = True

        self.attached_pub.publish(attached)

        self.done = True

        self.get_logger().info(
            "Backpack attached"
        )


def main(args=None):

    rclpy.init(args=args)

    node = BackpackPickup()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':

    main()