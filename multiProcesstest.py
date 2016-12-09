import nxt
import nxtConnect # has to be in search path
import time
import random
from multiprocessing import Process


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

from multiprocessing import Process, Value

from nxt.motor import Motor, PORT_A, PORT_B, PORT_C
from nxt.sensor import Touch, PORT_4, PORT_3, PORT_2, Light, PORT_1, Ultrasonic

light = Light(brick, PORT_4)
turningMotor = Motor(brick, PORT_B)
walkingMotor = Motor(brick, PORT_C)
armMotor = Motor(brick, PORT_A)
touch = Touch(brick, PORT_1)
ultrasonic = Ultrasonic(brick, PORT_2)
compass = Ultrasonic(brick, PORT_3)

def getLight():
    while True:
        currReading = light.get_lightness()
        print('Light: %.0f' %currReading)

def getSonar():
    while True:
        currSonar = ultrasonic.get_distance()
        print('Sonar: %.0f' %currSonar)

p1 = Process(target=getLight)
p1.start()
p2 = Process(target=getSonar)
p2.start()
