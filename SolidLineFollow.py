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
light = Light(brick, PORT_3)
touch = Touch(brick, PORT_4)

def sensorValue():
    # get light sensor value
    return 

def calibrate():
    # turn on light sensor
    light.set_illuminated(True)
    
    # zeroes motor position
    motorLeft.reset_position(False)
    motorRight.reset_position(False)
    
    # calibrates black value
    black = light.get_lightness()
    print("Black = %d" % black)
    
    # turns right ~30 degrees
    motorRight.turn(80, 360, brake=True, timeout=3, emulate=True)
    #motorLeft.turn(-80, 360, brake=True, timeout=3, emulate=True)
    sleep(0.25)
    
    # calibrates white value
    white = light.get_lightness()
    
    #turns back to start position
    motorRight.turn(-80, 360, brake = True, timeout=3, emulate=True)
    print("White = %d" % white)
    return (black,white)
    
def lineFollow():
    
    calibrateVal = calibrate()
    black = calibrateVal[0]
    white = calibrateVal[1]
    threshold = (black + white) / 2
    
    while abs(black - white) <= 50:
        print("Calibration Failed. Black and white are not distinct")
        if touch.is_pressed == True:
			calibrateVal = calibrate()
			black = calibrateVal[0]
			white = calibrateVal[1]
			threshold = (black + white) / 2
        
    print("Threshold = ", threshold)
    
    gain = 45
    pwr = 75
    
    while (light.get_lightness() > 0) and not (touch.is_pressed()):
        
        lightness = light.get_lightness() 
        print(light.get_lightness())
        
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
      
lineFollow()
            
