#!/usr/bin/python

import os
import sys
import re

jobIDs = []

if len(sys.argv) < 4:
	print "Usage <Path to Liblist> <Keyword> <New path for results>"
	exit()

jobIDFiles = {}

# Logic is to create dictionary of jobIDs where the values is a list of all liblist files corresponding to the jobID. 
for root, subdirs, filenames in os.walk(sys.argv[1]):
	for filename in filenames:
		if sys.argv[2] in filename:
			jobID = filename.split('_')[1].split('.')[0]
			try: 
				jobIDFiles[jobID].append(os.path.join(root, filename))
			except KeyError:
				jobIDFiles[jobID] = [os.path.join(root, filename)]

for key in jobIDFiles.keys():
	#print key + ' ' + ','.join(fPath for fPath in jobIDFiles.get(key))
	#print key + ' ' + str(len(jobIDFiles.get(key)))
	#raw_input()
	name = os.path.basename(jobIDFiles.get(key)[0])
	with open(sys.argv[3] +'/' +name , 'w') as outFile:
		libList = []
		for fPath in jobIDFiles.get(key):
			with open(fPath) as infile:
				for line in infile:
					libList.append(line.strip()) 
		libList = sorted(list(set(libList)))
		for lib in libList:
			print >> outFile, lib
	

#print len(list(set(jobIDs)))
