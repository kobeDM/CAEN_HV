#!  /usr/bin/python3
import subprocess
import os

exe="CAEN_N1471_mon.py"
selfpid=os.getpid()
cmd="ps -aux | grep "+exe+"  | grep python3 | grep -v 'ps -aux' |awk '{print $2}'"
#print(cmd)
pid=subprocess.run(cmd,shell=True,encoding='utf-8',stdout=subprocess.PIPE).stdout
cmd="kill "+pid
subprocess.run(cmd,shell=True)
#print(pid)
#print(selfpid)
