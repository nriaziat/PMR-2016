import nxt
import nxtConnect # has to be in search path
import time
import random

brickName = "Team60"
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
from time import sleep

from nxt.motor import Motor, PORT_A, PORT_B, PORT_C
from nxt.sensor import Touch, PORT_4, PORT_3, PORT_2, Light, PORT_1, Ultrasonic

light = Light(brick, PORT_4)
turningMotor = Motor(brick, PORT_B)
walkingMotor = Motor(brick, PORT_C)
armMotor = Motor(brick, PORT_A)
touch = Touch(brick, PORT_1)
ultrasonic = Ultrasonic(brick, PORT_2)
compass = Ultrasonic(brick, PORT_3)

#turningMotor.run(70)


def legPosition():
    touchState = touch.get_input_values().calibrated_value
    if touchState == 829 or touchState == 810:
        return True
    else:
        return False
        
def step(forwardPower = 120):
    walkingMotor.run(forwardPower)
    sleep(.2) # give it time to move off touch sensor
    while not legPosition():
        pass
    walkingMotor.run(0)
    walkingMotor.brake()
    return

outFile = open('compassValueswithMagnet.txt', 'w')
try:
    while True:
        step()
        compassVal = compass.get_distance()
        outFile.write('%f\n' % compassVal)
        print(compassVal)
            
except:
    outFile.close()
    walkingMotor.idle()
    
