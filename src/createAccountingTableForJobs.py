#!/usr/bin/python

import os
import sys
import re
import math
import pandas as pd
import scipy  as sp
import numpy  as np
import taccStatsExtract as taccExtract 
from collections import defaultdict

fields 	= []
keysArr = []
count   = 0
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

allJobIORead  = []
allJobIOWrite = []
def findBlockIOusage(execHostStr, jobStart, jobEnd):
	global  allJobIORead
	global	allJobIOWrite

	hostList  = []
	for host in execHostStr.split('+'):
		hostList.append(host.split('/')[0])
	hostList  = list(set(hostList))

	readBytes	= 0.0
	writeBytes	= 0.0

	peakReadBytes	= 0.0
	peakWriteBytes	= 0.0

	flag = False
	
	for host in hostList:
		nodeNumber = int((host.split('-')[1])[1:])
		readSectorsPer10mins = taccExtract.extractTaccStats(taccDB,\
					 nodeNumber, 'block', 'rd_sectors,E,U=512B',\
					 int(jobStart), int(jobEnd))
		writeSectorsPer10mins = taccExtract.extractTaccStats(taccDB,\
					 nodeNumber, 'block', 'wr_sectors,E,U=512B',\
					 int(jobStart), int(jobEnd))

		allJobIORead.extend(np.diff(readSectorsPer10mins))
		allJobIOWrite.extend(np.diff(writeSectorsPer10mins))
	
		if len(readSectorsPer10mins) > 0:
			totalRead = readSectorsPer10mins[-1] - readSectorsPer10mins[0]
			if len(readSectorsPer10mins) > 1:
				if peakReadBytes < np.amax(np.diff(readSectorsPer10mins)):
					peakReadBytes 	= np.amax(np.diff(readSectorsPer10mins))
		else:
			totalRead = 0
	
		if len(writeSectorsPer10mins) > 0:
			totalWrite = writeSectorsPer10mins[-1] - writeSectorsPer10mins[0]
			if len(writeSectorsPer10mins) > 1:
				if (peakWriteBytes < np.amax(np.diff(writeSectorsPer10mins))):
					peakWriteBytes 	= np.amax(np.diff(writeSectorsPer10mins))
		else:
			totalWrite = 0
	
		
		readBytes 	+= totalRead
		writeBytes 	+= totalWrite

	
	readBytes = readBytes*512
	writeBytes= writeBytes*512
	peakReadBytes = peakReadBytes*512
	peakWriteBytes= peakWriteBytes*512

	if math.isnan(readBytes) or math.isnan(readBytes) or math.isnan(readBytes) or math.isnan(readBytes):
		print "findBlockIOusage, NAN found!!"

	return readBytes, writeBytes, peakReadBytes, peakWriteBytes

allLliteRead = []
allLliteWrite= []
def findlliteUsage(execHostStr, jobStart, jobEnd):
	global 	allLliteRead
	global	allLliteWrite

	hostList  = []
	for host in execHostStr.split('+'):
		hostList.append(host.split('/')[0])
	hostList  = list(set(hostList))

	readBytes	= 0.0
	writeBytes	= 0.0

	peakReadBytes	= 0.0
	peakWriteBytes	= 0.0

	for host in hostList:
		nodeNumber = int((host.split('-')[1])[1:])
		readBytesPer10mins = taccExtract.extractTaccStats(taccDB,\
					 nodeNumber, 'llite', 'read_bytes,E,U=B',\
					 int(jobStart), int(jobEnd))
		writeBytesPer10mins = taccExtract.extractTaccStats(taccDB,\
					 nodeNumber, 'llite', 'write_bytes,E,U=B',\
					 int(jobStart), int(jobEnd))

		allLliteRead.extend(np.diff(readBytesPer10mins))
		allLliteWrite.extend(np.diff(writeBytesPer10mins))
	
		if len(readBytesPer10mins) > 0:
			totalRead = readBytesPer10mins[-1] - readBytesPer10mins[0]
			if len(readBytesPer10mins) > 1:
				if peakReadBytes < np.amax(np.diff(readBytesPer10mins)):
					peakReadBytes 	= np.amax(np.diff(readBytesPer10mins))
		else:
			totalRead = 0
	
		if len(writeBytesPer10mins) > 0:
			totalWrite = writeBytesPer10mins[-1] - writeBytesPer10mins[0]
			if len(writeBytesPer10mins) > 1:
				if peakWriteBytes < np.amax(np.diff(writeBytesPer10mins)):
					peakWriteBytes = np.amax(np.diff(writeBytesPer10mins))
		else:
			totalWrite = 0
		
		readBytes 	+= totalRead
		writeBytes 	+= totalWrite

	if math.isnan(readBytes) or math.isnan(readBytes) or math.isnan(readBytes) or math.isnan(readBytes):
		print "findlliteusage, NAN found!!"

	return readBytes, writeBytes, peakReadBytes, peakWriteBytes

