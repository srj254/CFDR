#!/usr/bin/python

import sys
import os
import re
import pandas as pd
from collections import defaultdict
from collections import Counter
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import operator

# Select data set corresponds to Library list data
def selectJobs(accFile, joblist):
	df = pd.io.parsers.read_csv(sys.argv[1], sep='\t')
	df = df[df['JobID'].isin(joblist)]
	return df

# Get all Jobs and dictioanry of Libraries vs Jobs
def getLibsForJobs(liblistPath):
	lib2Jobs = defaultdict(list)	
	joblist  = []

	for f in os.listdir(liblistPath):
		try:
			j = int(f.split('.')[0].split('_')[-1])
		except:
			continue

		with open(liblistPath+'/'+f) as libf:
			for line in libf:
				line = line.strip()
				try:	
		                        line = (line.rsplit('/', 1)[1]).split('.so')[0]+ '.so'
		                        if (line == ""):
                       			        continue
					lib2Jobs[line].append(int(j))
					joblist.append(j)
				except:
					continue
	return lib2Jobs, joblist

def jobsWithErrorCode(df, errCodes):
	df1 = df[df['Exit_status'].isin(errCodes)]
	jobs = df1['JobID'].tolist()
        return jobs
	
def jobsWithoutErrCode(df, errCodes):
	print "Total Jobs", len(df['JobID'].tolist())
	df1 = df[df['Exit_status'].isin(errCodes) == False]
	jobs = df1['JobID'].tolist()
        return jobs

if __name__ == "__main__":
	if len(sys.argv) != 4:
		print "Usage: ./script.sh AccFile liblistPath defaultLibs"
		exit()
	histList = []
	errCodes = [265, 271, 143]
	succCodes = [0]
	
	libDict, jlist = getLibsForJobs(sys.argv[2])
	df = selectJobs(sys.argv[1], list(set(jlist)))
	print "Total Jobs", len(df['JobID'].tolist())
	print "Jobs:", len(set(jlist))

	errJobs = jobsWithErrorCode(df, errCodes)
	print "Error:", len(errJobs)

	#succJobs= jobsWithErrorCode(df, succCodes)
	succJobs = jobsWithoutErrCode(df, errCodes)
	print "Success", len(succJobs)
	print "Libraries: ", len(libDict.keys())

	count = 0
	probLib = defaultdict(float)
	libWithErrJobs = defaultdict(float)
	libUsedWithSuccJobs = defaultdict(int)	
	for lib in libDict.keys():
		#print "Error and Library", set(errJobs)  & set(libDict[lib])
		#print "Success and Library", set(succJobs) & set(libDict[lib])
		#print "All libs", set(libDict[lib])
		#raw_input()

		pL_and_err = len(set(errJobs)  & set(libDict[lib]))

		if pL_and_err < 3:
			count += 1
			continue

		pL_and_suc = len(set(succJobs) & set(libDict[lib]))
		libUsedWithSuccJobs[lib] = pL_and_suc

		perr	   = len(set(errJobs))
		psucc	   = len(set(succJobs))
		pLgivenErr = float(pL_and_err/float(perr))
		pLgivenSuc = float(pL_and_suc/float(psucc))

		#print "------------------------------------"
		#print "Library Name:", lib
		#print "P(L|Err)=", pLgivenErr
		#print "P(L|Success)=", pLgivenSuc
		try:
			result = float(float(pLgivenErr) / float(pLgivenErr + pLgivenSuc))
			#result = float(float(pL_and_err) / float(pLgivenErr + pLgivenSuc))
			
			probLib[lib] = result
			#print result
			libWithErrJobs[lib] = float(pL_and_err) * result
		except:
			print Exception
			exit()

		#print "------------------------------------"

	#libProbTuple = sorted(probLib.items(), key=operator.itemgetter(1), reverse=True)
	libFreqTuple = sorted(libWithErrJobs.items(), key=operator.itemgetter(1), reverse=True)
	succJobLibFreq = zip(*sorted(libUsedWithSuccJobs.items(), key=operator.itemgetter(1), reverse=True))
	#print succJobLibFreq[0]	
	#raw_input()
	#print succJobLibFreq[1]	
	#raw_input()

	X = []
	Y = []
	#print len(probLib.keys())
	syslibs = []
	with open(sys.argv[3]) as lf:
		for line in lf:
			syslibs.append(line.strip())

	for l in libFreqTuple:
		if l[0] in succJobLibFreq[0][:100]:
			#print "Top100:",'\t', l[0],'\t', l[1],'\t', probLib[l[0]],'\t', len(set(errJobs) & set(libDict[l[0]]))
			continue
		if l[0] in syslibs:
			#print "SysLibs:", '\t', l[0],'\t', l[1],'\t', probLib[l[0]],'\t', len(set(errJobs) & set(libDict[l[0]]))
			continue
		if probLib[l[0]] < 0.8:
			continue

		X.append(l[0])
		Y.append(libWithErrJobs[l[0]])
		print l[0],'\t', l[1],'\t', probLib[l[0]],'\t', len(set(errJobs) & set(libDict[l[0]]))
		#Y.append(l[1])
		#print l[0], l[1]
	plt.plot(Y)
	#print libProbTuple[0], libProbTuple[200], libProbTuple[400], libProbTuple[600], libProbTuple[800], libProbTuple[1000]
	#plt.xticks(np.arange(10), rotation='vertical')
	plt.savefig('libBugyLvl.png', format="png")

	'''
	c95 =0
	c98 =0
	c99 =0
	c01 =0
	for i in histList:
		if i == 1:
			c95 += 1
			c98 += 1
			c99 += 1
			c01 += 1
		elif i >= 0.99:
			c95 += 1
			c98 += 1
			c99 += 1
		elif i >= 0.98:
			c98 += 1
			c95 += 1
		elif i >= 0.90:
			c95 += 1
		else:
			continue

	n, bins, patches = plt.hist(histList)
	print bins, n
	plt.savefig("BugHist.png", format="png")
	'''		
