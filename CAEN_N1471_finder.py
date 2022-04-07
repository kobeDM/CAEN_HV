#!  /usr/bin/python3
import serial
import time
import re
import sys
import datetime
import os
import pyvisa as visa
import argparse

import CAEN_N1471_commands as N1471

MODULE="N1471"

def port_search():
    bar=N1471.bar
    ser=''#bar=9600
    serno=[] #成功したCOMポート番号を格納（Pythonで使う番号そのもの）
    for i in range(32):	
        port = '/dev/ttyUSB'+str(i)
        try:
            ser = serial.Serial(port, bar)
            serno.append(port)
            ser.close()		
        except:
            None
    return serno

print("### Search for "+MODULE+" ###")
ports=port_search() #search for active ports
#print(ports)
port=N1471.CAEN_search(ports)
print(str(MODULE)+" USB port="+str(port))
#dev = serial.Serial(port, N1471.bar, timeout=1, xonxoff=True, bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE)


