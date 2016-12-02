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

light = Light(brick, PORT_4)
turningMotor = Motor(brick, PORT_B)
walkingMotor = Motor(brick, PORT_C)
armMotor = Motor(brick, PORT_A)
touch = Touch(brick, PORT_1)
ultrasonic = Ultrasonic(brick, PORT_2)
compass = Ultrasonic(brick, PORT_3)

#TODO
# calibrate sleep times might need adjusting
# find bin is probably non functional, and VERY necessary (very short range when picking up bin)
# additional bin ID data to get more accurate values
# line follow data

# LINE FOLLOW VARIABLES
turningPower = 70 # 70, motor power used when turning in line follow
negInertiaPower = 65 # 65, motor power for negative inertia
findLineTimeout = 0.5 # 0.5, time between switching motor to the opposite direction
negInertiaLengthOnWhite = 0.2 # 0.2, time before braking on negative inertia when originally on white
negInertiaLengthOnBlack = 0.05 # 0.05, time before braking on negative inertia when originally on black (should be smaller than white to prevent overshooting the line)

# CALIBRATION VARIABLES
calTurningPower = 70 # 70, motor power used to turn when calibrate
calFirstTurnTime = 0.2 # 0.2, time to turn on first turn
calSecondTurnTme = 0.15 # 0.15, time to turn on second turn
calDelta = 10 # no default since it's new, range of light values for which line follow continues going straight (range is 2 * delta)

# BIN PICKUP VARIABLES
binDistance = 8 # 8, ultrasonic reading where PMR stops following line and starts looking for bin
findBinDelta = 3 # 3, 
pickupMotorPower = 90 # 90, motor power used to pick up bin (and identify it)

# BIN ID VARIABLES
organicCeramicBound = 0.418654 # this is just a bs value atm
ceramicMetallicBound = 0.4403975 # ^

# BIN DROP OFF VARIABLES
compassDelta = 30 # 30, anything outside of this range means we're at a bin drop off
binDropOffStepBuffer = 2 # 2, number of steps taken after seeing a wrong bin drop off
dropOffPowerWithBin = 70 # motor power when setting down bin
dropOffTimeMotorOn = 0.1 # time motor runs before braking
dropOffTimeBrake = 0.05 # time motor is braked
dropOffPowerNoBin = 75 # motor power once bin is on ground
  
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
          
def step(forwardPower = 120):
    walkingMotor.run(forwardPower)
    sleep(.1) # give it time to move off touch sensor
    while not legPosition():
        walkingMotor.run(0)
        walkingMotor.brake()
        return
            
def calibrate():
    # turn on light sensor
    light.set_illuminated(True)
    step(forwardPower)
    
    sleep(0.25)
    
    # calibrates black value
    black = light.get_lightness()
    print("Black = %d" % black)
    
    # turns right ~30 degrees
    turningMotor.run(calTurningPower)
    sleep(calFirstTurnTime)
    turningMotor.run(0)
    turningMotor.brake()
    sleep(.25)
    
    # calibrates white value
    white = light.get_lightness()

    turningMotor.run(-calTurningPower)
    sleep(calSecondTurnTme)
    turningMotor.run(0)
    turningMotor.brake()
    print("White = %d" % white)
    threshold = ( black + white) / 2
    return (threshold)

def findBin():
    n = 0 
    direction = -1
    turningMotor.run(direction * turningPower)
    start = time.time()
    initialDistance = ultrasonic.get_distance()
    lowerDistance = initialDistance - findBinDelta
    while ultrasonic.get_distance() < lowerDistance:
        if time.time() - start < findLineTimeOut:
            pass
        elif n == 0:
            start = time.time()
            direction *= -1
            turningMotor.run(direction * turningPower)
            findLineTimeOut *= 2
            n += 1
        elif n == 1:
            start = time.time()
            direction *= -1
            turningMotor.run(direction * turningPower)
            findLineTimeOut *= .5
            n += 1
        else:
            turningMotor.run(0)
            turningMotor.brake()
            return
    turningMotor.run(0)
    turningMotor.brake()
    turningMotor.run(- direction * negInertiaPower)
    sleep(negInertiaLengthOnWhite)
    turningMotor.brake()
    return
    '''
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
    '''
    
