#!/bin/bash
#cd serving_files
#python -m SimpleHTTPServer 80 > /tmp/http.log &
rm -rf /var/www/html/serving_files
cp -r ./serving_files  /var/www/html/
nginx &
sleep 2
#python -m SimpleHTTPServer 80 >/dev/null &
PID=$!
echo $PID
#echo `ps -el |grep $PID`
