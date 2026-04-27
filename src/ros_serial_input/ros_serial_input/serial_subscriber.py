#!/usr/bin/env python3


import rclpy
from rclpy.node import Node
from std_msgs.msg import String



class SerialSubscriberNode(Node):

    def __init__(self):
        super().__init__("serial_subscriber")
        self.cmd_ser_sub_ = self.create_subscription(
            String, "serialOut", self.serial_print, 10)
        self.get_logger().info("Script is live!")


    def serial_print(self, msg: String):
        self.get_logger().info(str(msg))

def main(args=None):

    rclpy.init(args=args)
    node = SerialSubscriberNode()
    rclpy.spin(node)

    rclpy.shutdown()