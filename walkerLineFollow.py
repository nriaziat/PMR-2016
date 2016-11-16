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

from nxt.motor import Motor, PORT_A, PORT_B, PORT_C
from nxt.sensor import Touch, PORT_4, PORT_3, PORT_2, Light, PORT_1

light = Light(brick, PORT_1)
turningMotor = Motor(brick, PORT_B)
walkingMotor = Motor(brick, PORT_C)
legPosition = Touch(brick, PORT_3)
#ultrasonic = Sonar(brick, PORT_2)

def calibrate():
    # turn on light sensor
    light.set_illuminated(True)
    
    sleep(0.25)
    
    # calibrates black value
    black = light.get_lightness()
    print("Black = %d" % black)
    
    # turns right ~30 degrees
    turningMotor.turn(70, 80, brake=True, timeout=3, emulate=True)
    
    sleep(0.25)
    
    # calibrates white value
    white = light.get_lightness()
    
    #turns back to start position
    turningMotor.turn(-70, 80, brake = True, timeout=3, emulate=True)
    print("White = %d" % white)
    return (black,white)
    
def lineFollow():
    
	# takes calibration values from calibrate function
    calibrateVal = calibrate()
	
	#seperates white and black light values from funciton output
    black = calibrateVal[0]
    white = calibrateVal[1]
	
	# sets the threshold to the average of white and black
    threshold = (black + white) / 2
    
	# checks if black and white values are too close
    while abs(black - white) <= 50:
		# recalibrates PMR when user pressed touch sensor
        print("Calibration Failed. Black and white are not distinct. Reset PMR and press the touch sensor to re-calibrate.")
        
    print("Threshold = ", threshold)
    
	# sets error sensitivity
    gain = 150
	
	# sets general drive power
    #pwr = 75
    
	#checks to make sure light sensor is plugged in, kill switch isnt pressed
    while (light.get_lightness() > 0):
        
        walkingMotor.run(power = 120)
		# polls light sensor value
        currLightness = light.get_lightness() 
        #print(light.get_lightness())
        
		# recalibrates black if darker black found
        if currLightness < black and currLightness != 0: # THIS MIGHT BE DUMB, CHECK LATER
            black = currLightness
            
		# recalibrates white if lighter white found
        if currLightness > white:
            white = currLightness
            
			
        error = currLightness - threshold
		
		#normalize correction value to sensor range
        correction = (error * gain) / (white - black)
        
        # determine direction to turn
        d = 1
        if correction < 0: 
            d = -1
            correction *= -1
        
		# run motors based on how far off the line PMR is
        turningMotor.turn(d * 70, correction, brake = True)
     
	# idle motors if sensor unplugged or killswitch pressed
    turningMotor.idle()
    walkingMotor.idle()
      
lineFollow()
            
