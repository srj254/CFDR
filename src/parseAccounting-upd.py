#!/usr/bin/python

import os
import sys
import re
import pandas as pd
import scipy  as sp
import numpy  as np
import taccStatsExtract as taccExtract 
from collections import defaultdict

fields 	= []
keysArr = []
count   = 0
pgFltArray = []
global taccDB
taccDB 	= None

def jobConcentrationOnExecHost(execHostStr):
	hostCount = defaultdict(int)
	hostList  = execHostStr.split('+')
	tempList  = []
	for host in hostList:
		tempList.append(host.split('/')[0])
	for item in tempList:
		hostCount[item] += 1
	val = (float(len(hostList))/float(len(hostCount.keys())))
	return int(val*100), len(hostCount.keys()), len(hostList)

def findPageFaults(execHostStr, jobStart, jobEnd):
	global pgFltArray
	hostList  = []
	for host in execHostStr.split('+'):
		hostList.append(host.split('/')[0])
	hostList  = list(set(hostList))
	minPgFlt = 0
	maxPgFlt = 0
	flag = False
	for host in hostList:
		nodeNumber = int((host.split('-')[1])[1:])
		pagefaultsPer10Mins = taccExtract.extractTaccStats(taccDB, nodeNumber, 'vm', 'pgmajfault,E', int(jobStart), int(jobEnd))
#		print host, nodeNumber, jobStart, int(jobStart), jobEnd, int(jobEnd)
#		print pagefaultsPer10Mins
#		print np.diff(pagefaultsPer10Mins)
#		print np.amax(list(np.diff(pagefaultsPer10Mins)))
		if len(pagefaultsPer10Mins) < 2:
			maxPgFlt = 0
			flag = True
		elif maxPgFlt < np.amax(list(np.diff(pagefaultsPer10Mins))):
			maxPgFlt = np.amax(list(np.diff(pagefaultsPer10Mins)))
			pgFltArray.append(maxPgFlt)
	return maxPgFlt, flag
		
def parseLine(line):
	global count
	VAR_DEBUG_EN = 0; 
	# can be changed to raw_input() so that debug prints can be controlled
	# print "Enter 1 to print the parsed string"
	# VAR_DEBUG_EN = int(raw_input())
	tokens = line.split(';')
	if 'E' not in tokens:
		return
	keyValDict = {}
	item = tokens[-1]
	keyValDict['LogTS'] = tokens[0]
	keyValDict['JobStatus'] = tokens[1]
	keyValDict['JobID'] = tokens[2].split('.', 1)[0]
	keyValDict['LoggerHostName'] = tokens[2].split('.', 1)[1]
	keyValues = item.split(' ')
	for keyVal in keyValues:
		myString = keyVal
		if 2 == keyVal.count('='):
			pairs = myString.split(':')
			pairs[0] = pairs[0].strip('\n')+","+pairs[-1].split('=')[-1]
			myString = pairs[0]
		pair = myString.split('=')
		keyValDict[pair[0].strip('\n')] = pair[1].strip('\n')
		if VAR_DEBUG_EN == 1: 
			print '*************************************'
			print myString
			print '*************************************'
			print pair
			VAR_DEBUG_EN = 0
	
	jobDensity, uniqHosts, totalCores = jobConcentrationOnExecHost\
					(keyValDict.get('exec_host'))
	keyValDict['jobDensity'] = str(jobDensity)
	keyValDict['uniqHosts']  = str(uniqHosts)
	keyValDict['totalCores'] = str(totalCores)
	maxPgFlt, flag = findPageFaults(keyValDict.get('exec_host'), keyValDict.get('start'), keyValDict.get('end'))
#	print "Max Page Fault", maxPgFlt
#	raw_input()
	count += int(flag)
	keyValDict['maxMajPgFlt']= str(int(maxPgFlt))
	fields.append(keyValDict)
	
def getAccData(filePath):
	for root, dirNames, fileNames in os.walk(filePath):
		for fileName in fileNames:
			with open(os.path.join(root, fileName), "r") as f:
				for line in f.readlines():
					parseLine(line)	
	return fields

if __name__ == "__main__":
	if len(sys.argv) < 4:
        	print "Usage: ./parseAccouting.py <Path to Accounting files> <file to Write> <taccStatsPath> <Arguments(Optional. Keep it empty if not sure)>", "\n",\
		      	"(Provide the exact keywords or attribute names in <Arguments> to",\
			"generate statistics for only that column in the statistics file)"
	        exit()
	
	taccStatsPath = sys.argv[3]
	taccDB = taccExtract.createTaccDB(taccStatsPath)

	getAccData(sys.argv[1])
	print "Count Zeros", count
	print "Max" , np.amax(pgFltArray)
	print "Min" , np.amin(pgFltArray)
	print "Mean", np.mean(pgFltArray)

	for field in fields:
		for key in field.keys():
			if key not in keysArr:
				keysArr.append(key)
	keysArr.sort()

	argc = len(sys.argv)
	columnKeys = []
	if argc > 4:
		columnKeys.append('JobID')
		for key in sys.argv[3:]:
			if key not in keysArr:
				print 'Wrong Input:' + key
				raw_input()
			else:
				columnKeys.append(key)
		print columnKeys
	else:
		columnKeys = keysArr

	statisticsFile = open(sys.argv[2], "w")
	print >> statisticsFile, '\t'.join(key for key in columnKeys)

	na_Values = []
	for field in fields:
		valuesArr = []
		for key in columnKeys:
			value = field.get(key) 
			if value is None:
				valuesArr.append('-NA-')
			else:
				valuesArr.append(value)
		print >> statisticsFile, '\t'.join(valuesArr)
	statisticsFile.close()

