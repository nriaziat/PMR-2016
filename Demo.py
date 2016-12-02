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

def constantValues():
    
    # line follow
    forwardPower = 120 # normally at full power, can't thing of any reason we would change this
    turningPower = 70 # typically 70
    return(forwardPower, turningPower)
    
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
        
def lineFollow(threshold, black, white):
    forwardPower = 120
    step(forwardPower)
    findLine(threshold, black, white)
    return
    
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
    return(binIdentity)
    
def main():
	calVals = callibrate()

	# line follow to the loop
	while True:
		lineFollow()
	# just line follow
	# 	I feel like we need a seperate section to differentiate between on the way to the track and on the loop

	# follow loop until we get to the bin place
	while sonar.get_distance() > 8: # random number atm
		lineFollow()
	# line follow until we find a bin

	# grab a bin and figure out what's in it
	binIdentity = binPickup() # I think numerical values would be easiest here: 1 for organic, 2 for ceramic, and 3 for metallic
	# 	we need to convert the bin name into a drop off location at some point, so why not decide it as one (and we can have comments saying what this represents)
	hasBin = True

	# line follow to the right drop off location
	# callibrate compass
	n = 0 # we haven't found any drop off locations yet
	while hasBin:
		if # compass is in range
			lineFollow()
		else:
			n += 1 # we found a bin drop off location
			if n == binID:
				binDropOff()
				hasBin = False
			else:
				for i in range(3): # we don't want to register the same drop off location multiple times
					lineFollow()
	
	# go back and repeat
	#	put the above in a while true loop


# so since we need to do the same thing over and over and over again, I think having it divided like this would be good
def main():
	callibrate()
	# line follow to the loop
	while True:
		lineFollowUntilBin()
		lineFollowUntilDropOff()

def lineFollowUntilBin():
	while sonar.get_distance() > 8: # random number atm
		lineFollow()
	binIdentity = binPickup()

def lineFollowUntilDropOff():

# not sold on doing this anymore since we need to pass the callibration values between each function, probably would be easier to have it in a single while true loop
