#!/bin/bash
FILES=`ls -1 -h serving_files`
WORK_DIR=`mktemp -d`
cd $WORK_DIR
for F in $FILES; do
	OUT=`timeout 120 wget $@/serving_files/$F  2>&1 |tail -n2`
	if [[ $OUT == *"saved"* ]];then
		SPEED=`echo $OUT | sed -e "s/.*(\(.*\)).*/\1/"`
		printf "\"$SPEED\"\t"
	else
		printf "\"0\"\t"
	fi
done

