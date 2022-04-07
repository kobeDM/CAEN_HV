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

default_directory="/home/msgc/status"
default_filetag="_3"

config_output = 'both'
MODULE="N1471"
#WRITEDIR_DEF="/home/msgc/status/CAEN/"
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

print("### Read "+MODULE+" ###")

# parser 
parser = argparse.ArgumentParser(description='CAEN HV read')
parser.add_argument('-d', '--directory', default=default_directory, help='output directory')
parser.add_argument('-t', '--file_tag', default=default_filetag, help='file tag')
#parser.add_argument("-o",help="one shot flag",action='store_true')
#parser.add_argument("-i",help="interval (sec)",type=int,default=int_def)
args=parser.parse_args();
dirname=args.directory
filetag=args.file_tag

if dirname[-1] != "/":
    dirname=dirname+"/"

#database check              
if odb:
    print("output to database "+sql_dbname)
    import pymysql.cursors
    conn = pymysql.connect(host='10.37.0.214',port=3306,user='rubis',passwd='password',autocommit='true')
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS " + sql_dbname)
    cursor.execute("USE " + sql_dbname)
    cursor.execute("CREATE TABLE IF NOT EXISTS  CAEN_N1471_1(time TIMESTAMP not null default CURRENT_TIMESTAMP,ch0_V FLOAT,ch0_I FLOAT,ch1_V FLOAT,ch1_I FLOAT,ch2_V FLOAT,ch2_I FLOAT,ch3_V FLOAT,ch3_I FLOAT)")


    
    
print("### Search for "+MODULE+" ###")
ports=port_search() #search for active ports
print(ports)
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
 #   print("output file: "+fout)
    f = open(fout,'a')
    todaydetail  =    datetime.datetime.today()
    #    print("")
    statuses=[]
    polarities=[]
    currents=[]
    voltages=[]
    for ch in range(N1471.num_ch):
        #read status
        cmd=str.encode(N1471.cmd_get_status.replace("CHANNEL",str(ch)))
        statuses.append(N1471.query_value(cmd, N1471.replystr,dev).replace("\r",""))
        #read polarity
        cmd=str.encode(N1471.cmd_get_polarity.replace("CHANNEL",str(ch)))
        polarities.append(N1471.query_value(cmd, N1471.replystr,dev).replace("\r",""))
        #read voltage
        cmd=str.encode(N1471.cmd_get_voltage.replace("CHANNEL",str(ch)))
        voltages.append(N1471.query_value(cmd, N1471.replystr,dev).replace("\r",""))
        #read current
        cmd=str.encode(N1471.cmd_get_current.replace("CHANNEL",str(ch)))
        currents.append(N1471.query_value(cmd, N1471.replystr,dev).replace("\r",""))

     
    print  (todaydetail.strftime("%Y/%m/%d/%H:%M:%S "),end="")
    print  (todaydetail.strftime("%Y/%m/%d/%H:%M:%S "),end="",file=f)
    for ch in range(N1471.num_ch):
        print("%.1f %.3f "  % (float((polarities[ch]+voltages[ch])),float(currents[ch])),end="")            
        if ocsv:   
            print("%.1f %.3f "  % (float((polarities[ch]+voltages[ch])),float(currents[ch])),end="",file=f)

    print(" > "+fout)
                
    if ocsv:   
        print("",file=f)
        f.close()
    
    if odb:
        date_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("insert into CAEN_N1471_1(ch0_V,ch0_I,ch1_V,ch1_I,ch2_V,ch2_I,ch3_V,ch3_I) values(%s, %s, %s, %s, %s, %s, %s, %s)",(str(float((polarities[0]+voltages[0]))),currents[0],str(float((polarities[1]+voltages[1]))),currents[1],str(float((polarities[2]+voltages[2]))),currents[2],str(float((polarities[3]+voltages[3]))),currents[3]))


    
    time.sleep(1)



