#!/bin/bash

filename=$PWD/$1
dir=`dirname $0`
while read line; do
    echo "DOING >> python3 ./playwright-python-screenshot-3-browsers-5-breakpoints.py $line"
    python3 $dir/playwright-python-screenshot-3-browsers-5-breakpoints.py $line
done < $filename
