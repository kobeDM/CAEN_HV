import serial
import time
import re
import sys
import datetime
import os

todaydetail  =    datetime.datetime.today()
#print(todaydetail)
port = '/dev/ttyUSB0'
#port = '/dev/ttyUSB1'
caenN1470 = serial.Serial(port, 9600, timeout=1, xonxoff=True, bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE)
print (caenN1470)
time.sleep(1)


# Sends a query and returns the value
def query_value(querystr, replystr):
    try:
        caenN1470.write(querystr)
        time.sleep(0.1)
#        reply = caenN1470.read(100)
        reply = caenN1470.read(100).decode('utf-8')
#        print("reply",replystr,reply)
        m = re.match(replystr, reply)
#        m = re.match(replystr, "aho")
#        m = re.match(re.compile(replystr), re.compile(reply))
#        m=re.match("aho","aho")
#        print(m)
        if (m):
            #print "error..."
            #return -1
            return m.group(2)
        else:
            print("error...")
            return -1
    except serial.serialutil.SerialException:
        return -1


# Returns the value (0 or 1) of a given bit position in a given number                                                                 
def get_bit(number, pos):
    return (int(number) & 2**pos) / 2**pos


replystr = re.compile('^#BD:(\d{2}),CMD:OK,VAL:(.*)')

cmdstr = str.encode('$BD:00,CMD:MON,PAR:BDNAME\r')
cmd_get_status_ch0 = str.encode('$BD:00,CMD:MON,CH:0,PAR:STAT\r')
cmd_get_polarity_ch0 = str.encode('$BD:00,CMD:MON,CH:0,PAR:POL\r')
cmd_get_voltage_ch0  = str.encode('$BD:00,CMD:MON,CH:0,PAR:VMON\r')
cmd_get_current_ch0  = str.encode('$BD:00,CMD:MON,CH:0,PAR:IMON\r')

cmd_get_status_ch1   = str.encode('$BD:00,CMD:MON,CH:1,PAR:STAT\r')
cmd_get_polarity_ch1 = str.encode('$BD:00,CMD:MON,CH:1,PAR:POL\r')
cmd_get_voltage_ch1  = str.encode('$BD:00,CMD:MON,CH:1,PAR:VMON\r')
cmd_get_current_ch1  = str.encode('$BD:00,CMD:MON,CH:1,PAR:IMON\r')

cmd_get_status_ch2   = str.encode('$BD:00,CMD:MON,CH:2,PAR:STAT\r')
cmd_get_polarity_ch2 = str.encode('$BD:00,CMD:MON,CH:2,PAR:POL\r')
cmd_get_voltage_ch2  = str.encode('$BD:00,CMD:MON,CH:2,PAR:VMON\r')
cmd_get_current_ch2  = str.encode('$BD:00,CMD:MON,CH:2,PAR:IMON\r')
    
cmd_get_status_ch3   = str.encode('$BD:00,CMD:MON,CH:3,PAR:STAT\r')
cmd_get_polarity_ch3 = str.encode('$BD:00,CMD:MON,CH:3,PAR:POL\r')
cmd_get_voltage_ch3  = str.encode('$BD:00,CMD:MON,CH:3,PAR:VMON\r')
cmd_get_current_ch3  = str.encode('$BD:00,CMD:MON,CH:3,PAR:IMON\r')

reply = query_value(cmdstr, replystr)
print ("sent: ", cmdstr)
print ("read: ", reply)
print ("")

#p = re.compile(r'([a-z]+)@([a-z]+)\.com')
#print(p)


today = datetime.date.today()
print (today)
#f = open('{0:%Y%m%d}'.format(today),'a')



while True:

    tmp_today = datetime.date.today()
    if today != tmp_today:
        print (tmp_today)
        today = tmp_today
    fna = '{0:%Y%m%d}'.format(today)
    fna += "_3"
    print(fna)
#    f = open('{0:%Y%m%d}'.format(today),'a')
    f = open(fna,'a')

    todaydetail  =    datetime.datetime.today()
    #print(todaydetail)

    reply_status_ch0 = query_value(cmd_get_status_ch0, replystr)
    #print("ch0",end="")
    ch0_on = get_bit(reply_status_ch0, 0)
    ch0_disabled = get_bit(reply_status_ch0, 10)
    #print(".",end="")
    reply_voltage_ch0 = query_value(cmd_get_voltage_ch0, replystr)
    reply_current_ch0 = query_value(cmd_get_current_ch0, replystr)
    reply_pol_ch0 = query_value(cmd_get_polarity_ch0, replystr)
   # print(".")
    #print("ch1",end="")
    reply_status_ch1 = query_value(cmd_get_status_ch1, replystr)
    ch1_on = get_bit(reply_status_ch1, 0)
    ch1_disabled = get_bit(reply_status_ch1, 10)

    reply_voltage_ch1 = query_value(cmd_get_voltage_ch1, replystr)
    reply_current_ch1 = query_value(cmd_get_current_ch1, replystr)
    reply_pol_ch1 = query_value(cmd_get_polarity_ch1, replystr)
 #   print(".")
  #  print("ch2",end="")


    reply_status_ch2 = query_value(cmd_get_status_ch2, replystr)
    ch2_on = get_bit(reply_status_ch2, 0)
    ch2_disabled = get_bit(reply_status_ch2, 10)

    reply_voltage_ch2 = query_value(cmd_get_voltage_ch2, replystr)
    reply_current_ch2 = query_value(cmd_get_current_ch2, replystr)
    reply_pol_ch2 = query_value(cmd_get_polarity_ch2, replystr)
 #   print(".")
#    print("ch3",end="")

    reply_status_ch3 = query_value(cmd_get_status_ch3, replystr)
    ch3_on = get_bit(reply_status_ch3, 0)
    ch3_disabled = get_bit(reply_status_ch3, 10)

    reply_voltage_ch3 = query_value(cmd_get_voltage_ch3, replystr)
    reply_current_ch3 = query_value(cmd_get_current_ch3, replystr)
    reply_pol_ch3 = query_value(cmd_get_polarity_ch3, replystr)
#    print(".")

    print  (todaydetail.strftime("%Y/%m/%d/%H:%M:%S "),end="")
    print ("%.0f %.3f %.0f %.3f %.0f %.3f %.0f %.3f" % (float(reply_voltage_ch0), float(reply_current_ch0),float(reply_voltage_ch1), float(reply_current_ch1),float(reply_voltage_ch2), float(reply_current_ch2),float(reply_voltage_ch3), float(reply_current_ch3)))
 
    print  (todaydetail.strftime("%Y/%m/%d/%H:%M:%S "),end="",
            file=f)
    print ("%.0f %.3f %.0f %.3f %.0f %.3f %.0f %.3f" % (float(reply_voltage_ch0), float(reply_current_ch0),float(reply_voltage_ch1), float(reply_current_ch1),float(reply_voltage_ch2), float(reply_current_ch2),float(reply_voltage_ch3), float(reply_current_ch3)),file=f)
    f.close()
#    time.sleep(1)
