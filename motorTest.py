import nxt
import nxtConnect # has to be in search path
import time

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

#from basicFunctions import step, calibrate


turningMotor = Motor(brick, PORT_B)
walkingMotor = Motor(brick, PORT_C)
armMotor = Motor(brick, PORT_A)

def legsDown():
    walkingMotor.run(120)
    init = brick.get_battery_level()
    while brick.get_battery_level() > init - 700:
        pass
    walkingMotor.brake()

repeat = ''
while repeat == '':
    legsDown()
    repeat = raw_input()
