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
from nxt.sensor import Touch, PORT_4, PORT_3, PORT_2, Light, PORT_1

light = Light(brick, PORT_1)
turningMotor = Motor(brick, PORT_B)
walkingMotor = Motor(brick, PORT_C)
legPosition = Touch(brick, PORT_3)
#ultrasonic = Sonar(brick, PORT_2)

def step(forwardPower):
    print('stepping')
    walkingMotor.run(power = forwardPower)
    sleep(.1)
    while True:
        if legPosition.is_pressed() == True:
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
    turningMotor.turn(40, 80, brake=True, timeout=3, emulate=True)
    
    sleep(0.25)
    
    # calibrates white value
    white = light.get_lightness()
    
    #turns back to start position
    #turningMotor.turn(-40, 80, brake = True, timeout=3, emulate=True)
    print("White = %d" % white)
    return (black,white)

def findLine(turnPower, threshold, black, white, delta, side, n = 0):
    print('turning')
    lightRange = 10
    initialLightness = light.get_lightness()
    minPower = 60
    # determine direction to turn
    if initialLightness < threshold:
        onBlack = 1
    else:
        onBlack = -1
    
    start = time.time()
    
    while True:
        currLightness = light.get_lightness()
        
        if currLightness > white:
            currLightness = white
        elif currLightness < black:
            currLightness = black
        error = currLightness - threshold
        
        #normalize correction value to sensor range
        correction = turnPower * (error) / (white - black)
        
        print(correction)
        if abs(correction) < lightRange:
            print('breaking')
            return
            
        if abs(correction) < minPower:
            if correction < 0:
                correction = -minPower
            else:
                correction = minPower
        print(correction)
		# run motors based on how far off the line PMR is
        turningMotor.run(power = -correction)
        
        #print(currLightness)
        if (onBlack == 1 and currLightness > (threshold - delta)) or (onBlack == -1 and currLightness <= (threshold + delta)):
            turningMotor.brake()
            return
        #elif time.time() - start > 5:
        #    side *= -1
        #    n += 1
        #    findLine(turnPower, threshold, black, white, delta, side, n)
        
def lineFollow():
    forwardPower = 120
    turnPower = 60
    delta = 0
    side = 1 # right
    
    calibrateVal = calibrate()
    black = calibrateVal[0]
    white = calibrateVal[1]
    threshold = (black + white) / 2
    
    while True:
        step(forwardPower)
        findLine(turnPower, threshold, black, white, delta, side)
    turningMotor.idle()
    walkingMotor.idle()
             
lineFollow()
