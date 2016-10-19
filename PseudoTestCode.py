import nxt
import nxtConnect # has to be in search path

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
from nxt.sensor import Light, Touch, Ultrasonic
from nxt.sensor import PORT_1, PORT_2, PORT_3, PORT_4
from nxt.motor import Motor, PORT_A, PORT_B, PORT_C

"""##########################################################################################
################################     IMPORT MOTORS AND SENSORS HERE     ################################
###########################################################################################"""

motorLeft = Motor(brick, PORT_B)
motorRight = Motor(brick, PORT_C)
armMotor = Motor(brick, PORT_A)
light = Light(brick, PORT_3)
touch = Touch(brick, PORT_4)
sonar = Ultrasonic(brick, PORT_2)
led = Light(brick, PORT_1) # experimental

"""########################################################################################"""

def binIdent():
    n = 80
	# incrememnts the motor power down
	#	until the arm falls or kill-switch is pressed
    while n > 10 and not touch.is_pressed():
	
        armMotor.run(power = -n)
		sleep(0.25)
		
		# checks if arm has fallen
        if sonar.get_distance() < 8:
			
			#different end motor powers correspon to different bins
            if n < 20:
			
                print("Bin 1 Picked Up")
                armMotor.idle()
				
            elif n < 60:
			
                print("Bin 2 Picked Up")
                armMotor.idle()
				
            else:
			
                print("Bin 3 Picked Up")
                armMotor.idle()
				
		# if the arm is not down, increment n down
        else:
            n -= 5
			
    armMotor.idle()

	
def sensorValue():
    
    return light.get_lightness() 

	
def calibrate():
    
    light.set_illuminated(True)
	
    motorLeft.reset_position(False)
    motorRight.reset_position(False)
	
    black = sensorValue()
    print("Black = %d" % black)
	
    motorRight.turn(60, 100, brake=True, timeout=1.5, emulate=True)
	
    sleep(0.25)
	
    white = sensorValue()
	
    motorRight.turn(-60, 100, brake = True, timeout=1.5, emulate=True)
	
    print("White = %d" % white)
    return (black,white)
    
	
def lineFollow():
	
	# tune these values for broken and dotted lines
    gain = 75
    pwr = 55
	
    while (sensorValue() > 0) and not (touch.is_pressed()):

        lightness = sensorValue()
        print(sensorValue())
        
        if lightness < black:
            black = lightness
            
        if lightness > white:
            white = lightness
            
        error = lightness - threshold
        correction = (error * gain) / (white - black)
        
        motorRight.run(power = -(pwr + correction))
        motorLeft.run(power = -(pwr - correction))
        
    motorLeft.idle()
    motorRight.idle()
	
	
def binPickup():
	    
    calibrateVal = calibrate()
    black = calibrateVal[0]
    white = calibrateVal[1]
    threshold = (black + white) / 2
    
    if abs(black - white) <= 50:
        print("Calibration Failed. Black and white are not distinct")
        return
        
    print("Threshold = ", threshold)
	
    while touch.is_pressed() == False:
        if sonar.get_distance < 15: 
		
			pos1 = armMotor.get_tacho()
			
			while sonar.get_distance > 10:
				armMotor.run(power = 20)
			armMotor.idle()
			pos2 = armMotor.get_tacho()
			
			delta = pos2 - pos1 
			motorLeft.run(power = 60)
			motorRight.run(power = 60)
			
			sleep(0.25)
			
			motorLeft.brake()
			motorRight.brake()
			
			armMotor.turn(-90, -delta, brake = True, timeout = 2, emulate = True)
			armMotor.brake()
			
        else:
			lineFollow()
			
	return
    
	
binIdent()
            
