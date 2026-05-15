#!/usr/bin/env python3

## Python program containing serial functions
## used by the serial_publisher
## Author: Jasper Yeend (a1901955)
## Date Created: 5.05.2026
## Last Modified: 9.05.2026

import serial, time, os


def StartSerial(SERIALINPUTS)->serial:
    """Initiates the serial connection between arduino's and the Pi."""

    # Empty serial array to hold established connections
    arduino_serial =  [0] * len(SERIALINPUTS)


    # Establishing connection to valid serial ports
    for i, serial_device in enumerate(SERIALINPUTS):

        # Checks if serial device is connected
        if os.path.exists(serial_device):

            # Starts the device
            arduino_serial[i] = serial.Serial(serial_device, 9600, timeout = 1)

    # Wait time to allow arduinos to initialise
    time.sleep(2)
    return arduino_serial
    

def ClearSerial(arduino_serial, SERIALINPUTS)->None:
    """Clears old serial messages from buffer."""
    
    for i, serial_device in enumerate(SERIALINPUTS):
        if os.path.exists(serial_device):
            arduino_serial[i].reset_input_buffer()
            arduino_serial[i].reset_output_buffer()


def SerialCheck(arduino_serial, SERIALINPUTS):
    """Checks serial input from all connected devices."""
    # Checks all devices
    for i, serial_device in enumerate(SERIALINPUTS):

        # Checks if serial device is connected (prevents errors if a disconnect occurs)
        if os.path.exists(serial_device):

            # Reads input as line. Inputs are all printed in form A00000000000000000000|0 0 0 0 0 0
            # corresponding to the identifier, digital port status on the arduino, and 5 analog port status
            serial_input = arduino_serial[i].readline()
            return serial_input.decode("utf-8", errors='ignore')
        

def FindModule(serial_input)->chr:
    """Returns the input module."""
    return(serial_input[0])


# Unfinished code for parsing specific modules (once more than just digital inputs come in)
def ParseSerial(serial_input, module_number, col, OUTPUTS)->str:
    
    match module_number:
        case 0: # module A

            # Pushbutton Check
            if col < 6 and serial_input[col+3] == 1:
                return '1'
            else:
                return '0'
            

def CheckUnit(file_name, module):
    """Returns an array of pins and corresponding topics for a given module."""
    
    # Reading the file
    with open(file_name, 'r') as file:
        content = file.read()

    # Positioning index at module in file    
    index = content.find('UNIT ' + module + ':')
    index += 8

    buttonArray = []

    # Checking for all possible topics
    while index < len(content) and content[index] == '/':
        index += 2

        #  Finding topic name
        name = '/' + module
        while content[index] != ':':
            name = name + content[index]
            index += 1

        # Finding corresponding pin
        pin = ''
        while content[index] != '\n':
            if content[index].isdigit():
                pin = pin + content[index]
            index += 1

        # Appending to output array
        buttonArray.append([int(pin), name])
        
        index += 1

    # Returns array of module data    
    return buttonArray


def FindTopics(file_name):
    """Returns an array of all required publisher topics from txt file."""

    # Reading the file
    with open(file_name, 'r') as file:
        content = file.read()

    # Sets index at start    
    index = 0
    publisher_array = []

    # Checks index is within text range
    while index < len(content):

        # Checks for new topic
        if content[index] == '/':
            name = ''

            # Reads topic name
            while content[index] != ':':
                name += content[index]
                index += 1

            # Appends topic name
            publisher_array.append(name)
        index += 1

    # Returns all topic names
    return publisher_array
