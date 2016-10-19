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
from nxt.sensor import Light, Touch
from nxt.sensor import PORT_1, PORT_2, PORT_3, PORT_4
from nxt.motor import Motor, PORT_A, PORT_B, PORT_C


motorLeft = Motor(brick, PORT_B)
motorRight = Motor(brick, PORT_C)
armMotor = Motor(brick, PORT_A)
light = Light(brick, PORT_3)
touch = Touch(brick, PORT_4)
sonar = Ultrasonic(brick, PORT_2)

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
		if sonar.get_distance < 6: #change this distance value 
			armMotor.turn(90, 100, brake = True, timeout = 2, emulate = True) #change this power and tacho value
			motorLeft.run(power = 60)
			motorRight.run(power = 60)
			sleep(1)
			motorLeft.brake()
			motorRight.brake()
			armMotor.turn(-90, 100, brake = True, timeout = 2, emulate = True)
			armMotor.brake()
		else:
			lineFollow()
	return
      
binPickup()
            
