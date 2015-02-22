#!/usr/bin/python

import os
import re
import sys

class job:
	jobID = ""
	attr  = ""
	dimension = ""
	def __init__(self, ID, jobAttr, dim):
		self.jobID = ID
		self.attr  = jobAttr
		self.dimension = dim

def parseLine(line):
	chunks = line.split(' ')
	return chunks

def getJobID(line):
	linechunks = parseLine(line)
	return linechunks[0];

def outlierAnalysis(filepath):
	flag = True;
	maxOutlrGrp = []
	outlierDict = {}
	normalDict  = {}

	for i in range(0,531):
		flag = True
		flag = flag and os.path.isfile(filepath+str(i)+'w')
		flag = flag and os.path.isfile(filepath+str(i)+'c')
		flag = flag and os.path.isfile(filepath+str(i)+'v')
		flag = flag and os.path.isfile(filepath+str(i)+'m')
		if flag == True :
			maxOutlrGrp.append(i)
	
	for groupNum in maxOutlrGrp:
		listw = []
		listc = []
		listv = []
		listm = []
		with open(filepath + str(groupNum) + 'w') as f:
			for line in f:
				listw.append(getJobID(line))
		with open(filepath + str(groupNum) + 'c') as f:
			for line in f:
				listc.append(getJobID(line))
		with open(filepath + str(groupNum) + 'v') as f:
			for line in f:
				listv.append(getJobID(line))
		with open(filepath + str(groupNum) + 'm') as f:
			for line in f:
				listm.append(getJobID(line))
		commonJobs = list(set(listw) & set(listc) & set(listv) & set(listm))
		if len(commonJobs) > 0:
			 outlierDict[groupNum] = commonJobs

	a = ['w', 'v', 'c', 'm']
	for groupNum in outlierDict.keys():
		listNProcessed = []
		for counter in range(0,4):	
			with open(filepath + "/" + str(groupNum) + 'N' + a[counter]) as f:
				listN = []
				for line in f:
					obj = job(getJobID(line), (str(parseLine(line)[-1])).strip(), a[counter])
					listN.append(obj)
				flag50 = False
				flag25 = False
				flag01 = False
				for item in listN:
					if item.attr == "50P" and flag50 == False:
						listNProcessed.append(item)
						flag50 = True
					elif item.attr == "25P" and flag25 == False:
						listNProcessed.append(item)
						flag25 = True
					elif item.attr == "01P" and flag01 == False:
					 	listNProcessed.append(item)
						flag01 = True
		normalDict[groupNum] = listNProcessed
#		print len(listNProcessed)
	return outlierDict, normalDict

				
if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "Usage ./outlierAnalysis.py <path to outliers> <path to processed liblist>"
		exit() 
	outlierJobs, normalJobsWithAttr = outlierAnalysis(sys.argv[1])
	for grpNum in outlierJobs.keys():
		print ",".join(job for job in outlierJobs.get(grpNum))

	for grpNum in outlierJobs.keys():
		print "*******************************************************************"
		temp = 0;
		for root, dirs, filenames in os.walk(sys.argv[2]):
			for f in filenames: 
				if any(job in f for job in outlierJobs.get(grpNum)) and f.endswith('.liblist'):
					print "O  > ", grpNum, " \tFilePath: ",os.path.join(root, f)
				else:
					if any((jobWithAttr.jobID in f and jobWithAttr.dimension is 'w') for jobWithAttr in normalJobsWithAttr.get(grpNum)) and f.endswith('.liblist'):
						print "Nw > ", grpNum, " \tFilePath: ",os.path.join(root, f)
					if any((jobWithAttr.jobID in f and jobWithAttr.dimension is 'v') for jobWithAttr in normalJobsWithAttr.get(grpNum)) and f.endswith('.liblist'):
						print "Nv > ", grpNum, " \tFilePath: ",os.path.join(root, f)
					if any((jobWithAttr.jobID in f and jobWithAttr.dimension is 'm') for jobWithAttr in normalJobsWithAttr.get(grpNum)) and f.endswith('.liblist'):
						print "Nm > ", grpNum, " \tFilePath: ",os.path.join(root, f)
					if any((jobWithAttr.jobID in f and jobWithAttr.dimension is 'c') for jobWithAttr in normalJobsWithAttr.get(grpNum)) and f.endswith('.liblist'):
						print "Nc > ", grpNum, " \tFilePath: ",os.path.join(root, f)

