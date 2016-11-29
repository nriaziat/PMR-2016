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
ultrasonic = Ultrasonic(brick, PORT_2)
compass = Ultrasonic(brick, PORT_4)

def step(forwardPower):
    #print('stepping')
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
    turningMotor.run(power = 70)
    sleep(0.2)
    turningMotor.brake()
    sleep(.5)
    
    # calibrates white value
    white = light.get_lightness()

    turningMotor.run(power = -70)
    sleep(.15)
    turningMotor.brake()
    print("White = %d" % white)
    threshold = ( black + white) / 2
    return (black, white, threshold)

def compassCal():
    startPos = turningMotor.get_tacho().tacho_count
    print(startPos)
    currPos = startPos
    turningMotor.run(70)
    minVal = compass.get_distance()
    maxVal = minVal
    start = time.time()
    while abs(currPos - startPos) > 5 and time.time() - start < .2:
        currPos = turningMotor.get_tacho().tacho_count
        print(currPos)
        currCompass = compass.get_distance()
        print(currPos, currCompass)
        if currCompass > maxVal:
            maxVal = currCompass
        elif currCompass < minVal:
            minVal = currCompass
    turningMotor.run(0)
    turningMotor.idle()
    print(minVal, maxVal)
    return minVal, maxVal
    
def findBin():
    timeOut = .5
    turningPower = 60
    n = 0
    turningMotor.run(power = turningPower)
    start = time.time()
    print('scan')
    direction = 1
    while ultrasonic.get_distance() > 15:
        if time.time() - start < timeOut:
            pass
        elif n == 0:
            start = time.time()
            direction *= -1
            turningMotor.run(power = -turningPower)
            timeOut *= 2
            #print("1st time")
            n += 1
        elif n == 1:
            start = time.time()
            turningMotor.run(power = turningPower)
            timeOut *= .5
            direction *= -1
            #print("2nd time")
            n += 1
        else:
            #print("return")
            turningMotor.brake()
            return "1"
    turningMotor.brake()
    turningMotor.run(power = -70 * direction)
    sleep(.0875)
    turningMotor.brake()
    return
    
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
        turningMotor.run(power = 65)
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
        turningMotor.run(power = -65)
        #print('ant')
        sleep(.2)
        turningMotor.brake()
        return
    

    '''
    print('turning')
    initialLightness = light.get_lightness()
    timeOut = .5

    # determine direction to turn
    if initialLightness < threshold:
        onBlack = 1
    else:
        onBlack = -1
    
    start = time.time()
    
    turningMotor.run(power = onBlack * turnPower)
    
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
    '''

def lineFollow(threshold, black, white):
    forwardPower = 120
    step(forwardPower)
    findLine(threshold, black, white)
    
def binPickup():
    while ultrasonic.get_distance() > 6 and ultrasonic.get_distance() < 240:
        step(90)
    step(90)
    sleep(1)
    print("picking up")
    binIdentity = binID()
    return(binIdentity)
    
def binID():
    
    initialPos = armMotor.get_tacho().tacho_count
    startTime = time.time()
    armMotor.run(power = -85)
    while abs(armMotor.get_tacho().tacho_count - initialPos) < 90 and time.time() - startTime < .51:
        pass
    finalTime = time.time() - startTime
    armMotor.brake()
    print(finalTime)
    
    if finalTime < .31:
        binIdentity = 'organic'

    elif finalTime < .36:
        binIdentity = 'ceramic'

    else:
        binIdentity = 'metal'

    return(binIdentity)
    
def binDropOff():
    
    armMotor.run(50)
    sleep(1)
    armMotor.idle()
    
    return

def taskOne():
    while True:
        try:
            walkingMotor.run(power = 120)
        except KeyboardInterrupt:
            armMotor.idle()
            turningMotor.idle()
            walkingMotor.idle()
            return
    
def taskTwo():
    calVals = calibrate()
    black = calVals[0]
    white = calVals[1]
    threshold = calVals[2]
    while True:
        try:
            lineFollow(threshold, black, white)
        except KeyboardInterrupt:
            armMotor.idle()
            turningMotor.idle()
            walkingMotor.idle()
            break
    return        
       
def taskFour():
    binHeight = 12
    
    calVals = calibrate()
    black = calVals[0]
    white = calVals[1]
    threshold = calVals[2]
    
    initialCompass = compass.get_distance()
    delta = 30
    minVal = initialCompass - delta
    maxVal = initialCompass + delta
    
    while True:
        try:
            compassReading = compass.get_distance()
            if not (minVal < compassReading < maxVal):
                for i in range(3):
                    turningMotor.idle()
                    walkingMotor.idle()
                    brick.play_tone_and_wait(500, 250)
                print('magnet found')
                return
            else:
                lineFollow(threshold, black, white)
                #step(120)
        except KeyboardInterrupt:
            armMotor.idle()
            turningMotor.idle()
            walkingMotor.idle()
            return
 
def taskFive():
    calVals = calibrate()
    black = calVals[0]
    white = calVals[1]
    threshold = calVals[2]
    
    armMotor.run(50)
    sleep(.1)
    armMotor.idle()
    
    while True:
        try:
            print(ultrasonic.get_distance())
            if ultrasonic.get_distance() > 15:
                lineFollow(threshold, black, white)
                #step(120)
            else:
                sleep(.5)
                #c = findBin()
                #if c != 0:
                #    sleep(.5)
                binPickup()
                sleep(.5)
                n = 0
                while n < 10:
                    findLine(threshold,black,white)
                    step(120)
                    n += 1
                print("setting down")
                armMotor.run(power = 70)
                sleep(.5)
                armMotor.idle()
                turningMotor.brake()
                for i in range(6):
                    step(-120)
                    
                brick.play_tone_and_wait(500, 250)
                brick.play_tone_and_wait(800, 250)
                brick.play_tone_and_wait(300, 250)
                brick.play_tone_and_wait(500, 1000)
                brick.play_tone_and_wait(500, 50)
                brick.play_tone_and_wait(500, 50)
                brick.play_tone_and_wait(250, 250)
                break

        except KeyboardInterrupt:
            armMotor.idle()
            walkingMotor.idle()
            turningMotor.idle()
            return

def taskSix():
    try:
        print(binID())
        armMotor.run(60)
        sleep(.1)
        armMotor.idle()
    except KeyboardInterrupt:
        armMotor.idle()
        turningMotor.idle()
        walkingMotor.idle()
    return

def main():
    n = 0
    calibrateVals = calibrate()
    black = calibrateVals[0]
    white = calibrateVals[1]
    threshold = calibrateVals[2]
    
    initialCompass = compass.get_distance()
    delta = 30
    minVal = initialCompass - delta
    maxVal = initialCompass + delta
    
    while True:
        if ultrasonic.getDistance() > 15 and (minVal < compass.get_distance() < maxVal):
            lineFollow(threshold, black, white)
        
        elif ultrasonic.getDistance() <= 15:
            binIdenity = binPickup()
            
        elif binVal < compass.get_distance() < maxVal:
            n += 1
            if binIdentity == 'organic' and n == 1:
                
                binDropOff()
                
            elif binIdentity == 'ceramic' and n == 2:
                
                binDropOff()
                
            elif binIdentity == 'metal' and n == 3:
                
                binDropOff()
            
        
       

    
main()

