# CAEN_HV

```
# requires pymysql　serial pyvisa
$ sudo python3 -m pip install pymysql　pyserial pyvisa
```
then read CAEN N1471
```
$ CAEN_N1471_read.py [-d outoput directory] [ -t file tag]
# ex) sudo CAEN_N1471_read.py -d /home/msgc/status/CAEN/ -t _1 
```

## CAEN N1471 monitor with influxDB + Grafana
```
$ CAEN_N1471_mon.py [-d outoput directory] [ -t file tag]
# ex) sudo python3 CAEN_N1471_mon.py
# *** EDIT influxDB configuration before running his python script!!! *** 
```

