#!/usr/bin/env python3


import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import sys

## This is just a test file so I havent added comments


def ask_topic(prompt="Enter topic to subscribe to: "):
    """Asking which topic to subscribe to"""
    return input(prompt).strip()


class SerialSubscriberNode(Node):

    def __init__(self, topic):
        super().__init__("serial_subscriber")
        self.cmd_ser_sub_ = self.create_subscription(
            String, topic, self.serial_print, 10)
        self.get_logger().info("Script is live!")


    def serial_print(self, msg: String):
        self.get_logger().info(str(msg))

def main(args=None):
    topic = ask_topic()
    rclpy.init(args=args)
    node = SerialSubscriberNode(topic)
    rclpy.spin(node)

    rclpy.shutdown()