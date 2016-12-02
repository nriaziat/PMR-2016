
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

#from basicFunctions import step, calibrate

light = Light(brick, PORT_4)
turningMotor = Motor(brick, PORT_B)
walkingMotor = Motor(brick, PORT_C)
armMotor = Motor(brick, PORT_A)
touch = Touch(brick, PORT_1)
#ultrasonic = Ultrasonic(brick, PORT_2)
#compass = Ultrasonic(brick, PORT_3)

def legPosition():
    touchState = touch.get_input_values().calibrated_value
    if touchState == 829 or touchState == 810:
        return True
    else:
        return False
        
def armPosition():
    touchState = touch.get_input_values().calibrated_value
    if touchState == 995 or touchState == 810:
        return True
    else:
        return False

def legsDown():
    walkingMotor.run(120)
    init = brick.get_battery_level()
    while brick.get_battery_level() > init - 700:
        pass
    walkingMotor.brake()
            
def binPickup():
    start = time.time()
    startPos = armMotor.get_tacho().tacho_count
    armMotor.run(-90)
    while abs(armMotor.get_tacho().tacho_count - startPos) < 100:
        pass
    armMotor.brake()
    diff = time.time() - start
    sleep(0.5)
    
    while abs(armMotor.get_tacho().tacho_count - startPos) > 40:
        armMotor.run(70)
        sleep(.1)
        armMotor.brake()
        sleep(0.05)
    
    armMotor.run(75)
    
    while not armPosition():
        pass
    armMotor.idle()
    return diff

def binID():
    timeDifference = binPickup()
    if timeDifference < .418654:
        binIdentity = 'organic'
    elif timeDifference < .4403975:
        binIdentity = 'ceramic'
    else:
        binIdentity = 'metallic'
    return(binIdentity, timeDifference)

def getBinType():
    num = random.randint(1,3)
    if num == 1:
        binType = 'organic'
    elif num == 2:
        binType = 'ceramic'
    else:
        binType = 'metallic'
    return binType
    
def main():
    n = 0
    successes = 0
    repeat = ''
    while repeat == '':
        print(brick.get_battery_level())
        binType = getBinType()
        print(binType)
        repeat = raw_input('Repeat?')
        rawVals = binID()
        binIdentity = rawVals[0]
        diff = rawVals[1]
        if binType == binIdentity:
            successes += 1
            print('success')
        else:
            print('failure')
        n += 1
        print(float(successes) / float(n))
    return
    

'''
while True:
    print(brick.get_battery_level())
    print(binID())
    raw_input()
'''
main()

