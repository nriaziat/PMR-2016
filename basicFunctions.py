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

light = Light(brick, PORT_1)
turningMotor = Motor(brick, PORT_B)
walkingMotor = Motor(brick, PORT_C)
armMotor = Motor(brick, PORT_A)
legPosition = Touch(brick, PORT_3)
ultrasonic = Ultrasonic(brick, PORT_4)


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
    if not legPosition.is_pressed:
        step(90)
    
    sleep(0.25)
    
    # calibrates black value
    black = light.get_lightness()
    print("Black = %d" % black)
    
    # turns right ~30 degrees
    turningMotor.turn(60, 80, brake=True, timeout=3, emulate=True)
    
    sleep(0.25)
    
    # calibrates white value
    white = light.get_lightness()
    
    #turns back to start position
    #turningMotor.turn(-40, 80, brake = True, timeout=3, emulate=True)
    print("White = %d" % white)
    threshold = ( black + white) / 2
    return (black, white, threshold)

def findLine(turnPower, threshold, black, white):
    print('turning')
    initialLightness = light.get_lightness()
    timeOut = .5

    # determine direction to turn
    if initialLightness < threshold:
        onBlack = 1
    else:
        onBlack = -1
    
    start = time.time()
    
    turningMotor.run(power = -onBlack * turnPower)
    
    n = 0
    
    while True:
        currLightness = light.get_lightness()
      
        #print(currLightness)
        if (onBlack == 1 and currLightness > threshold) or (onBlack == -1 and currLightness <= threshold):
            turningMotor.brake()
            return
        elif time.time() - start > timeOut:
            n += 1
            print(n)
            if n == 2:
                start = time.time()
                while time.time() - start > 2 * timeOut:
                    turningMotor.run(power = onBlack * turnPower)
            elif n == 3:
                return
            turningMotor.run(power = onBlack * turnPower)
            print('timeOut')
            start = time.time()           
        
def lineFollow(threshold, black, white):
    forwardPower = 90
    turnPower = 60
    step(forwardPower)
    findLine(turnPower, threshold, black, white)
    
def binPickup():
    #move forward slowly
    step(80)
    #stop
    identity = binID()
    return(identity)
    
def binID():
    initialPos = armMotor.get_tacho().tacho_count
    startTime = time.time()
    armMotor.run(power = -85)
    while abs(armMotor.get_tacho().tacho_count - initialPos) < 70:
        pass
    armMotor.brake()
    finalTime = time.time() - startTime
    print(finalTime)
    '''n = 40
    initialPos = armMotor.get_tacho().tacho_count
    print(initialPos)
    while n < 124:
        armMotor.run(-n)
        if abs(armMotor.get_tacho().tacho_count - initialPos) > 120:
            print('done')
            #armMotor.turn(-n, 120)
            break
        else:
            n += 1
    print(n)
    armMotor.brake()
    '''      
    if finalTime < .3: #organic and ceramic are ~ the same time at power -85, maybe try a lower motor power first
        #beep a shitton
        binIdentity = 'Organic Bin'
    elif finalTime < .38:
        #beep also a shitton
        binIdentity = 'Ceramic Bin'
    else:
        # beep a lot of tons of shit
        binIdentity = 'Metal Bin'
        
    return(binIdentity)
    
def binDropOff():
    
    #stop
    #turn 90
    #drop bin
    #backoff
    #turn -90
    return
    
def ultrasonicCleaner():
    if not minDistance < ultrsonic.get_distance() < maxDistance:
        distance = 0
    return distance
    

def main():
    calVals = calibrate()
    black = calVals[0]
    white = calVals[1]
    threshold = calVals[2]
    while True:
        if ultrasonic.get_distance() > binHeight:
            lineFollow(threshold, black, white)
        elif binDropOffTouch.is_preseed():
            binDropOff()
        else:
            n = 0
            start = time.time()
        
            # clean data to make sure theres a bin
            while time.time() - start < .5:
                sumDist += ultrasonic.get_distance() 
                n += 1
            sumDist /= n
            
            if sumDist < maxDistance:
                identity = binPickup()
                print('Bin Identified: ', identity)
#print(binID())
