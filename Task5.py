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

light = Light(brick, PORT_1)
turningMotor = Motor(brick, PORT_B)
walkingMotor = Motor(brick, PORT_C)
armMotor = Motor(brick, PORT_A)
legPosition = Touch(brick, PORT_3)
ultrasonic = Ultrasonic(brick, PORT_4)

def step(forwardPower):
    #print('stepping')
    walkingMotor.run(power = forwardPower)
    sleep(.1)
    while True:
        if legPosition.is_pressed() == True:
            walkingMotor.run(power = 0)
            walkingMotor.brake()
            return
            
def lineFollow():
    step(120)
    pass

def taskFive():
    '''calVals = calibrate()
    black = calVals[0]
    white = calVals[1]
    threshold = calVals[2]'''
    
    while True:
        print(ultrasonic.get_distance())
        if ultrasonic.get_distance() > 12:
            #lineFollow(threshold, black, white)
            lineFollow()
        else:
        
            step(90)
            step(90)
            step(90)
            sleep(.5)
            print("picking up")
            armMotor.run(power = -80)
            sleep(.5)
            armMotor.brake()
            sleep(.5)
            turningMotor.turn(60, 200)
            start = time.time()
            while time.time() - start < 3:
                lineFollow()
            print("setting down")
            armMotor.run(power = 70)
            sleep(.7)
            armMotor.idle()
            step(-120)
            step(-120)
            step(-120)
            step(-120)
            step(-120)
            step(-120)
            
            break
