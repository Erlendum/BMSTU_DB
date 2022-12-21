#!/bin/bash

methods="Redis Db"
ops="Select Insert Update Delete"

if [ ! -z "$1" ]; then
	methods="$1"
fi
if [ ! -z "$2" ]; then
	ops="$2"
fi

mkdir -p data

echo "Measuring..."

cd src

for method in $methods; do
    for op in $ops; do
	    echo -n -e "$method $op\r"
	    go run . -mode=true -benchType=$op -benchShow=$method  >> "../data/data_$method$op.txt"
    done
done
