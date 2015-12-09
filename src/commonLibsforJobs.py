#!/usr/bin/python

import sys
import os
import re
import pandas as pd
from collections import defaultdict
from collections import Counter

def selectJobs(accFile, exitcodes):
	df = pd.io.parsers.read_csv(sys.argv[1], sep='\t')
	df = df[df['Exit_status'].isin(exitcodes)]
	joblist = df['JobID'].tolist()
	return joblist
 
def getLibsForJobs(joblist, liblistPath):
	job2Libs = defaultdict(list)	
	count = 0
	commonLibs = []
	for f in os.listdir(liblistPath):
		print count
		count = count + 1
		try:
			j = int(f.split('.')[0].split('_')[-1])
		except:
			continue

		if j not in joblist:
			continue

		job2Libs[int(j)] = []

		with open(liblistPath+'/'+f) as libf:
			for line in libf:
				line = line.strip()
				try:	
		                        line = (line.rsplit('/', 1)[1]).split('.so')[0]+ '.so'
		                        if (line == ""):
                       			        continue
					job2Libs[int(j)].append(line)
				except:
					continue
		commonLibs.extend(job2Libs[int(j)])
	return job2Libs, commonLibs

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "Usage: ./script.sh AccFile liblistPath"
		exit()

# Get Lib vs Job list 
# Get Joblist for error codes

ExitCodes = [0]
joblist = selectJobs(sys.argv[1], ExitCodes)
print len(joblist), '\n\n\n\n'
job2libs, commonLibs= getLibsForJobs(joblist, sys.argv[2])

c = Counter(commonLibs)
for i in c.most_common(100):
	print i


#for job in job2libs.keys():
#	print job, job2libs[job]
