#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from std_msgs.msg import Bool
from std_msgs.msg import String


class Explorer(Node):

    def __init__(self):

        super().__init__('autonomous_explorer')

        self.state = "EXPLORE"
        self.obstacle_detected = False

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

        self.publisher_ = self.create_publisher(
            Twist,
            '/cmd_vel',
            10)

        self.timer = self.create_timer(
            0.1,
            self.explore)

    def state_callback(self, msg):

        self.state = msg.data

    def obstacle_callback(self, msg):
        
        self.obstacle_detected = msg.data


    def explore(self):

        if self.state != "EXPLORE":
            return

        cmd = Twist()
        
        if self.obstacle_detected == False:
            cmd.linear.x = 0.4
        else:
            cmd.angular.z = 0.6

        self.publisher_.publish(cmd)  
        

        
        

def main(args=None):

    rclpy.init(args=args)

    node = Explorer()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()