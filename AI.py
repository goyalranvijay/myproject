#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class ainode(Node):
    def __init__(self):
        super().__init__("AI")

        self.pub1 = self.create_publisher(String, "/AI2VCU", 10)
        self.timer = self.create_timer(1.0, self.timer_cb)
        self.sub2=self.create_subscription(String,"/VCU2AI",self.i_heardvcu,10)

    def timer_cb(self):
        msg = String()
        msg.data = "HI"
        self.pub1.publish(msg)
        self.get_logger().info("ALIVE::HI")
    def i_heardvcu(self, msg):
        self.get_logger().info("Thank God You Are Alive")

def main(args=None):
    rclpy.init(args=args)
    node = ainode()
    rclpy.spin(node)
    rclpy.shutdown()
