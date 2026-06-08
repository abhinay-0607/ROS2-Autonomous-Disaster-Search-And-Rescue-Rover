import rclpy

from rclpy.node import Node

from std_msgs.msg import Bool
from std_msgs.msg import String


class MissionManager(Node):

    def __init__(self):

        super().__init__('mission_manager')

        self.current_state = "EXPLORE"

        self.state_pub = self.create_publisher(
            String,
            '/mission_state',
            10)

        self.create_subscription(
            Bool,
            '/victim_detected',
            self.victim_callback,
            10)

        self.create_subscription(
            Bool,
            '/victim_reached',
            self.victim_reached_callback,
            10)

        self.create_subscription(
            Bool,
            '/backpack_reached',
            self.backpack_reached_callback,
            10)

        self.create_subscription(
            Bool,
            '/backpack_attached',
            self.backpack_attached_callback,
            10)

        self.create_subscription(
            Bool,
            '/ambulance_reached',
            self.ambulance_reached_callback,
            10)

        self.timer = self.create_timer(
            0.1,
            self.publish_state)

    def victim_callback(self, msg):

        if msg.data and self.current_state == "EXPLORE":

            self.current_state = "APPROACH_VICTIM"

            self.get_logger().info(
                "Victim detected -> APPROACH_VICTIM"
            )

    def victim_reached_callback(self, msg):

        if msg.data and self.current_state == "APPROACH_VICTIM":

            self.current_state = "GO_TO_BACKPACK"

            self.get_logger().info(
                "Victim reached -> GO_TO_BACKPACK"
            )

    def backpack_reached_callback(self, msg):

        if msg.data and self.current_state == "GO_TO_BACKPACK":

            self.current_state = "PICKUP_BACKPACK"

            self.get_logger().info(
                "Backpack reached -> PICKUP_BACKPACK"
            )

    def backpack_attached_callback(self, msg):

        if msg.data and self.current_state == "PICKUP_BACKPACK":

            self.current_state = "GO_TO_AMBULANCE"

            self.get_logger().info(
                "Backpack attached -> GO_TO_AMBULANCE"
            )

    def ambulance_reached_callback(self, msg):

        if msg.data and self.current_state == "GO_TO_AMBULANCE":

            self.current_state = "EXPLORE"

            self.get_logger().info(
                "Ambulance reached -> EXPLORE"
            )

    def publish_state(self):

        msg = String()

        msg.data = self.current_state

        self.state_pub.publish(msg)

    def reset_mission(self):

        self.current_state = "EXPLORE"

        self.get_logger().info(
            "Mission reset -> EXPLORE"
        )


def main(args=None):

    rclpy.init(args=args)

    node = MissionManager()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':

    main()