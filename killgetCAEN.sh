#! /bin/sh
pids=`ps -aux | grep CAEN | grep local | awk '{print $2}'`
echo $pids
sudo kill $pids
 