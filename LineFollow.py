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

def calibrate ():
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
    print(light.get_lightness())

calibrate()
