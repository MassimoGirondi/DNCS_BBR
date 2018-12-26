#!/bin/bash
cd page
pwd
#python -m SimpleHTTPServer 80 > /tmp/http.log &
nginx &
PID=$!
echo $PID
#echo `ps -el |grep $PID`
