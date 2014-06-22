#!/bin/bash

ping6 -w 3 www.google.com
while [[ $? -ne 0 ]];do
	sleep 5;
	ping6 -w 3 www.google.com;
done;
python2.7 fetchHostsManyTreads.py google_url.txt

