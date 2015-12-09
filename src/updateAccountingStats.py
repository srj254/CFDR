#!/usr/bin/python

import re
import sys
import os
import pandas as pd
import numpy  as np
import scipy  as sp
from   collections import defaultdict
import liblistAnalysis as libListAnalyser

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "Usage: ./<Script.sh> <AccountingStatsFile> <liblistTable>"
		exit()

#	jobDict = {}
#	jobGroups = {}
#	jobGroups  = libListAnalyser.groupJobs(sys.argv[2], 'conte', 0, "")
#	for key in jobGroups.keys():
#		for job in jobGroups.get(key):
#			jobDict[job] = key
	'''
	with open(sys.argv[2]) as f:
		for line in f:
			(key, val) = line.split()
			jobDict[key] = val

	df = pd.io.parsers.read_csv(sys.argv[1], sep='\t')
	df.set_index('JobID')
	jobIDs = df['JobID']
	grpIDs = ['-1']*len(df[df.columns.values.tolist()[0]])
	df['JobGrp'] = pd.Series(grpIDs)
	
	df['OriginalUser'] = df['user']
	user2Anon = defaultdict()
	count = 1
	for user in list(set(df['user'].values.tolist())):
		user2Anon[user] = "User"+str(count)
		count +=1

	for index, row in df.iterrows():
		df.ix[index, 'user'] = user2Anon[df.ix[index, 'user']]

		if df.ix[index, 'PeakPgFlt'] > 500:
			df.ix[index, 'Thrashing'] = True
		else:
			df.ix[index, 'Thrashing'] = False

		val = jobDict.get(str(row['JobID']))
		if val is None:
			df.ix[index, 'JobGrp'] = "-NA-"
		else:
			df.ix[index, 'JobGrp'] = str(val)
	'''

	df = pd.io.parsers.read_csv(sys.argv[1], sep='\t')
	df['OrigJobname'] = df['jobname']
	df['OrigAccount'] = df['account']
	df['OrigGroup']   = df['group']
	df['OrigQueue']   = df['queue']

	job2Anon = defaultdict()
	acc2Anon = defaultdict()
	grp2Anon = defaultdict()
	q2Anon   = defaultdict()

	count = 1
	for jname in list(set(df['jobname'].values.tolist())):
		job2Anon[jname] = "JobName"+str(count)
		count +=1
	count = 1
	for accname in list(set(df['account'].values.tolist())):
		acc2Anon[accname] = "Acc"+str(count)
		count +=1
	count = 1
	for grpname in list(set(df['group'].values.tolist())):
		grp2Anon[grpname] = "Group"+str(count)
		count +=1
	count = 1
	for qname in list(set(df['queue'].values.tolist())):
		if qname == "standby":
			q2Anon[qname] = qname
		else:
			q2Anon[qname] = "queue"+str(count)
		count +=1

	for index, row in df.iterrows():
		df.ix[index, 'jobname'] = job2Anon[df.ix[index, 'jobname']]
		df.ix[index, 'account'] = acc2Anon[df.ix[index, 'account']]
		df.ix[index, 'queue']   = q2Anon[df.ix[index, 'queue']]
		df.ix[index, 'group']   = grp2Anon[df.ix[index, 'group']]
		print index

	df['OrigJobname'] = None
	df['OrigAccount'] = None
	df['OrigGroup']   = None
	df['OrigQueue']   = None
	df['OriginalUser']= None

	df.to_csv(sys.argv[1], sep='\t')
