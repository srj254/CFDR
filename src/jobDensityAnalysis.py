#!/usr/bin/python

import os
import re
import sys
import time
import parseAccounting as accDataParser
import liblistAnalysis as libListAnalyser
import matplotlib.pyplot as plt
import numpy as np
import scipy 
from scipy import stats
from collections import defaultdict

def cnvtTime(timeString):
	if timeString is None:
		return 0
	time = timeString.split(':')
	result = int(time[0])*3600 + int(time[1])*60 + int(time[0])
	return result

def getJobStats(jobs):
	wtime  = defaultdict(dict)
	cputime= defaultdict(dict)
	for job in jobs:
		try:
			wtime[job] 	= cnvtTime(jobStats.get(job).get('resources_used.walltime'))
		except:
			wtime[job] 	= cnvtTime('00:00:00')
			print "Enter a Key"
			raw_input()
		try:
			cputime[job] 	= cnvtTime(jobStats.get(job).get('resources_used.cput'))
		except:
			cputime[job] 	= cnvtTime('00:00:00')
			print "Enter a Key again"
			raw_input()
	return wtime, cputime
			
jobGroups  = {}
jobStats   = {}
statistics = []
#Important Parameters to be set before running the file
VAR_DEBUG_EN		= 0;

if len(sys.argv) < 5:
	print "Usage " + "./<Script Name>.py <AccoutingData> <LibListPath> <PathToWrite> <jDensity>"
	exit()

print sys.argv[3]+"/DenseAndSparseJobs"+str(int(sys.argv[4]))+".tsv"

temp = int(sys.argv[4])
print "Jobs are being grouped", time.time()
jobGroups  = libListAnalyser.groupJobs(sys.argv[2], 'conte', 0, sys.argv[3])
for key in jobGroups.keys():
	if len(jobGroups.get(key)) != len(list(set(jobGroups.get(key)))):
		print "Not equal ", key
		raw_input()

print "Jobs are Grouped", time.time()
statistics = accDataParser.getAccData(sys.argv[1])
print "Account stats are parsed", time.time()

for record in statistics:
	jobStats[record.get('JobID')] = record

jobList = []
for grpNum in jobGroups.keys():
	jobList.extend(jobGroups.get(grpNum))

if VAR_DEBUG_EN == 1:
	print len(jobList)
	print len(jobStats.keys())
	raw_input()
	diff = set(jobList) - set(jobStats.keys())
	print len(list(diff))
	raw_input()
	diff = set(jobStats.keys()) - set(jobList)
	print len(list(diff))
	raw_input()

denseJobGrp 	= {}
sparseJobGrp  	= {}
for grpNum in jobGroups.keys():
	sparseJobs   	= defaultdict(list)
	denseJobs 	= defaultdict(list)

	for jobID in jobGroups.get(grpNum):
		try:
			jobRecord = jobStats.get(jobID)
			jobDensity= int(jobRecord.get('jobDensity'))
			totalCores= int(jobRecord.get('totalCores'))
			if totalCores < 4:
				continue
		except AttributeError:
			continue

		if jobDensity > (int(sys.argv[4])):
			denseJobs[totalCores].append(jobID)			
		else:
			sparseJobs[totalCores].append(jobID)	

	denseJobGrp[grpNum] 	= denseJobs
	sparseJobGrp[grpNum]  	= sparseJobs
	
f = open(sys.argv[3]+"/DenseAndSparseJobs"+str(int(sys.argv[4]))+".tsv", 'w')
print >> f, "GroupNum\tNumcore\tSize\tWtimeMed\tWtimeMean\tWtimeSdev\tWtMax\tWtMin\tCPUtimeMed\tCPUtimeMean\tCPUtimeSdev\tCPUtMAx\tCPUtMin\tIsDense"
for grpNum in denseJobGrp.keys():
	denseJobs =  denseJobGrp.get(grpNum)
	for totalCores in denseJobs.keys():
		jobs = denseJobs.get(totalCores)
		jobs = sorted(jobs)
		walltimes, cputimes = getJobStats(jobs)
		print >> f, "%8d\t%8d\t%5d\t%8f\t%8f\t%8f\t%8f\t%8f\t%8f\t%8f\t%8f\t%8f\t%8f\t%5d"\
			%(grpNum,\
			totalCores,\
			len(jobs), \
			np.median(walltimes.values()), \
			np.mean(walltimes.values()), \
			np.std(walltimes.values()), \
			np.amax(walltimes.values()), \
			np.amin(walltimes.values()), \
			np.median(cputimes.values()), \
			np.mean(cputimes.values()), \
			np.std(cputimes.values()), \
			np.amax(cputimes.values()), \
			np.amin(cputimes.values()), \
			True)

for grpNum in sparseJobGrp.keys():
	sparseJobs =  sparseJobGrp.get(grpNum)
	for totalCores in sparseJobs.keys():
		jobs = sparseJobs.get(totalCores)
		jobs = sorted(jobs)
		walltimes, cputimes = getJobStats(jobs)
		print >> f, "%8d\t%8d\t%5d\t%8f\t%8f\t%8f\t%8f\t%8f\t%8f\t%8f\t%8f\t%8f\t%8f\t%5d"\
			%(grpNum,\
			totalCores,\
			len(jobs), \
			np.median(walltimes.values()), \
			np.mean(walltimes.values()), \
			np.std(walltimes.values()), \
			np.amax(walltimes.values()), \
			np.amin(walltimes.values()), \
			np.median(cputimes.values()), \
			np.mean(cputimes.values()), \
			np.std(cputimes.values()), \
			np.amax(cputimes.values()), \
			np.amin(cputimes.values()), \
			False)

f.close()

'''
singleGrpDict = {}
for key in singleNodeGrp.keys():
	wtimeArr = []
	for jobID, wtime in singleNodeGrp.get(key):
		wtimeArr.append(cnvtTime(wtime))#/int(jobStats.get(jobID).get('totalCores')))
	singleGrpDict[key] = [np.mean(wtimeArr), np.median(wtimeArr), np.std(wtimeArr)]

multiGrpDict = {}
for key in multiNodeGrp.keys():
	wtimeArr = []
	for jobID, wtime in multiNodeGrp.get(key):
		wtimeArr.append(cnvtTime(wtime))#/int(jobStats.get(jobID).get('totalCores')))
	multiGrpDict[key] = [np.mean(wtimeArr), np.median(wtimeArr), np.std(wtimeArr)]

for key in list(set(singleGrpDict.keys()+multiGrpDict.keys())):
	if singleGrpDict.get(key) is not None and multiGrpDict.get(key) is not None and \
	   len(singleNodeGrp.get(key)) > 5 and len(multiNodeGrp.get(key)) > 5:
#		print str(key) + "," + str(len(singleNodeGrp.get(key))) + "," +\
#		               	",".join(str(item) for item in singleGrpDict.get(key))+","+\
#			       	str(len( multiNodeGrp.get(key))) +"," + \
#			       	",".join(str(item) for item in  multiGrpDict.get(key))
		with open(str(key)+".csv", "w") as ofile:
			for jID, wtime in singleNodeGrp.get(key):
				print >> ofile, jID, ",", cnvtTime(wtime) 
			print >> ofile, "Demiliter", "Here"
			for jID, wtime in multiNodeGrp.get(key):
				print >> ofile, jID, ",", cnvtTime(wtime)
'''
