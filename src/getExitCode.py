#!/usr/bin/python 
import sys
import os
import time
import pandas as pd
import datetime
import time
import string 
from collections import defaultdict
from collections import Counter

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "Usage ./Script.sh parsedFile AccountingStats"
		exit()

	df = pd.io.parsers.read_csv(sys.argv[2], sep='\t')
	df = df[['start', 'end', 'JobID', 'Exit_status']]
	end = 1417900000
        #df = df[df['Exit_status'].isin([127,-1,255])]

        df = df[df['end'] < end]
	totalJobs = (df['JobID'].tolist())
	print len(totalJobs)
	totalEcode= (df['Exit_status'].tolist())

	totalJ2E_dict = dict(zip(totalJobs, totalEcode))
	totalCtr = dict(Counter(totalEcode))
	print dict(totalCtr)
	
	#tempdf = df[df['Exit_status'] == 127]
	#templist = tempdf['JobID'].tolist()[0]
	#print templist

	msgDict = defaultdict(str)
	#files  = os.listdir(sys.argv[1])
	files = [sys.argv[1]]
	for fname in files:
		with open(fname) as f:
			allJobs = set([])
			for line in f.readlines():
				parts = line.strip().split('\t')
				piece = parts[0][1:-1]
				try:
					jobID = [int(i) for i in piece.split(',')]
					
					#if len(jobID) > 1:
					#	print jobID

					#for j in jobID:
					#	if j in templist:
					#		print parts[1]
					for j in jobID:
						msgDict[j] = parts[1]
						#print parts[1]
				except:
					continue
				allJobs.update(jobID)
			set(allJobs)

	#print len(allJobs)
	#raw_input()
	#print 'AllJobs', len(set(allJobs))
	start 	= []
	end 	= []
	
	j2Ecode = defaultdict(int)
	for j in set(allJobs):
		sub_df = df[df['JobID'] == j]
		ecode = sub_df['Exit_status'].tolist()[0]
		#start.append(sub_df['start'].tolist()[0])
		#end.append(sub_df['end'].tolist()[0])
		j2Ecode[j] = ecode
		#if ecode == -1:
		#	print j, ecode #, msgDict[j]

	syslogEcodeCtr = dict(Counter(j2Ecode.values()))

	#print max(end)
	#print min(start)
	#raw_input()

	den = sum(syslogEcodeCtr.values())
	#print syslogEcodeCtr
	print den
	
	count = 0
	#for i in syslogEcodeCtr.keys():
	for i in [127, 255]:
		n = syslogEcodeCtr.get(i)
		count += float(n)*100.00/den
		print i, '\t', float(n)*100.00/den
		print i, '\t', float(n)*100.00/totalCtr.get(i)

	#print count
		
			
	'''	
	of = open(sys.argv[3], 'a')

	outbuffer = []
	with open(sys.argv[1]) as f:
		alllines = f.readlines()
		for i, line in enumerate(alllines):
			if i%10000 == 0:
				print i
			if 'hansen' in line.lower():
				continue
			#cond = ['out of memory' in line.lower(), 'oom-killer' in line.lower(), 'lustreerror' in line.lower(), 'error' in line.lower()]
			#messages = ['out of memory', 'oom-killer', 'Lustre error', 'other error']
			#if any(cond):
			if True:
				epochSec = cnvtTime(line[:15] + " 2014")
				if line[16:21] == "conte" and line[23:26].isdigit():
					jlist = getJobAt(df, epochSec, line[16:26], None)
					if len(jlist) != 0:
						jlistStr = '['+','.join(str(e) for e in jlist)+']'
						outLine = '\t'.join([jlistStr, str(i), sys.argv[4]])
						outbuffer.append(outLine)
			
			if len(outbuffer) > 1000:
				for l in outbuffer:
					print >> of, l
				outbuffer = []
		for l in outbuffer:
			print >> of, l
		outbuffer = []
	of.close()
	'''
