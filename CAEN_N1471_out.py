#! /usr/bin/sudo  /usr/bin/python3
import serial
import time
import re
import sys
import datetime
import os
#import pyvisa as visa
import argparse

import CAEN_N1471_commands as N1471

default_directory="/home/msgc/status"
default_filetag="_3"

MODULE="N1471"
#WRITEDIR_DEF="/home/msgc/status/CAEN/"

# Returns the value (0 or 1) of a given bit position in a given number
def get_bit(number, pos):
    return (int(number) & 2**pos) / 2**pos

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

def monitor():
#    statuses=[]
    polarities=[]
    currents=[]
    voltages=[]
    todaydetail  =    datetime.datetime.today()
    print  (todaydetail.strftime("%Y/%m/%d/%H:%M:%S "),end="")
    for ch in range(N1471.num_ch):
        #read polarity
        cmd=str.encode(N1471.cmd_get_polarity.replace("CHANNEL",str(ch)))
        polarity=str(N1471.query_value(cmd, N1471.replystr,dev)).replace("\r","")
        pol=1
        if(polarity=="-"):
            pol=-1
        #read voltage
        cmd=str.encode(N1471.cmd_get_voltage.replace("CHANNEL",str(ch)))
        voltage=str(N1471.query_value(cmd, N1471.replystr,dev)).replace("\r","")
        #read current
        cmd=str.encode(N1471.cmd_get_current.replace("CHANNEL",str(ch)))
        current=str(N1471.query_value(cmd, N1471.replystr,dev)).replace("\r","")
#        print(polarity+" "+str(pol)+" "+voltage+" "+current)
        print("%.1f %.3f "  % (pol*float(voltage),float(current)),end=" ")
    print("")    



print("### Output "+MODULE+" ###")

# parser 
parser = argparse.ArgumentParser(description='CAEN HV read')
parser.add_argument('arg1',help='ch (0-3)',type=int)
parser.add_argument('arg2',help='V',type=float)
#parser.add_argument('-d', '--directory', default=default_directory, help='output directory')
#parser.add_argument('-t', '--file_tag', default=default_filetag, help='file tag')
#parser.add_argument("-o",help="one shot flag",action='store_true')
#parser.add_argument("-i",help="interval (sec)",type=int,default=int_def)
args=parser.parse_args();
ch=args.arg1
V=args.arg2
print("  Output "+str(V)+"V on channle "+str(ch))

if ch<0 or  ch>3 :
    print("channel"+str(ch)+" is out of range. (must be in 0-3)")
    exit(1)

#dirname=args.directory
#filetag=args.file_tag

#if dirname[-1] != "/":
#    dirname=dirname+"/"

ports=port_search() #search for active ports
port=N1471.CAEN_search(ports)

print("  Search for "+MODULE,end=" ",flush=True)

giveup=100
i=0
#if type(port) == int :
while type(port) == int :
    print(".",end=" ",flush=True)
    ports=port_search() #search for active ports
    port=N1471.CAEN_search(ports)
    i=i+1
    if i > giveup:
        print("port not found")
        exit(1)
    time.sleep(1)
#    exit(1)

print("\n  USB port: "+str(port))
dev = serial.Serial(port, N1471.bar, timeout=1, xonxoff=True, bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE)

#today = datetime.date.today()
#todaydetail  =    datetime.datetime.today()

monitor()

#ch=0
#print("ch:"+str(ch)+" output:"+str(V)+"V")
cmd=str.encode(N1471.cmd_set_voltage.replace("CHANNEL",str(ch)).replace("VALUE",str(V)))
#print(cmd)
replystr=str(N1471.query_value(cmd, N1471.replystr,dev)).replace("\r","")
print(replystr)


monitor()

#print  (todaydetail.strftime("%Y/%m/%d/%H:%M:%S "),end="")

  #  print("",file=f)
  #  f.close()
  #  time.sleep(1)



