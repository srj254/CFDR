#!/usr/bin/python

import os
import sys
import re

lists = []
#print "taccDict = {"

for filename in os.listdir('./'):
	with open(filename) as f:
		line = f.readline()
		lists.append(filename.split('.')[0])
#		print "'"+filename.split('.')[0]+"':", line.split(), ", "
#		print ""

#print "}"

print lists
