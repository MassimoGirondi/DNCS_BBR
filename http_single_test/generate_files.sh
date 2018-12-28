rm -rf serving_files
mkdir serving_files
#LIST=""
cd serving_files
for SIZE in 500K 1M 2M 5M 10M 100M; do
	dd if=/dev/urandom of=$SIZE bs=$SIZE count=1
	#LIST=$LIST"\n"$SIZE
done
ls -1 -h > ../field_list
#echo $LIST > serving_files/index.html
