import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import sys

class Commander(Node):
    def __init__(self):
        super().__init__('commander')
        self.publisher_ = self.create_publisher(String, '/cmd', 10)
        self.get_logger().info("Commander Online. Commands: forward, backward, turn left, turn right")
        self.create_timer(0.1, self.read_input)

    def read_input(self):
        print("\nMove Command: ", end='', flush=True)
        line = sys.stdin.readline().strip().lower()
        if line:
            msg = String()
            msg.data = line
            self.publisher_.publish(msg)

def main():
    rclpy.init()
    rclpy.spin(Commander())
    rclpy.shutdown()
