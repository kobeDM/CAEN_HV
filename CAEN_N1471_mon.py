#! /usr/bin/sudo  /usr/bin/python3
import serial
import time
import re
import sys
import datetime
import os
import pyvisa as visa
import argparse

import CAEN_N1471_commands as N1471

default_directory="/home/msgc/status/CAEN"
default_filetag="_3"

config_output = 'both'
MODULE="N1471"
sql_dbname=MODULE

ocsv, odb = True, True
if config_output == 'db':
    ocsv, odb = False, True
if config_output == 'both':
    ocsv, odb = True, True

# Returns the value (0 or 1) of a given bit position in a given number
def get_bit(number, pos):
    return (int(number) & 2**pos) / 2**pos

def port_search():
    bar=N1471.bar
    ser=''#bar=9600
    serno=[] # get COM port that succeeded in connection to N1471
    for i in range(32):	
        port = '/dev/ttyUSB'+str(i)
        try:
            ser = serial.Serial(port, bar)
            serno.append(port)
            ser.close()		
        except:
            None
    return serno

print("### Read "+MODULE+" ###")

# parser 
parser = argparse.ArgumentParser(description='CAEN HV read')
parser.add_argument('-d', '--directory', default=default_directory, help='output directory')
parser.add_argument('-t', '--file_tag', default=default_filetag, help='file tag')
args=parser.parse_args();
dirname=args.directory
filetag=args.file_tag

if dirname[-1] != "/":
    dirname=dirname+"/"

#database check              
if odb:
    from influxdb import InfluxDBClient
    client = InfluxDBClient( host = "10.37.0.227",
                             port = "8086",
                             username = "root",
                             password = "root",
                             database = "det_01c" )

print("### Search for "+MODULE+" ###")
ports=port_search() #search for active ports
print(ports)
#port=-1
port=N1471.CAEN_search(ports)
while type(port) == int:
    print(".",end="")
    port=N1471.CAEN_search(ports)

print(str(MODULE)+" USB port="+str(port))
dev = serial.Serial(port, N1471.bar, timeout=1, xonxoff=True, bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE)

today = datetime.date.today()
#print (today)
todaydetail  =    datetime.datetime.today()

while True:
    tmp_today = datetime.date.today()
    if today != tmp_today:
        print (tmp_today)
        today = tmp_today
    fout = dirname
    fout += '{0:%Y%m%d}'.format(today)
    fout += filetag
    f = open(fout,'a')
    todaydetail  =    datetime.datetime.today()
    statuses=[]
    polarities=[]
    currents=[]
    voltages=[]
    for ch in range(N1471.num_ch):
        cmd=str.encode(N1471.cmd_get_polarity.replace("CHANNEL",str(ch)))
        ret=N1471.query_value(cmd, N1471.replystr,dev)
        if type(ret) != int:
            polarities.append(ret.replace("\r",""))
        cmd=str.encode(N1471.cmd_get_voltage.replace("CHANNEL",str(ch)))
        ret=N1471.query_value(cmd, N1471.replystr,dev)
        if type(ret) != int:
            voltages.append(ret.replace("\r",""))
        cmd=str.encode(N1471.cmd_get_current.replace("CHANNEL",str(ch)))
        ret=N1471.query_value(cmd, N1471.replystr,dev)
        if type(ret) != int:
            currents.append(ret.replace("\r",""))
     
    print  (todaydetail.strftime("%Y/%m/%d/%H:%M:%S "),end="")
    print  (todaydetail.strftime("%Y/%m/%d/%H:%M:%S "),end="",file=f)
    if len(voltages)==N1471.num_ch and len(currents)==N1471.num_ch:
        if ocsv:   
            for ch in range(N1471.num_ch):
                print("%.1f %.3f "  % (float((polarities[ch]+voltages[ch])),float(currents[ch])),end="")            
                print("%.1f %.3f "  % (float((polarities[ch]+voltages[ch])),float(currents[ch])),end="",file=f)
            print("")
            print("",file=f)
        f.close()    
        if odb:
            date_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            utctime = datetime.datetime.utcnow()
            json_data = [
                {
                    'measurement' : "HV",
                    'fields' : {
                        'ch0_V' : float((polarities[0]+voltages[0])),
                        'ch0_I' : float(currents[0]),
                        'ch1_V' : float((polarities[1]+voltages[1])),
                        'ch1_I' : float(currents[1]),
                        'ch2_V' : float((polarities[2]+voltages[2])),
                        'ch2_I' : float(currents[2]),
                        'ch3_V' : float((polarities[3]+voltages[3])),
                        'ch3_I' : float(currents[3])
                    },
                    'time' : utctime,
                    'tags' : {
                        'host' : "CAEN_N1471A",
                        'device' : "CAEN_N1471A"
                    }
                }
            ]

            result = client.write_points( json_data )




