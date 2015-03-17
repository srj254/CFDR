#!/usr/bin/python

import os
import sys
import re
import string

def getNodeName(fName):
	p = re.findall(r"[\w]+", fName)
	raw_input()
	return (p[1])[1:] 

if __name__== "__main__":
	print "Usage <crtTaccStatsTable.py> <>"
	#exit()

for root, subDirs, fNames in os.walk(sys.argv[1]):
	for subDir in subDirs:
		print getNodeName(subDir)	
	for fName in fNames:
		pass	
