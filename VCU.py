#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class vcunode(Node):

    def __init__(self):
        super().__init__("VCU")

        self.sub1 = self.create_subscription(String,"/AI2VCU",self.i_heard,10)
        self.pub2=self.create_publisher(String,"/VCU2AI",10)
 
    def i_heard(self, msg):
        self.get_logger().info("Thank God You Are Alive")
        self.get_logger().info(f"VCU received: {msg.data}")
    def timer_calacklb(self):
        msg = String()
        msg.data = "HI"
        self.pub2.publish(msg)
        self.get_logger().info("VCU alive too")

def main(args=None):
    rclpy.init(args=args)
    node = vcunode()
    rclpy.spin(node)
    rclpy.shutdown()
