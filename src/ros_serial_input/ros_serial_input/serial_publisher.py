#!/usr/bin/env python3

## Python program to read serial input from connected modules
## and publish the output to the "serialOut" node
## Author: Jasper Yeend (a1901955)
## Date Created: 28.04.2026
## Last Modified: 28.04.2026

import rclpy
import serial, time, os
from rclpy.node import Node
from std_msgs.msg import String


## Note: In current program, only devices connected on initialisation will function.
## I will change this when I work out how to do it (potentially with threading).
## Second Note: There is a weird bug where the arduino code sometimes outputs
## HIGH on pins 1 - 4 in the first 1 - 2 serial comms despite these being LOW.
## This only occurs on one arduino I've tested on, and I have to assume it is some
## sort of initialisation bug. Will potentially scrap first few inputs to rectify.



# Is combining the pyserial and publisher into one piece of code an affront to man? Yes. 
# Am I bothered to change it? Probably not.



# Array of serial ports 5 total for 5 possible modules (Assumes all use standard Arduino format /dev/ttyACMx)
SERIALINPUTS = ['/dev/ttyACM0', '/dev/ttyACM1', '/dev/ttyACM2', '/dev/ttyACM3', '/dev/ttyACM4']
## Note to self: will need to enable serial reading on the Pi for non-root user

# Empty serial array to hold established connections
arduinoSerial =  [0] * len(SERIALINPUTS)


# Establishing connection to valid serial ports
for i, serialDevice in enumerate(SERIALINPUTS):

    # Checks if serial device is connected
    if os.path.exists(serialDevice):

        # Starts the device
        arduinoSerial[i] = serial.Serial(serialDevice, 9600, timeout = 1)

# Wait time to allow arduinos to initialise
time.sleep(2)


# Clears old serial messages from buffer
for i, serialDevice in enumerate(SERIALINPUTS):
    if os.path.exists(serialDevice):
        arduinoSerial[i].reset_input_buffer()
        arduinoSerial[i].reset_output_buffer()



# Defining the serial publisher
class SerialPublisherNode(Node):


    # Publisher startup commands
    def __init__(self):

        # Naming the serial publisher
        super().__init__("serial_publisher")

        # Creating the serial publisher. Any subscribers should use
        # the serialOut node (ill rename this to be more specific later)
        self.cmd_ser_pub_ = self.create_publisher(String, "serialOut", 10)
        
        # Timer for polling serial output
        self.timer_ = self.create_timer(0.1, self.send_serial)

        # Status message on start
        self.get_logger().info("Script is live!")
    
    # Publishing each timer cycle
    def send_serial(self):

        # Checks all devices
        for i, serialDevice in enumerate(SERIALINPUTS):

            # Checks if serial device is connected (prevents errors if a disconnect occurs)
            if os.path.exists(serialDevice):

                # Reads input as line. Inputs are all printed in form A00000000000000000000|0 0 0 0 0 0
                # corresponding to the identifier, digital port status on the arduino, and 5 analog port status
                serialInput = arduinoSerial[i].readline()

                ## If a line was sent, prints the line (for testing)
                if serialInput:
                    # Defines msg to Ros type String
                    msg = String()

                    # Fetches msg data from serialInput
                    msg.data = serialInput.decode("utf-8", errors='ignore')
                    
                    # Publishes message to serialOut node
                    self.cmd_ser_pub_.publish(msg)


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