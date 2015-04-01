#!/usr/bin/python

import re
import os.path
import sys
import time
import string 

if len(sys.argv) < 4:
	print "Usage ./<Executable file Name> <Path to Tacc stats files> <range Low> <range high>"
	exit()

taccStatsFileName = sys.argv[1]
schemaTypes = [];
timestamp = 0;

global tempTaccDict
tempTaccDict = {}

def parseSystemInfo(filePath, line):
	sysInfo = line.split(' ')
#	f = open(filePath+ '/'+ 'SystemInformationTable.tsv', 'a')
#	print sysInfo
#	print >> f, '\t'.join((field.strip()) for field in sysInfo)
#	f.close()
    
def parseSchemaDescriptor(filePath, line):
	global tempTaccDict
	fields = line.split(' ')
	schemaTypes.append(fields[0])
	if os.path.isfile(filePath+ '/'+ fields[0]+'.tsv'):
		return
#	print filePath+ '/'+ fields[0]+'.tsv'
	f = open(filePath+ '/'+ fields[0]+'.tsv', 'w')
	tempTaccDict[filePath+ '/'+ fields[0]+'.tsv'] = []
	fields[0] = 'Identifier'
	fields.insert(0,'Timestamp')
#	print fields
	print >> f, '\t'.join(field.strip() for field in fields)
	f.close()

def statsParser(filePath, line):
	global tempTaccDict 
	global timestamp

	if (re.match('^\$', line)):
#		print "Sysinformation>>", line[1:]
        	(parseSystemInfo(filePath, line[1:]))
	elif (re.match('^!', line)):
#		print "!Schema>>", line[1:]
        	(parseSchemaDescriptor(filePath, line[1:]))
	elif line.split(' ')[0] in schemaTypes:
#		print "Schema Types>>", line
#	        f = open(filePath + '/' + line.split(' ')[0] + '.tsv', 'a')
        	fieldInfo = line.split(' ')[1:]
	        fieldInfo.insert(0,timestamp)
#		print fieldInfo
		tempLine  = '\t'.join((str(info).strip()) for info in fieldInfo)
		tempTaccDict[filePath + '/' + line.split(' ')[0] + '.tsv'].append(tempLine)
#		print >> f, '\t'.join((str(info).strip()) for info in fieldInfo)
#	        f.close()
	else:
#		print "else>>", line
        	if len(line.split(' ')) == 2:
			try:
	        		timestamp = int(line.split(' ')[0])
				oldtimestamp = timestamp
			except:
				pass	
#	       		print timestamp
		else:
			pass
#			print "TIMESTAMP NOT FOUND!!!!!"
#	raw_input()
    
## Program starts Here ##
        
root, subDirs, fileNames = next(os.walk(taccStatsFileName))

for subDir in subDirs:
	tempTaccDict.clear()

	low = int(sys.argv[2])
	high= int(sys.argv[3])
	val = int((subDir.split('.')[0].split('-')[1])[1:])
	if low <= val and high > val:
		print subDir
#		print val
	else:
		continue

	for fileName in os.listdir(os.path.join(root, subDir)):
		if fileName.endswith(".tsv"):
			os.remove(os.path.join(root, subDir, fileName))	
			continue
		if not fileName.endswith(".gz"):
		        with open(os.path.join(root, subDir, fileName), 'r') as f:
                		for line in f:
		                	statsParser(os.path.join(root, subDir), line)

	for fileName in tempTaccDict.keys():
		with open(fileName, 'w') as writeFile:
			for line in tempTaccDict.get(fileName):
				print >> writeFile, line
#		print fileName
#	raw_input()
#	raw_input();
