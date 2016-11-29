import nxt
import nxtConnect # has to be in search path
import time

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
from nxt.sensor import Touch, PORT_4, PORT_3, PORT_2, Light, PORT_1, Ultrasonic

#from basicFunctions import step, calibrate

#light = Light(brick, PORT_1)
#turningMotor = Motor(brick, PORT_B)
walkingMotor = Motor(brick, PORT_C)
armMotor = Motor(brick, PORT_A)

walkingMotor.brake()
armMotor.brake()

def test(normalization, fileName):
    with open(fileName, 'w') as outputFile:
        outputFile.write('Initial value: %f' % normalization)
        for i in range(1000):
            diff = normalization - brick.get_battery_level()
            outputFile.write('%f\n' % diff)
            sleep(0.05)

def main():
    repeat = ''
    while repeat == '':
        normalization = 0
        for i in range(100):
            normalization += brick.get_battery_level()
            sleep(0.05)
        normalization /= 100
        brick.play_tone_and_wait(500, 250)
        binType = raw_input('Input bin type: ')
        fileName = 'binID_rawData_' + binType + '.txt'
        test(normalization, fileName)
        brick.play_tone_and_wait(1000, 250)
        repeat = raw_input('Press enter to repeat')

main()
