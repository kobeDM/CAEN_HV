#! /bin/sh

#EXE_3="nohup sudo /usr/local/bin/python3 /home/msgc/bin/getCAEN1471_v3.py"
EXE_3="nohup sudo /usr/local/bin/python3 /home/msgc/src/getCAEN_N1471_p3/getCAEN_N1471_p3.py"
echo $EXE_3
${EXE_3} &
#gnome-terminal --title "PCI-3133 board 1" -x ${EXE_1} 
#gnome-terminal  --title "PCI-3133 board 2" -x ${EXE_2}
