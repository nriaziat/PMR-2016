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

    n = 0
	# incrememnts the motor power up
	#	until the arm raises or kill-switch is pressed
    while n < 100 and not touch.is_pressed():
	
        armMotor.run(power = n)
		sleep(0.25)
		
		# checks if arm has raised
        if sonar.get_distance() > 8:
			
			#different end motor powers correspond to different bins
            if n < 20:
				
				return(1)
                print("Bin 1 Picked Up")
				
            elif n < 60:
				
				return(2)
                print("Bin 2 Picked Up")
  
				
            else:
			
				return(3)
                print("Bin 3 Picked Up")

			
			while sonar.get_distance() < 7:
				armMotor.run(power = n)
			armMotor.brake()
			return
				
		# if the arm is not up, increment n up
        else:
            n += 3
	
		
    armMotor.idle()

	
def calibrate():
    
    light.set_illuminated(True)
	
    motorLeft.reset_position(False)
    motorRight.reset_position(False)
	
    black = light.get_lightness() 
    print("Black = %d" % black)
	
    motorRight.turn(60, 100, brake=True, timeout=1.5, emulate=True)
	
    sleep(0.25)
	
    white = light.get_lightness() 
	
    motorRight.turn(-60, 100, brake = True, timeout=1.5, emulate=True)
	
    print("White = %d" % white)
    return (black,white)
    
	
def lineFollow():
	
	# tune these values for broken and dotted lines
    gain = 75
    pwr = 55
	
    while (light.get_lightness() > 0) and not (touch.is_pressed()):

        lightness = light.get_lightness() 
        print(light.get_lightness() )
        
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
	    
    """calibrateVal = calibrate()
    black = calibrateVal[0]
    white = calibrateVal[1]
    threshold = (black + white) / 2
    
    if abs(black - white) <= 50:
        print("Calibration Failed. Black and white are not distinct")
        return
        
    print("Threshold = ", threshold)"""
	
    while touch.is_pressed() == False:
        if sonar.get_distance < 15: 
			
			while sonar.get_distance > 10:
				
				armMotor.run(power = 20)
				
			armMotor.idle()
			
			#motorLeft.run(power = 60)
			#motorRight.run(power = 60)
			
			#sleep(0.25)
			
			#motorLeft.brake()
			#motorRight.brake()
			
			binNum = binIdent()
			
        #else:
			#lineFollow()
			
	return
    
	
binPickup()
            
