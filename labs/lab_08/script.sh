#!/bin/sh

cd lab_08
while(true) do
	python3 gen.py ./
	sudo mv *.json ../nifi/in_file
	sleep 10
done