allIBRead  = []
allIBWrite = []
def findIBUsage(execHostStr, jobStart, jobEnd):
	global allIBRead
	global allIBWrite

	hostList  = []
	for host in execHostStr.split('+'):
		hostList.append(host.split('/')[0])
	hostList  = list(set(hostList))

	readBytes	= 0.0
	writeBytes	= 0.0

	peakReadBytes	= 0.0
	peakWriteBytes	= 0.0

	for host in hostList:
		nodeNumber = int((host.split('-')[1])[1:])
		readBytesPer10mins = taccExtract.extractTaccStats(taccDB,\
					 nodeNumber, 'ib_ext', 'port_rcv_data,E,U=4B',\
					 int(jobStart), int(jobEnd))
		writeBytesPer10mins = taccExtract.extractTaccStats(taccDB,\
					 nodeNumber, 'ib_ext', 'port_xmit_data,E,U=4B',\
					 int(jobStart), int(jobEnd))

		allIBWrite.extend(np.diff(readBytesPer10mins))
		allIBRead.extend(np.diff(writeBytesPer10mins))
	
		if len(readBytesPer10mins) > 0:
			totalRead = readBytesPer10mins[-1] - readBytesPer10mins[0]
			if len(readBytesPer10mins) > 1:
				if peakReadBytes < np.amax(np.diff(readBytesPer10mins)):
					peakReadBytes 	= np.amax(np.diff(readBytesPer10mins))
		else:
			totalRead = 0
	
		if len(writeBytesPer10mins) > 0:
			totalWrite = writeBytesPer10mins[-1] - writeBytesPer10mins[0]
			if len(writeBytesPer10mins) > 1:
				if peakWriteBytes < np.amax(np.diff(writeBytesPer10mins)):
					peakWriteBytes 	= np.amax(np.diff(writeBytesPer10mins))
		else:
			totalWrite = 0
		
		readBytes 	+= totalRead
		writeBytes 	+= totalWrite

	if math.isnan(readBytes) or math.isnan(readBytes) or math.isnan(readBytes) or math.isnan(readBytes):
		print "findIBEXTusage, NAN found!!"

	return (readBytes*4), (writeBytes*4), (peakReadBytes*4), (peakWriteBytes*4)

def findMemUsage(execHostStr, jobStart, jobEnd):

	hostList  = []
	for host in execHostStr.split('+'):
		hostList.append(host.split('/')[0])
	hostList  = list(set(hostList))

	peakMemUsed = []
	avgMemUsed  = []

	for host in hostList:
		nodeNumber = int((host.split('-')[1])[1:])
		memChanges = taccExtract.extractTaccStats(taccDB,\
					 nodeNumber, 'mem', 'MemUsed,U=KB',\
					 int(jobStart), int(jobEnd))

		if len(memChanges) > 0:
			peakMemUsed.append(np.amax(memChanges))
			avgMemUsed.append(np.mean(memChanges))

	peakMem = np.mean(peakMemUsed)
	avgMem   = np.mean(avgMemUsed)

	if math.isnan(peakMem):
		peakMem = 0
	if math.isnan(avgMem):
		avgMem = 0
	
	return peakMem, avgMem

allPageFltDiffs = []
def findPageFaults(execHostStr, jobStart, jobEnd):
	global allPageFltDiffs

	hostList  = []
	for host in execHostStr.split('+'):
		hostList.append(host.split('/')[0])
	hostList  = list(set(hostList))
	pageFlt 	= 0.0
	peakPgFlt 	= 0.0
	avgJumpsPgFlt 	= 0.0
	flag = False
	
	for host in hostList:
		nodeNumber = int((host.split('-')[1])[1:])
		pagefaultsPer10Mins = taccExtract.extractTaccStats(taccDB,\
					 nodeNumber, 'vm', 'pgmajfault,E',\
					 int(jobStart), int(jobEnd))
	
		a = np.diff(pagefaultsPer10Mins)
		allPageFltDiffs.extend(a)
