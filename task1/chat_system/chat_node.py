import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class ChatNode(Node):
    def __init__(self):
        super().__init__('chat_node')
        self.pub = self.create_publisher(String, 'chat_topic', 10)
        self.sub = self.create_subscription(String, 'chat_topic', self.callback, 10)
        self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        msg = String()
        msg.data = 'Invictus: Hello Hawcker!'
        self.pub.publish(msg)

    def callback(self, msg):
        self.get_logger().info(f'Heard: {msg.data}')

def main():
    rclpy.init()
    node = ChatNode()
    rclpy.spin(node)
    rclpy.shutdown()
