#!/usr/bin/bash

# you can add more test arguments
arguments=('0.5 300000 2' '0.3 300000 3' '0.25 300000 4')

TARGET=rand-pair
make $TARGET >/dev/null || exit 1

for arg in "${arguments[@]}"; do
	echo "./$TARGET $arg"
	./$TARGET $arg 
done