#		print a
#		print pagefaultsPer10Mins, nodeNumber, jobStart, jobEnd
#		raw_input()
	
		if len(pagefaultsPer10Mins) > 0:
			totalPageFaults = pagefaultsPer10Mins[-1] - pagefaultsPer10Mins[0]
			if len(pagefaultsPer10Mins) > 1:
				if peakPgFlt < np.amax(np.diff(pagefaultsPer10Mins)):
					peakPgFlt 	= np.amax(np.diff(pagefaultsPer10Mins))
					avgJumpsPgFlt   = np.mean(np.diff(pagefaultsPer10Mins))
		else:
			totalPageFaults = 0
			flag = True
		
		if totalPageFaults > pageFlt:
			pageFlt = totalPageFaults
		
	return pageFlt, peakPgFlt, avgJumpsPgFlt, flag
		
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
	
	majPgFlt, peakPgFlt, avgPgFltJumps, flag = findPageFaults(keyValDict.get('exec_host'), \
						keyValDict.get('start'), keyValDict.get('end'))
	count += int(flag)
	keyValDict['MajPgFlt']   = str(int(majPgFlt))
	keyValDict['PeakPgFlt']  = str(int(peakPgFlt))
	if peakPgFlt > 200:
		keyValDict['Thrashing']  = str(True)
	else:
		keyValDict['Thrashing']  = str(False)

	keyValDict['AvgPgFltJumps'] = str(int(avgPgFltJumps))
	if (float(keyValDict.get('end')) - float(keyValDict.get('start'))) > 0:
		keyValDict['majPgFltRate'] = str (float(majPgFlt)/\
						 (float(keyValDict.get('end')) -\
						  float(keyValDict.get('start'))))
	else:
		keyValDict['majPgFltRate'] = str(0)

	ibRead, ibWrite, ibPeakRead, ibPeakWrite = findIBUsage(keyValDict.get('exec_host'),\
						 keyValDict.get('start'), keyValDict.get('end'))
	blkRead, blkWrite, blkPeakRead, blkPeakWrite = findBlockIOusage(keyValDict.get('exec_host'),\
						 keyValDict.get('start'), keyValDict.get('end')) 
	llteRead, llteWrite, lltePeakRead, lltePeakWrite = findlliteUsage(keyValDict.get('exec_host'), \
						 keyValDict.get('start'), keyValDict.get('end'))
	avgPeakMem, avgMem 			 = findMemUsage(keyValDict.get('exec_host'), \
	                                         keyValDict.get('start'), keyValDict.get('end'))

	keyValDict['ibReadInB']  	= str(int(ibRead))
	keyValDict['ibWriteInB']	= str(int(ibWrite))
	keyValDict['ibPeakReadInB'] 	= str(int(ibPeakRead))
	keyValDict['ibPeakWriteInB']	= str(int(ibPeakWrite))

	keyValDict['blkReadInB']	= str(int(blkRead))
	keyValDict['blkWriteInB']	= str(int(blkWrite))
	keyValDict['blkPeakReadInB']	= str(int(blkPeakRead))
	keyValDict['blkPeakWriteInB']	= str(int(blkPeakWrite))
	
	keyValDict['llteReadInB']	= str(int(llteRead))
	keyValDict['llteWriteInB']	= str(int(llteWrite))
	keyValDict['lltePeakReadInB']	= str(int(lltePeakRead))
	keyValDict['lltePeakWriteInB']	= str(int(lltePeakWrite))
	
	keyValDict['avgPeakMemInKB']	= str(int(avgPeakMem))
	keyValDict['avgMemInKB']	= str(int(avgMem))
	
	fields.append(keyValDict)
	
def getAccData(filePath):
	acount = 0
	for root, dirNames, fileNames in os.walk(sys.argv[1]): 
		for fileName in fileNames:
			with open(os.path.join(root, fileName), "r") as f:
				for line in f.readlines():
					acount += 1
					parseLine(line)
			if acount > 5000:
				print "5000 Done"
				acount = 0
	return fields

if __name__ == "__main__":
	if len(sys.argv) < 4:
        	print "Usage: ./createAccountingTableForJobs.py <Path to Accounting files> <file to Write> <taccStatsPath> <Arguments(Optional. Keep it empty if not sure)>", "\n",\
		      	"(Provide the exact keywords or attribute names in <Arguments> to",\
			"generate statistics for only that column in the statistics file)"
	        exit()
	
	taccStatsPath = sys.argv[3]
	taccDB = taccExtract.createTaccDB(taccStatsPath)
	print "TACC DB Done!"
	getAccData(sys.argv[1])
	print "AccStats Done!"
	with open("Diff.tsv", 'w') as diffi:
		print >> diffi, ",".join(str(diff) for diff in allPageFltDiffs)
	print "Done !!"
	allPageFltDiffs = filter(lambda x: x>0 , allPageFltDiffs)
	print np.mean(allPageFltDiffs), (np.std(allPageFltDiffs))

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

