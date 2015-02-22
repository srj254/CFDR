#!/usr/bin/python

import sys
import os

if len(sys.argv) < 3:
	print "Usage ./Scriptname.py <path to OutlierFile> <path to files that are actually empty (Can use a shell command to find this)>"
	exit()

f1 = open(sys.argv[2], 'r')

with open(sys.argv[1], "r") as f:
	for line in f:
		print "inside"
		if any(path in line for path in f1):
			print f
		print "outside"
f1.close()
