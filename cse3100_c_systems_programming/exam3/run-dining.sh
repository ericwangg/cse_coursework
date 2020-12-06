#!/usr/bin/bash

# you can add more test arguments
arguments=( 
	''			# 0 
	'-g0  -G9 -t2 -T4' 	# 1
	'-g8  -G0 -t4 -T0' 	# 2
	'-g10 -G0 -t2 -T4' 	# 3
	'-g6  -G5 -t3 -T3 -m10'	# 4
	)

if ! [[ "$1" =~  ^[0-9]+$ && $(( $1 >= 0 && $1 < ${#arguments[@]} )) == 1 ]] ; then
	echo "Specify a number in [0,  ${#arguments[@]})."
	exit 1
fi

arg=${arguments[$1]}

TARGET=dining
make $TARGET >/dev/null || exit 1

# can do multiple runs
num_runs=1

TMPFN="test-output.TXT"

echo "./$TARGET $arg "
for (( i = 0; i < num_runs; i++));  do
	./$TARGET $arg | python3 ./check-dining.py -V > $TMPFN || { head -1 $TMPFN; tail -50 $TMPFN; echo "error"; exit 1; }
done

tail -20 $TMPFN

echo "$TARGET has passed the test this time."
