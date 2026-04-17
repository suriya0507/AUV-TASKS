import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sub_interfaces.msg import BotPose

class Navigator(Node):
    def __init__(self):
        super().__init__('navigator')
        
        # 1. Define the States
        self.states = ["North", "East", "South", "West"]
        self.current_state_idx = 0  # Start at North
        
        # 2. Define the Position
        self.x = 0.0
        self.y = 0.0

        # 3. Define Movement Vectors (The State Machine's "Effectors")
        # Format: { State: (delta_x, delta_y) }
        self.move_map = {
            "North": (0.0, 1.0),
            "East":  (1.0, 0.0),
            "South": (0.0, -1.0),
            "West":  (-1.0, 0.0)
        }

        self.sub = self.create_subscription(String, '/cmd', self.handle_command, 10)
        self.pub = self.create_publisher(BotPose, '/bot_pose', 10)
        self.get_logger().info("Navigator State Machine Initialized at North (0,0)")

    def handle_command(self, msg):
        cmd = msg.data
        
        # State Transition Logic (Turning)
        if cmd == "turn right":
            self.current_state_idx = (self.current_state_idx + 1) % 4
        elif cmd == "turn left":
            self.current_state_idx = (self.current_state_idx - 1) % 4
        
        # State-Dependent Execution (Movement)
        current_facing = self.states[self.current_state_idx]
        dx, dy = self.move_map[current_facing]

        if cmd == "forward":
            self.x += dx
            self.y += dy
        elif cmd == "backward":
            self.x -= dx
            self.y -= dy

        self.publish_pose(current_facing)

    def publish_pose(self, facing):
        msg = BotPose()
        msg.x = self.x
        msg.y = self.y
        msg.facing_direction = facing
        self.pub.publish(msg)
        self.get_logger().info(f"State: {facing} | Pos: ({self.x}, {self.y})")

def main():
    rclpy.init()
    rclpy.spin(Navigator())
    rclpy.shutdown()import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sub_interfaces.msg import BotPose

class Navigator(Node):
    def __init__(self):
        super().__init__('navigator')
        self.x, self.y = 0.0, 0.0
        self.dirs = ["North", "East", "South", "West"]
        self.idx = 0  # Facing North
        
        self.sub = self.create_subscription(String, '/cmd', self.callback, 10)
        self.pub = self.create_publisher(BotPose, '/bot_pose', 10)

    def callback(self, msg):
        cmd = msg.data
        if cmd == "turn right": self.idx = (self.idx + 1) % 4
        elif cmd == "turn left": self.idx = (self.idx - 1) % 4
        
        face = self.dirs[self.idx]
        if cmd == "forward":
            if face == "North": self.y += 1.0
            elif face == "East": self.x += 1.0
            elif face == "South": self.y -= 1.0
            elif face == "West": self.x -= 1.0
        
        # Build and publish custom message
        pose = BotPose()
        pose.x = self.x
        pose.y = self.y
        pose.facing_direction = face
        self.pub.publish(pose)
        self.get_logger().info(f"Sub at ({pose.x}, {pose.y}) facing {pose.facing_direction}")

def main():
    rclpy.init()
    rclpy.spin(Navigator())
    rclpy.shutdown()
