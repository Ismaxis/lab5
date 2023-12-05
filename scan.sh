#!/bin/bash

SLEEP_FOR=10
OUTPUT_PATH="mem.stat"

PID=$(cat ".pid")
echo $PID > $OUTPUT_PATH

while true; do
	top -b -n 1 -o %MEM | head -12 >> $OUTPUT_PATH	
	sleep $SLEEP_FOR
done
