#!/usr/bin/python


import re
import sys
import os
import pandas as pd
import numpy as np
import scipy as sp
import liblistAnalysis as libListAnalyser

if __name__ == "__main__":
	if len(sys.argv) != 4:
		print "Usage: ./<Script.sh> <AccountingStatsFile> <LiblistPath> <PathToWrite>"
		exit()

	jobDict = {}
	jobGroups = {}
	jobGroups  = libListAnalyser.groupJobs(sys.argv[2], 'conte', 0, "")
	for key in jobGroups.keys():
		for job in jobGroups.get(key):
			jobDict[job] = key
	
	df = pd.io.parsers.read_csv(sys.argv[1], sep='\t')
	jobIDs = df['JobID']
	grpIDs = ['-1']*len(df[df.columns.values.tolist()[0]])
	df['JobGrp'] = pd.Series(grpIDs)
	
	for index, row in df.iterrows():
		val = jobDict.get(str(row['JobID']))
		if val is None:
			df.ix[index, 'JobGrp'] = "-NA-"
		else:
			df.ix[index, 'JobGrp'] = str(val)
	
	df.to_csv(sys.argv[3]+"/AccountingStats_WithJGrp.tsv", sep='\t')

