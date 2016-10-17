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

from nxt.sensor import Light, Gyro
from nxt.sensor import PORT_1, PORT_2

lightSensor = Light(brick, PORT_1)
gyro = Gyro(brick, PORT_2)

gyro.calibrate()
while True:
    print(gyro.get_rotation_speed())

"""#turn sensor left
white = lightSensor.get_lightness()
#turn to initial position 
black = lightSensor.get_lightness
threshold = (white + black) / 2
 
while True:
    if lightSensor.get_lightness() > threshold:
        while motor has turned less than 91 degrees
            #turn sensor right until < thresold
            #note sensor final turn angle
        if lightSensor.get_lightness() <= threshold:
            #turn until gyro angle is same as sensor turn angle
        else:
            while motor has turned greater than -91 degrees
                #turn sensor left until change
            if lightSensor.get_lightness() <= threshold:
                #turn until gyro angle is same as sensor turn angle
            else:
                #go straight"""
            
