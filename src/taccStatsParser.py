#!/usr/bin/python

import re
import os.path
import sys
import time
import string 

taccStatsFileName = sys.argv[1]
schemaTypes = [];
timestamp = 0;

def parseSystemInfo(filePath, line):
	sysInfo = line.split(' ')
	f = open(filePath+ '/'+ 'SystemInformationTable.tsv', 'a')
#	print sysInfo
	print >> f, '\t'.join((field.strip()) for field in sysInfo)
	f.close()
    
def parseSchemaDescriptor(filePath, line):
	fields = line.split(' ')
	schemaTypes.append(fields[0])
	f = open(filePath+ '/'+ fields[0]+'.tsv', 'w')
	fields[0] = 'Identifier'
	fields.insert(0,'Timestamp')
#	print fields
	print >> f, '\t'.join(field.strip() for field in fields)
	f.close()
       
def statsParser(filePath, line):
	global timestamp
	if (re.match('^\$', line)):
#		print "Sysinformation>>", line[1:]
        	(parseSystemInfo(filePath, line[1:]))
	elif (re.match('^!', line)):
#		print "!Schema>>", line[1:]
        	(parseSchemaDescriptor(filePath, line[1:]))
	elif line.split(' ')[0] in schemaTypes:
#		print "Schema Types>>", line
	        f = open(filePath + '/' + line.split(' ')[0] + '.tsv', 'a')
        	fieldInfo = line.split(' ')[1:]
	        fieldInfo.insert(0,timestamp)
#		print fieldInfo
		print >> f, '\t'.join((str(info).strip()) for info in fieldInfo)
	        f.close()
	else:
#		print "else>>", line
        	if len(line.split(' ')) == 2:
        		timestamp = int(line.split(' ')[0])
#	       		print timestamp
		else:
			pass
#			print "TIMESTAMP NOT FOUND!!!!!"
#	raw_input()
    
## Program starts Here ##
        
if len(sys.argv) < 2:
	print "Usage ./<Executable file Name> <Path to Tacc stats files>"
	exit()

root, subDirs, fileNames = next(os.walk(taccStatsFileName))

for subDir in subDirs:
	print subDir
	for fileName in os.listdir(os.path.join(root, subDir)):
		if fileName.endswith(".tsv"):
			os.remove(os.path.join(root, subDir, fileName))	
			continue
		if not fileName.endswith(".gz"):	
		        with open(os.path.join(root, subDir, fileName), 'r') as f:
                		for line in f:
		                	statsParser(os.path.join(root, subDir), line)
#	raw_input();
