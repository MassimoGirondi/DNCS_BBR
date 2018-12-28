#!/bin/bash

#cd page
rm -rf /var/ww/html/web_page
cp -r page /var/html/web_page
pwd
#python -m SimpleHTTPServer 80 > /tmp/http.log &
nginx &
PID=$!
echo $PID
#echo `ps -el |grep $PID`
