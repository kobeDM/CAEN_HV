import serial
import re

MODULE="N1471"
#bar=9600
bar=115200
num_ch=4

cmdstr = str.encode('$BD:00,CMD:MON,PAR:BDNAME\r')
replystr = re.compile('^#BD:(\d{2}),CMD:OK,VAL:(.*)')

cmd_get_voltage  = '$BD:00,CMD:MON,CH:CHANNEL,PAR:VMON\r'
cmd_get_status = '$BD:00,CMD:MON,CH:CHANNEL,PAR:STAT\r'
cmd_get_polarity = '$BD:00,CMD:MON,CH:CHANNEL,PAR:POL\r'
cmd_get_current  = '$BD:00,CMD:MON,CH:CHANNEL,PAR:IMON\r'

cmd_set_voltage  = '$BD:00,CMD:SET,CH:CHANNEL,PAR:VSET,VAL:VALUE\r'

cmd_set_on  = '$BD:00,CMD:SET,CH:CHANNEL,PAR:ON\r'
cmd_set_off  = '$BD:00,CMD:SET,CH:CHANNEL,PAR:OFF\r'

#cmd_get_status_ch0 = str.encode('$BD:00,CMD:MON,CH:0,PAR:STAT\r')
#cmd_get_polarity_ch0 = str.encode('$BD:00,CMD:MON,CH:0,PAR:POL\r')
#cmd_get_voltage_ch0  = str.encode('$BD:00,CMD:MON,CH:0,PAR:VMON\r')
#cmd_get_current_ch0  = str.encode('$BD:00,CMD:MON,CH:0,PAR:IMON\r')



#cmd_get_status_ch1   = str.encode('$BD:00,CMD:MON,CH:1,PAR:STAT\r')
#cmd_get_polarity_ch1 = str.encode('$BD:00,CMD:MON,CH:1,PAR:POL\r')
#cmd_get_voltage_ch1  = str.encode('$BD:00,CMD:MON,CH:1,PAR:VMON\r')
#cmd_get_current_ch1  = str.encode('$BD:00,CMD:MON,CH:1,PAR:IMON\r')

#cmd_get_status_ch2   = str.encode('$BD:00,CMD:MON,CH:2,PAR:STAT\r')
#cmd_get_polarity_ch2 = str.encode('$BD:00,CMD:MON,CH:2,PAR:POL\r')
#cmd_get_voltage_ch2  = str.encode('$BD:00,CMD:MON,CH:2,PAR:VMON\r')
#cmd_get_current_ch2  = str.encode('$BD:00,CMD:MON,CH:2,PAR:IMON\r')
    
#cmd_get_status_ch3   = str.encode('$BD:00,CMD:MON,CH:3,PAR:STAT\r')
#cmd_get_polarity_ch3 = str.encode('$BD:00,CMD:MON,CH:3,PAR:POL\r')
#cmd_get_voltage_ch3  = str.encode('$BD:00,CMD:MON,CH:3,PAR:VMON\r')
#cmd_get_current_ch3  = str.encode('$BD:00,CMD:MON,CH:3,PAR:IMON\r')

# Sends a query and returns the value
def query_value(querystr, replystr,dev):
    try:
        dev.write(querystr)
        #        time.sleep(0.1)
        reply_undecoded = dev.read(100)
        #        print("reply:"+repr(reply_undecoded[0:3]))
        if len(reply_undecoded) ==0:
#            print("no response")
            return -1
        if reply_undecoded[0:1] == b'\x9c':
 #           print("something else")#not utf-8 decodable
            return -1
        reply = reply_undecoded.decode('utf-8')
        m = re.match(replystr, reply)
        if (m):
            return m.group(2)
        else:
            return -1
    except serial.serialutil.SerialException:
        return -1

#search for a CAEN module
def CAEN_search(ports):
    for i in range(len(ports)):
#        print(str(i)+" "+ports[i],end="\t\t\t")
        dev = serial.Serial(ports[i], bar, timeout=1, xonxoff=True, bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE)
        reply = query_value(cmdstr, replystr,dev)
        if str(reply)[0:len(MODULE)] == MODULE :
  #          print(MODULE+" found")
            return ports[i]
    return -1


