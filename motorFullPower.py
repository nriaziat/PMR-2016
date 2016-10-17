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

motorA = Motor(brick, PORT_A)
motorB = Motor(brick, PORT_B)

motorA.run(power = 125)
motorB.run(power = 125)
