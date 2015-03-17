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
#			print username
#			raw_input()

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
			if ('so' not in lib) or (2 >= len(lib)):
#				print "passing"+ lib +"passed"
				continue
			print >> outFile, lib
			try: 
				libname = (lib.rsplit('/', 1)[1]).split('.so')[0]+ '.so'
			except:
				print "libname"+str(len(lib))+"is this"+ str('so' not in lib)
				libname = raw_input()
			libname = libname.lower()
#			print lib, libname
#			raw_input()
			try:
				libnameTable[libname] = libnameTable.get(libname) + 1;
			except:
				libnameTable[libname] = 1;
			try:
				libs2Users[libname].append(jobID2User.get(key))
			except:
				libs2Users[libname] = [username]

with open(sys.argv[3]+"/libraryTable", 'w') as f:
	for key in libnameTable.keys():
		print >> f, key, ",", libnameTable.get(key)
	

with open(sys.argv[3]+"/lib2Users", 'w') as f:
	for key in libs2Users.keys():
		print >> f, key, ",", len(list(set(libs2Users.get(key))))

mylist = []

for key in jobID2User.keys():
	mylist.append(jobID2User.get(key))

print "Unique Users: ", len(list(set(mylist))), "JobIDs: ",len(jobID2User.keys())
#print list(set(mylist))

#print len(list(set(jobIDs)))
