#!/usr/bin/python

import os
import sys
import re

f = open (sys.argv[1], 'r');

fileContent = f.readlines();

len(fileContent);

fileName = 1;
prevLine = '';

for line in fileContent:
	if "X-Mozilla-Status:" in line:
		fmail = open(str(fileName), 'w');
		fmail.write(prevLine)
		fmail.write(line)
	else: 
		try:
			fmail.write(line)
		except NameError:
			print ("Name Doesn't exist")
	prevLine = line
	fileName = fileName + 1;

