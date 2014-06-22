#!/bin/bash

ping6 -w 3 www.google.com
while [[ $? -ne 0 ]];do
	sleep 1;
	ping6 -w 3 www.google.com;
done;

