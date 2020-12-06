#!/usr/bin/bash

TMPFNS='pipe-sort-s.out'
TMPFNU='pipe-sort-u.out'
PROGRAM=pipe-sort

OPTION='-u'
paramters=( "20"  "100" "1000" "2000" "100000" ) 

set -e
make $PROGRAM
trap "echo 'Error: output from last run does not look correct';" ERR

for p in "${paramters[@]}"; do
	echo "./$PROGRAM $p"
	./$PROGRAM $p $OPTION > "$TMPFNU" 
	./$PROGRAM $p > "$TMPFNS" 
	# if [[ "$p" = "100" ]]; then  echo "something" >> "$TMPFNU"; fi  
	diff "$TMPFNS" <(sort -n "$TMPFNU")
done

echo "Your program seems to have passed all the tests in this script."
rm -rf "$TMPFNU" "$TMPFNS"
