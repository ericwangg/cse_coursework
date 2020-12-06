#!/usr/bin/bash -e

if [ $# != 1 ]; then 
	echo "Usage: $0 'pattern'"
	echo "Place the pattern in ''. The following are some examples."
	echo "'a*t'"
	echo "'a*'"
	echo "'*x'"
	exit 1
fi

IFS='*' read -r prefix suffix <<<"$1"

# echo "prefix is $prefix"
# echo "suffix is $suffix"

while read line; do
	case $line in "$prefix"*"$suffix")
		echo "$line"
    	esac
done < "filenames.txt"

