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
        
def step(forwardPower):
    #print('stepping')
    walkingMotor.run(power = forwardPower)
    sleep(.1)
    while True:
        if legPosition:
            walkingMotor.run(power = 0)
            walkingMotor.brake()
            return
            
def calibrate():
    # turn on light sensor
    light.set_illuminated(True)
    step(90)
    
    sleep(0.25)
    
    # calibrates black value
    black = light.get_lightness()
    print("Black = %d" % black)
    
    # turns right ~30 degrees
    turningMotor.run(power = 60)
    sleep(0.2)
    turningMotor.brake()
    sleep(.5)
    
    # calibrates white value
    white = light.get_lightness()

    turningMotor.run(power = -60)
    sleep(.15)
    turningMotor.brake()
    print("White = %d" % white)
    threshold = ( black + white) / 2
    return (black, white, threshold)
    
def findLine(threshold, black, white):
    timeOut = .5
    turningPower = 60
    n = 0
    #print('turning')
    if light.get_lightness() < threshold:
        #print('On black')
        direction = 1
        turningMotor.run(power = turningPower)
        start = time.time()
        while light.get_lightness() < threshold:
            if time.time() - start < timeOut:
                pass
            elif n == 0:
                start = time.time()
                turningMotor.run(power = -turningPower)
                timeOut *= 2
                #print("1st time")
                n += 1
            elif n == 1:
                start = time.time()
                turningMotor.run(power = turningPower)
                timeOut *= .5
                #print("2nd time")
                n += 1
            else:
                #print("return")
                turningMotor.brake()
                return
        turningMotor.brake()
        turningMotor.run(power = -65)
        sleep(.05)
        turningMotor.brake()
        return
    else:
        #print('On white')
        turningMotor.run(power = -turningPower)
        #print('turn left')
        start = time.time()
        direction = -1
        while light.get_lightness() > threshold:
            #print(light.get_lightness())
            if time.time() - start < timeOut:
                pass
            elif n == 0:
                start = time.time()
                turningMotor.run(power = turningPower)
                timeOut *= 2
                #print("1st time")
                n += 1
            elif n == 1:
                start = time.time()
                turningMotor.run(power = -turningPower)
                timeOut *= .5
                #print("2nd time")
                n += 1
            else:
                #print("return")
                turningMotor.brake()
                return
        turningMotor.brake()
        turningMotor.run(power = 65)
        #print('ant')
        sleep(.2)
        turningMotor.brake()
        return

def lineFollow(threshold, black, white):
    forwardPower = 120
    step(forwardPower)
    findLine(threshold, black, white)
    return

calVals = calibrate()
black = calVals[0]
white = calVals[1]
threshold = calVals[2]
while True:
    findLine(black, white, threshold)
