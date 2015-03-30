#!/usr/bin/python

import os
import sys
import re

jobIDs = []

if len(sys.argv) < 4:
	print "Usage <Path to Liblist> <Keyword> <New path for results>"
	exit()

jobIDFiles 	= {}
libnameTable 	= {}
libs2Users	= {}
jobID2User	= {}
# Logic is to create dictionary of jobIDs where the values is a list of all liblist files corresponding to the jobID. 
for root, subdirs, filenames in os.walk(sys.argv[1]):
	for filename in filenames:
		if sys.argv[2] in filename:
			jobID = filename.split('_')[1].split('.')[0]
			username = filename.split('_')[0]
			jobID2User[jobID] = username;
			try: 
				jobIDFiles[jobID].append(os.path.join(root, filename))
			except KeyError:
				jobIDFiles[jobID] = [os.path.join(root, filename)]
print "Total number of Jobs: ", len(jobIDFiles.keys())

for key in jobIDFiles.keys():
	name = os.path.basename(jobIDFiles.get(key)[0])
	with open(sys.argv[3] +'/' +name , 'w') as outFile:
		libList = []
		for fPath in jobIDFiles.get(key):
			with open(fPath) as infile:
				for line in infile:
					libList.append(line.strip()) 
		libList = sorted(list(set(libList)))
		writeIntoFile = []		
		for lib in libList:
			if ('.so' not in lib) or (2 >= len(lib)):
				continue
			lib = lib.strip()
#			print >> outFile, lib
			try: 
				libname = (lib.rsplit('/', 1)[1]).split('.so')[0]+ '.so'
			except:
				print "libname: ", lib
				print "Enter the libname: "
				libname = raw_input()
			writeIntoFile.append(lib)	
			libname = libname.lower()
			try:
				libnameTable[libname] = libnameTable.get(libname) + 1;
			except:
				libnameTable[libname] = 1;
			try:
				libs2Users[libname].append(jobID2User.get(key))
			except:
				libs2Users[libname] = [username]
		print >> outFile, '\n'.join(lib for lib in writeIntoFile)

with open(sys.argv[3]+"/libraryTable", 'w') as f:
	for key in libnameTable.keys():
		print >> f, key, ",", libnameTable.get(key)
	

with open(sys.argv[3]+"/lib2Users", 'w') as f:
	for key in libs2Users.keys():
		print >> f, key, ",", len(list(set(libs2Users.get(key))))

mylist = []

for key in jobID2User.keys():
	mylist.append(jobID2User.get(key))

print "Unique Users: ", len(list(set(mylist))), "\nJobIDs: ",len(jobID2User.keys())
