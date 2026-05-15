#!/usr/bin/env python3

## Python program to read serial input from connected modules
## and publish the output to corresponding topics
## Author: Jasper Yeend (a1901955)
## Date Created: 28.04.2026
## Last Modified: 15.05.2026

import rclpy
import serial, time, os
from rclpy.node import Node
from std_msgs.msg import String
from . import serial_processor


## Note: In current program, only devices connected on initialisation will function.
## I will change this when I work out how to do it (potentially with threading).

# Array of serial ports 5 total for 5 possible modules (Assumes all use standard Arduino format /dev/ttyACMx)
SERIALINPUTS = ['/dev/ttyACM0', '/dev/ttyACM1', '/dev/ttyACM2', '/dev/ttyACM3', '/dev/ttyACM4']
## Note to self: will need to enable serial reading on the Pi for non-root user

# Saves the module info file (modules.txt) within this directory
module_file = os.path.join(os.path.dirname(__file__), "modules.txt")

# Starting the serial connection
arduino_serial = serial_processor.StartSerial(SERIALINPUTS)

# Clearing old serial from buffer
serial_processor.ClearSerial(arduino_serial, SERIALINPUTS)

# Defining the serial publisher
class SerialPublisherNode(Node):

    # Publisher startup commands
    def __init__(self):
        """Publisher definition."""

        # Naming the serial publisher
        super().__init__("serial_publisher")

        # Creating publisher dictionary
        self.publisher_list = {}

        # Finding all topics listed in module info file
        topics = serial_processor.FindTopics(module_file)

        # Creating all topics
        for topic in topics:
            self.publisher_list[topic] = self.create_publisher(String, topic, 10)    

        # Timer for polling serial output
        self.timer_ = self.create_timer(0.1, self.send_serial)

        # Status message on start
        self.get_logger().info("Script is live!")
    
    # Publishing each timer cycle
    def send_serial(self):
        """"Sends a serial output each timer cycle."""

        # Reading the serial input
        serial_input = serial_processor.SerialCheck(arduino_serial, SERIALINPUTS)

        # Checks if the serial input is valid
        if serial_input:
            self.get_logger().info(serial_input)
            # Determining which module is being sent
            module_number = serial_processor.FindModule(serial_input)

            # Finding all topics and pins for given module
            module_data = serial_processor.CheckUnit(module_file, module_number)
            
            # Checking serial and publishing information
            for i in range(len(module_data)):
                pin, topic = module_data[i]
                if serial_input[pin+1] == '1':
                    to_basestation = String()
                    to_basestation.data = '1'
                    self.publisher_list[topic].publish(to_basestation)
                    


# Main function for publisher
def main(args=None):

    # Initialising
    rclpy.init(args=args)

    # Defining node
    node = SerialPublisherNode()
    
    # Spinning node
    rclpy.spin(node)

    # Shutdown
    rclpy.shutdown()