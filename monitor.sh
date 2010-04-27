#!/bin/bash
# Author: Mark Sullivan

if [ $# -ne 1 ]
then
    rtime=10
else
    rtime=$1
fi

j=0
while true
do
    clear
    echo "===	Iteration $j	==="
    for i in `ls ./wget-log*`
    do
        file=`head -1 $i | sed s/--.*--//`
        echo -ne `basename $file`
        echo -ne "  "
        grep % $i | tail -1 | sed 's/\.\.//g' | sed 's/    / /'
    done
    let j++
    sleep $rtime
done
