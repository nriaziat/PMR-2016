'''
This module provides students
1) a function that can pick up an existing
bluetooth connection without searching for it. Thus, the wait time for
the actual nxt-code to start is reduced.
2) a function that connects to a brick over USB without checking
firmware compatibiltiy (advanced users only)

Restrictions (for Bluetooth):
    1) the device is already paired.
    2) the code is developed to run on Linux (a Linux sys command is used)

Author: Michael Fruhnert, 19-Sep-2016
'''

import bluetooth
import usb
import subprocess as sp
from nxt.bluesock import BlueSock
from nxt.usbsock import USBSock, ID_VENDOR_LEGO, ID_PRODUCT_NXT

# provide the user-friendly name of the NXT to be connected
# device must already be paired / known to the system
def btConnect(nxtName):
    # use linux system tool to list bluetooth devices
    p = sp.Popen(["bt-device", "--list"], stdin=sp.PIPE,
            stdout=sp.PIPE, close_fds=True)
    (stdout, stdin) = (p.stdout, p.stdin)
    data = stdout.readlines()
    # first line either 'Added devices:' or 'No devices Found' - skip
    ind = 1
    mac = ''
    while ((ind < len(data)) and (mac == '')):
        line = str(data[ind]).split(" ") # to separate name and MAC
        if (" ".join(line[:-1]) == nxtName):
            mac = line[-1].strip()[1:-1] # MAC address, chop () off
        ind += 1

    if (mac == ''):
        print("Error: Device not found. Make sure it is already paired.")
        exit()
    else:
        return BlueSock(mac).connect()

# uses the first NXT brick connected over USB WITHOUT checking its firmware
# (can be used to "trick" nxt-python to run with RobotC firmware over USB)
def usbConnect():
    for bus in usb.busses():
        for device in bus.devices:
            if ((device.idVendor == ID_VENDOR_LEGO)
                        and (device.idProduct == ID_PRODUCT_NXT)):
                return USBSock(device).connect()

    print("Error: No device found on USB. Make sure the NXT is turned on.")
    exit()