def findLine(lowerThreshold, upperThreshold):
    n = 0
    if light.get_lightness() > upperThreshold:
        # white
        direction = -1
        turningMotor.run(direction * turningPower)
        start = time.time()
        while light.get_lightness() > threshold:
            if time.time() - start < findLineTimeOut:
                pass
            elif n == 0:
                start = time.time()
                direction *= -1
                turningMotor.run(direction * turningPower)
                findLineTimeOut *= 2
                n += 1
            elif n == 1:
                start = time.time()
                direction *= -1
                turningMotor.run(direction * turningPower)
                findLineTimeOut *= .5
                n += 1
            else:
                turningMotor.run(0)
                turningMotor.brake()
                return
        turningMotor.run(0)
        turningMotor.brake()
        turningMotor.run(- direction * negInertiaPower)
        sleep(negInertiaLengthOnWhite)
        turningMotor.brake()
        return
    else:
        # black
        direction = 1
        turningMotor.run(direction * turningPower)
        start = time.time()
        while light.get_lightness() < lowerThreshold:
            if time.time() - start < findLineTimeOut:
                pass
            elif n == 0:
                start = time.time()
                direction *= -1
                turningMotor.run(direction * turningPower)
                findLineTimeOut *= 2
                n += 1
            elif n == 1:
                start = time.time()
                direction *= -1
                turningMotor.run(direction * turningPower)
                findLineTimeOut *= .5
                n += 1
            else:
                turningMotor.run(0)
                turningMotor.brake()
                return
        turningMotor.run(0)
        turningMotor.brake()
        turningMotor.run(power = - direction * negInertiaPower)
        sleep(negInertiaLengthOnBlack)
        turningMotor.run(0)
        turningMotor.brake()
        return
        
def lineFollow(lowerThreshold, upperThreshold):
    step()
    findLine(lowerThreshold, upperThreshold)
    return
    
def binPickup():
    start = time.time()
    startPos = armMotor.get_tacho().tacho_count
    armMotor.run(-pickupMotorPower)
    while abs(armMotor.get_tacho().tacho_count - startPos) < 100:
        pass
    armMotor.brake()
    diff = time.time() - start
    return diff

def binID():
    timeDifference = binPickup()
    if timeDifference < organicCeramicBound:
        binIdentity = 1
    elif timeDifference < ceramicMetallicBound:
        binIdentity = 2
    else:
        binIdentity = 3
    return(binIdentity)
    
def binDropOff():
    while abs(armMotor.get_tacho().tacho_count - startPos) > 40:
        armMotor.run(dropOffPowerWithBin)
        sleep(dropOffTimeMotorOn)
        armMotor.brake()
        sleep(ropOffTimeBrake)
    
    armMotor.run(dropOffPowerNoBin)
    while not armPosition():
        pass
    armMotor.idle()
    step(-forwardPower)
    return
    
def main():
    threshold = calibrate()
    lowerThreshold = threshold - delta
    upperThreshold = threshold + delta
    while True:
        while sonar.get_distance() > binDistance:
            lineFollow(lowerThreshold, upperThreshold)
        
        while ultrasonic.get_distance() < 3:
            findBin()
            step()
        binIdentity = binID() # picks up bin and returns what it is (1 for organic, 2 for ceramic, 3 for metallic)
        hasBin = True
        n = 0 # no bin drop off locations have been found yet
        initialCompass = compass.get_distance()
        compassUpper = initialCompass + compassDelta
        compassLower = initialCompass - compassDelta
        while hasBin:
            if compassLower < compass.get_distance() < compassUpper:
                lineFollow()
            else:
                n += 1 # bin drop off location found
                if n == binIdentity:
                    binDropOff()
                    hasBin = False
                else:
                    for i in range(binDropOffStepBuffer): # don't want to register the same bin drop off location twice, may not be necessary
                        lineFollow()
