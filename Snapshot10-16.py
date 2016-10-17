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
from nxt.sensor import Light
from nxt.sensor.hitechnic import Gyro
from nxt.sensor import PORT_1, PORT_2
from nxt.motor import Motor, PORT_A, PORT_B, PORT_C


motorLeft = Motor(brick, PORT_A)
motorRight = Motor(brick, PORT_B)
light = Light(brick, PORT_2)

def manualCalibrate():
    black = light.get_lightness()
    print(black)
    sleep(2)
    white = light.get_lightness()
    print(white)
    threshold = (white + black) / 2 
    print(threshold)
    return threshold


    
def sensorValue():
    while True:
        light.set_illuminated(True)
        return light.get_lightness()
    
def lineFollow():
    light.set_illuminated(True)
    motorLeft.reset_position(False)
    motorRight.reset_position(False)
    black = light.get_lightness()
    print(black)
    motorRight.turn(60, 100, brake=True, timeout=1.5, emulate=True)
    sleep(0.25)
    white = light.get_lightness()
    motorRight.turn(-60, 100, brake = True, timeout=1.5, emulate=True)
    print(white)
    threshold = (black + white) / 2
    print("Threshold = ", threshold)
    gain = 3
    0
    pwr = 90
    while sensorValue() > 0:
        print(sensorValue())
        error = sensorValue() - threshold
        correction = (error * gain) / (white - black)
        if error < 0:
            motorRight.run(power = -(pwr + correction))
        elif error >= 0:
            motorLeft.run(power = -(pwr - correction))
    motorLeft.idle()
    motorRight.idle()
    
def counter():
    print("Start")
    with open('data.txt', 'w') as data:
        light.set_illuminated(True)
        val = light.get_lightness()
        data.write(str(val))

lineFollow()    

            
