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
from nxt.sensor import Touch, PORT_4, PORT_3

turningMotor = Motor(brick, PORT_B)
walkingMotor = Motor(brick, PORT_C)
turnerSwitch = Touch(brick, PORT_4)
legPosition = Touch(brick, PORT_3)

while True:
    if turnerSwitch.is_pressed() == False:
        turningMotor.run(power = 0)
        a = 0
        walkingMotor.run(power = 120)
    
    else:
        if legPosition.is_pressed() == False:
            walkingMotor.run(power = 100)
        else:
            a = 1
        if a == 1:
            walkingMotor.run(power = 0)
            walkingMotor.brake()
            turningMotor.run(power = 120)
        
        
