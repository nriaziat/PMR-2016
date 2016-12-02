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
from nxt.sensor import Touch, PORT_4, PORT_3, PORT_2, Light, PORT_1, Ultrasonic

#from basicFunctions import step, calibrate

#light = Light(brick, PORT_1)
#turningMotor = Motor(brick, PORT_B)
#walkingMotor = Motor(brick, PORT_C)
armMotor = Motor(brick, PORT_A)

def binID():
    start = time.time()
    '''
    init = brick.get_battery_level()
    maxVal = init
    minVal = init
    '''
    sumVal = 0
    n = 0
    print('starting')
    while time.time() - start < 3:
        currVal = brick.get_battery_level()
        sumVal += currVal
        n += 1
        '''
        if currVal > maxVal:
            maxVal = currVal
        elif currVal < minVal:
            minVal = currVal
        '''
    brick.play_tone_and_wait(250, 250)
    mean = sumVal / n
    return(mean)

def repeater():
    sumVal = 0
    n = 0
    userInput = ''
    armMotor.brake()
    while n < 10:
        noLoad = binID()
        repeat = raw_input('Add bin')
        withLoad = binID2()
        diff = noLoad - withLoad
        print(noLoad, withLoad, diff)
        sumVal += diff
        n += 1
        print(n)
        userInput = raw_input('Again?\n')
    brick.play_tone_and_wait(500, 250)
    mean = sumVal / n
    print(mean)


repeater()
