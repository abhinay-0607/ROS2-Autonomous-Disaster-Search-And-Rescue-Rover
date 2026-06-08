import subprocess

import rclpy
from rclpy.node import Node

from std_msgs.msg import Bool

import tf2_ros


class BackpackFollower(Node):

    def __init__(self):

        super().__init__('backpack_follower')

        self.attached = False

        self.backpack_name = "survivor_backpack_1"

        self.create_subscription(
            Bool,
            '/backpack_attached',
            self.attached_callback,
            10
        )

        self.tf_buffer = tf2_ros.Buffer()

        self.tf_listener = tf2_ros.TransformListener(
            self.tf_buffer,
            self
        )

        self.timer = self.create_timer(
            0.1,
            self.follow_backpack
        )

    def attached_callback(self, msg):

        self.attached = msg.data

    def follow_backpack(self):

        if not self.attached:
            return

        try:

            transform = self.tf_buffer.lookup_transform(
                'map',
                'gripper_base_link',
                rclpy.time.Time()
            )

            x = transform.transform.translation.x
            y = transform.transform.translation.y
            z = transform.transform.translation.z


            x += 0.15
            z += 0.05

            req = f'''
name: "{self.backpack_name}"

position {{
  x: {x}
  y: {y}
  z: {z}
}}
'''

            subprocess.run(
                [
                    'gz',
                    'service',
                    '-s',
                    '/world/beach_disaster_world/set_pose',
                    '--reqtype',
                    'gz.msgs.Pose',
                    '--reptype',
                    'gz.msgs.Boolean',
                    '--timeout',
                    '1000',
                    '--req',
                    req
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

        except Exception:

            pass


def main(args=None):

    rclpy.init(args=args)

    node = BackpackFollower()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':

    main()