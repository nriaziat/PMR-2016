#!/usr/bin/env python

'''
This is an nxt-python example program to illustrate how to connect to
the NXT and control its ports (motors / sensors)
Requirements:
    1) Motor connected to Port A
    2) Touch sensor connected to Port 1
    
Note 1: Run as 'python example.py' (NOT pyhton3!)
Note 2: Use 'sudo python example.py' to use the USB connection

Author: Michael Fruhnert, 05-Sep 2016
'''

#######################################################################
## First you need to connect to your NXT
#######################################################################

import nxt
import nxtConnect # has to be in search path

brickName = "TeamXX"
useUSB = False

if useUSB:
    brick = nxt.find_one_brick(
        name = brickName,
        strict = True,
        method = nxt.locator.Method(usb = True, bluetooth = True))
else:
    # the bluetooth function of the nxt library works too, but "wastes"
    # time searching for devices.
    brick = nxtConnect.btConnect(brickName)
    
print(brick.get_device_info()) # check what brick you connected to

#######################################################################
## Then, you can specify what you want the NXT to do
#######################################################################
from time import sleep

# see files in library ( /usr/local/lib/python2.7/dist-packages/nxt )
# for a more comprehensive list of ports / commands available 
from nxt.motor import Motor, PORT_A, PORT_B, PORT_C
from nxt.sensor import Light, Sound, Touch, Ultrasonic
from nxt.sensor import PORT_1, PORT_2, PORT_3, PORT_4

# use try with finally to stop motors at end, even if program
# encountered an (programming) error.
try:
    touchSensor = Touch(brick, PORT_1) # plug touch sensor into Port 1
    motor = Motor(brick, PORT_A) # plug motor into Port A
    
    # Note: |Power| <50 might not be strong enough to turn motor / 
    # overcome the internal friction
    motor.run(power = 70) # go forward
    sleep(2.5) # let NXT do its thing for 2.5 seconds
    motor.run(power = -70) # go backward
    sleep(2)
    
    # will read when this line of code is reached, so KEEP sensor
    # pressed till then
    print("Current touch sensor state: {}".format(
            touchSensor.get_sample()))
    
finally:
    Motor(brick, PORT_A).idle() # otherwise motor keeps running
    print("Terminating Program")
    brick.sock.close()
