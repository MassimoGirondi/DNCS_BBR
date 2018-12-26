#!/bin/bash
WORK_DIR=`mktemp -d`
cd $WORK_DIR
OUT=`timeout 120 wget -e robots=off -r $@ -nv 2>&1 |tail -n2`

if [[ $OUT == *"Total"* ]];then
	SPEED=`echo $OUT |sed -e "s/.*(//" -e "s/)//"`
	TIME=`echo $OUT |sed -e "s/Total wall clock time: //" |sed -e "s/ Downloaded.*//" | tr -d '\n'`
	echo -e "\"$SPEED\"\t\"$TIME\""
else
	echo -e "0\t0"
fi


