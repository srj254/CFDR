#!/usr/bin/python

import os
import re
import sys
import parseAccounting as accDataParser
import liblistAnalysis as libListAnalyser

import numpy as np
import scipy 
from scipy import stats

def cnvtTime(timeString):
	time = timeString.split(':')
	result = int(time[0])*3600 + int(time[1])*60 + int(time[0])
	return result

jobGroups  = {}
jobStats   = {}
statistics = []
#Important Parameters to be set before running the file
VAR_MINSIZE_OF_GRP 	= 10;
SCORE_AT_PRCNTLE	= 95;
VAR_DEBUG_EN		= 0;

print "Make sure you don't have stale Outlier files in the provided destination path <Path to write Outlier Jobs>"
if len(sys.argv) < 10:
	print "Usage " + "./findOutliers.py <AccoutingData> <LibListPath> <conte | hansen> <writeToFile (0 | 1)> <whereToWriteJobGroups> <Path to write Outlier Jobs> <Minimum size of the Group> <Outlier Percentile score (0 to 100)> <Value2Use (w,c,m,v)>"
	exit()

VAR_MINSIZE_OF_GRP	= int(sys.argv[7])
SCORE_AT_PRCNTLE	= float(sys.argv[8])
if len(sys.argv[9]) > 1:
	print "Value2Use should be a character argument (w, c, m, v)"
	exit()

if SCORE_AT_PRCNTLE > 100 or SCORE_AT_PRCNTLE < 0:
	print "Percentile number is invalid"
	exit()

jobGroups  = libListAnalyser.groupJobs(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
for key in jobGroups.keys():
	if len(jobGroups.get(key)) != len(list(set(jobGroups.get(key)))):
		print "Not equal ", key
		raw_input()
statistics = accDataParser.getAccData(sys.argv[1])

#print len(jobGroups.keys())
#for jobGroupNumber in jobGroups.keys():
#	print type(jobGroups.get(jobGroupNumber))
#	print str(jobGroupNumber) + '-> ' + ' '.join(jobID for jobID in jobGroups.get(jobGroupNumber))

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

#print type(jobStats.get('7853184'))
#print jobStats.get('7853184').get('resources_used.walltime')
#print jobStats.get('7853184')

Groups = 0
for jobGroupNumber in jobGroups.keys():
	if len(jobGroups.get(jobGroupNumber)) < VAR_MINSIZE_OF_GRP:
		continue

	tempJobList = []
	tempWTime   = []
	tempCTime   = []
	tempMemUsed = []
	tempVMemUsed= []
	tempUserName= []

	for jobID in jobGroups.get(jobGroupNumber):
		try:
#			print jobID + "-> ", str(type(jobStats.get(jobID)))
#			print jobID, type(jobID)
			walltime = cnvtTime(jobStats.get(jobID).get('resources_used.walltime'))
			cputime  = cnvtTime(jobStats.get(jobID).get('resources_used.cput'))
			pattern  = re.compile("(\d+)(\((\d+)\))*")
			matches  = pattern.match(jobStats.get(jobID).get('Resource_List.nodes'))
			matches  = list(matches.groups())
			matches  = filter(None, matches)
			if len(matches) == 3 :
				cputime = cputime/((int(matches[0])) * (int(matches[2])))
			elif len(matches) == 1:
				cputime = cputime/(int(matches[0]))
			else:
				print(matches)	
		except Exception as e:
			#print 'T', jobID, e
			pass
		try:
			memused  = float((jobStats.get(jobID).get('resources_used.mem')).strip('kb'))
			vmemused = float((jobStats.get(jobID).get('resources_used.vmem')).strip('kb'))
#			print str(jobID), cputime, walltime, int(jobStats.get(jobID).get('end')) - int(jobStats.get(jobID).get('start')), memused, vmemused
		except Exception as e:
			#print 'M', jobID, e
			pass

		tempJobList.append(jobID)
		tempWTime.append(walltime)
		tempCTime.append(cputime)
		tempMemUsed.append(memused)
		tempVMemUsed.append(vmemused)
		try:
			tempUserName.append(jobStats.get(jobID).get('user'))
		except Exception as e:
			tempUserName.append("-NA-")	
			pass	
	Groups += 1
	if 	sys.argv[9] is 'w':
		array2use = tempWTime
	elif 	sys.argv[9] is 'c':
		array2use = tempCTime
	elif 	sys.argv[9] is 'v':
		array2use = tempVMemUsed
	elif 	sys.argv[9] is 'm':
		array2use = tempMemUsed
	
# 	code to identify the outliers above 1.5 times median value	
	try:
		myval = 0
		threshold = float(stats.scoreatpercentile(array2use, SCORE_AT_PRCNTLE))
		medianVal = float(stats.scoreatpercentile(array2use, 50))
		difference = threshold - float((float(1.5))*(float(medianVal)))

#		check if the threshold at 95th percentile is at least 5 seconds apart from median
		if(difference < 0):
			continue
		else:
			f = open(sys.argv[6] + "/" + str(jobGroupNumber) + sys.argv[9], "w")
			for index, value in enumerate(array2use):
				if value < threshold:
					continue
				
				try:
					myval = jobStats.get(tempJobList[index]).get('Resource_List.nodes')
				except Exception as e:
					myval = "(NA)"
				print >>f, tempJobList[index], tempUserName[index], 'W '+ str(tempWTime[index]), 'C '+str(tempCTime[index]), myval, 'M ' + str(tempMemUsed[index]), 'V '+ str(tempVMemUsed[index])
			f.close()
	except Exception as e:
		print e
		pass

	try:
		myval = 0
		sixtyPcntl  = float(stats.scoreatpercentile(array2use, 60))
		fortyPcntl  = float(stats.scoreatpercentile(array2use, 40))
		
		twentyPcntl = float(stats.scoreatpercentile(array2use, 20))
		thirtyPcntl = float(stats.scoreatpercentile(array2use, 30))
		
		firstPcntl = float(stats.scoreatpercentile(array2use, 1))
		fifthPcntl = float(stats.scoreatpercentile(array2use, 5))
		
		f = open(sys.argv[6] + "/" + str(jobGroupNumber) + "N" + sys.argv[9] , "w")
		flag = False
		for index, value in enumerate(array2use):
			attr = ""
			if fortyPcntl <= value <= sixtyPcntl:
				attr = "50P"
			elif twentyPcntl <= value <= thirtyPcntl:
				attr = "25P"
			elif firstPcntl <= value <= fifthPcntl:
				attr = "01P"
			else:
				continue
		
			try:
				myval = jobStats.get(tempJobList[index]).get('Resource_List.nodes')
			except Exception as e:
				myval = "(NA)"
			flag = True
			print >>f, tempJobList[index], tempUserName[index], 'W '+ str(tempWTime[index]), 'C '+str(tempCTime[index]), myval, 'M ' + str(tempMemUsed[index]), 'V '+ str(tempVMemUsed[index]), "Percentile "+ attr
		
		f.close()
		if flag == False:
			print jobGroupNumber, " Has no Normal files!!!!"
			os.remove(sys.argv[6] + "/" + str(jobGroupNumber) + "N" + sys.argv[9])
			raw_input()
	except Exception as e:
		print e
		pass

