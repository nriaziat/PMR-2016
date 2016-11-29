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

turningMotor = Motor(brick, PORT_B)
walkingMotor = Motor(brick, PORT_C)
armMotor = Motor(brick, PORT_A)
legPosition = Touch(brick, PORT_3)

def step(forwardPower):
    #print('stepping')
    walkingMotor.run(power = forwardPower)
    sleep(.1)
    while True:
        if legPosition.is_pressed() == True:
            walkingMotor.run(power = 0)
            walkingMotor.brake()
            return

def legsDown():
    walkingMotor.run(120)
    init = brick.get_battery_level()
    print('starting')
    while brick.get_battery_level() > init - 1000:
        pass
    walkingMotor.brake()
    return

armMotor.brake()
repeat = ''
#armPower = int(raw_input('Input arm power: '))
'''
while repeat == '':
    legsDown()
    repeat = raw_input()
'''
armMotor.turn(-90, 90, brake = False)

