import rclpy

from rclpy.node import Node
from std_msgs.msg import Bool
from sensor_msgs.msg import LaserScan

class ObstacleAvoidance(Node):
    def __init__(self):
        super().__init__('obstacle_avoidance')
        self.pub = self.create_publisher(Bool, '/obstacle_detected', 10)
        self.create_subscription(LaserScan, 'scan', self.scan_callback, 10)

    def scan_callback(self, msg):    
        obstacle_detected = False

        front = min(msg.ranges[330:390])

        if 0.0 < front < 3.0:
            obstacle_detected = True
            

        out = Bool()
        out.data = obstacle_detected
        self.pub.publish(out)
        
def main(args=None):        
    rclpy.init(args=args)
    obstacle_avoidance = ObstacleAvoidance()
    rclpy.spin(obstacle_avoidance)
    obstacle_avoidance.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':    
    main()