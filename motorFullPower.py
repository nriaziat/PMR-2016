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

#######################################################################
## Then, you can specify what you want the NXT to do
#######################################################################

from time import sleep

from nxt.motor import Motor, PORT_A, PORT_B, PORT_C
from nxt.sensor import Touch, PORT_4

motorLeft = Motor(brick, PORT_B)
motorRight = Motor(brick, PORT_C)
touch = Touch(brick, PORT_4)

while touch.is_pressed() == False:
    
    motorLeft.run(power = -80)
    
    motorRight.run(power = -80)
    
motorLeft.idle()
motorRight.idle()
