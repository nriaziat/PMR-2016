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


motor = Motor(brick, PORT_C)
light = Light(brick, PORT_2)

motor.reset_position(False)
print(motor.get_tacho())
black = light.get_lightness()
print("black = ", black)
motor.turn(30, 50, brake=True, timeout=1.5, emulate=True)
sleep(0.05)
print(motor.get_tacho())
motor.brake()
white = light.get_lightness()
print("white = ", white)
motor.turn(-30, 50, brake=True, timeout=1.5, emulate=True)
threshold = (black + white) / 2
print(motor.get_tacho())
print("Threshold = ", threshold)

while light.get_lightness() < 1020:
    light.get_lightness()
    if light.get_lightness() > threshold:
        light.get_lightness()
        motor.run(power = 10)
        light.get_lightness()
        
    if light.get_lightness() < threshold:
        light.get_lightness()
        motor.run(power = -10)
        light.get_lightness()
        
    print("light = ", light.get_lightness())
    angle = motor.get_tacho()
    print(angle)
motor.idle()
    
'''
lightSensor = Light(brick, PORT_1)
gyro = Gyro(brick, PORT_2)

sum = 0
gyro.calibrate()
updatePeriod = .01

while True:
    dps = gyro.get_rotation_speed()
    # integrate
    sum += dps * updatePeriod
    sleep(updatePeriod)
    print(sum)

#turn sensor left
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
                #go straight'''

            
