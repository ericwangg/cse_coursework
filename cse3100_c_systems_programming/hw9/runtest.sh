#/usr/bin/env bash

# set -x

SERVER=server_tickets
CLIENT=kiosks
SRV_OPT='-t50'
TMPFN='test-server-output.txt'

opt_checkmax='1'

opt_wait=''
opt_think=''
opt_n='-n4'
nr='1'

for a ; do 
	if [[ $a =~ ^-t[[:digit:]] ]]; then 
		SRV_OPT="$a"
	elif [[ $a =~ ^-n[[:digit:]] ]]; then 
		opt_n="$a"
	elif [[ $a == "-W" ]]; then 
		opt_wait="$a"
	elif [[ $a == "-T" ]]; then 
		opt_think="$a"
	elif [[ $a == "-M" ]]; then 	# do not check max connection
		opt_checkmax=''
	elif [[ $a =~ ^[[:digit:]]+$ ]]; then 
		nr="$a"
	else 
	       echo "Unknown option: $a" 	
	       echo "Valid options are: -n<N> -t<N> <N> -W -T -M"
	       exit 1
	fi
done

CLI_OPT="$opt_n $opt_wait $opt_think"
echo "number-of-runs:${nr} SRV_OPT=${SRV_OPT} CLI_OPT:${CLI_OPT}"

make

# kill any running server
SRV_PID=$(ps -C $SERVER -o pid=)
if [ -n "$SRV_PID" ] ; then 
	echo "Killing $SRV_PID ..."
	kill $SRV_PID 
fi

# do nr rounds
for ((i=0; i<nr; i++)) do
	echo run $i
	stdbuf -oL ./$SERVER $SRV_OPT > $TMPFN &
	# wait for server to start
	sleep 1

	failed=0
	./$CLIENT $CLI_OPT | python3 ./check-kiosks.py $SRV_OPT || failed=1
	kill $(ps -C $SERVER -o pid=)
	if [ "$failed" = "1" ] ; then 
		echo "Error: The program did not pass the test."
		exit 1
	fi

	if [ -n "$opt_checkmax" ]; then 
		max_connected=$(grep -o 'max=[[:digit:]]\+' "$TMPFN" | tail -1)
		(( "${max_connected#max=}" >= "${opt_n#-n}" )) || { echo "Error: max_connected is ${max_connected}"; exit 1; }
	fi
done

# rm -f "$TMPFN"

echo "The program passed the tests this time."
