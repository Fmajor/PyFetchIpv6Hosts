#!/bin/bash

ping6 -w 3 www.google.com
while [[ $? -ne 0 ]];do
	sleep 3;
	ping6 -w 3 www.google.com;
done;

python2.7 fetchHostsManyTreads.py youtube_and_facebook_url.txt 20
python2.7 fetchHostsManyTreads.py youtube_and_facebook_url.txt 20
