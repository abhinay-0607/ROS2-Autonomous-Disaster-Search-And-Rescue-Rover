import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from geometry_msgs.msg import Twist


class AvoidObstacle(Node):

    def __init__(self):

        super().__init__('avoid_obstacle')

        self.state = "EXPLORE"

        self.pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10)

        self.create_subscription(
            String,
            '/mission_state',
            self.state_callback,
            10)

        self.timer = self.create_timer(
            0.1,
            self.loop)

    def state_callback(self, msg):

        self.state = msg.data

    def loop(self):

        if self.state != "AVOID_OBSTACLE":
            return

        cmd = Twist()

        cmd.angular.z = 0.6

        self.pub.publish(cmd)


def main(args=None):

    rclpy.init(args=args)

    node = AvoidObstacle()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()