#!/usr/bin/python 
import sys
import os
import time
import pandas as pd
import datetime
import time
import string 
from itertools import islice

def cnvtTime(timeStr):
	dt = datetime.datetime.strptime(timeStr, "%b %d %H:%M:%S %Y")
	epochSec = time.mktime(dt.timetuple()) - (3600*5)
	return int(epochSec)
	
def getJobAt(df, timeStamp, nodeName, outfile):
	df1 = df[df['start'] < timeStamp]
	df1 = df1[df1['end'] > timeStamp]
	df1 = df1[df1['exec_host'].str.contains(nodeName) == True]
	return df1['JobID'].tolist()

if __name__ == "__main__":
	if len(sys.argv) != 5:
		print "Usage ./Script.sh SyslogFile AccountingStats OutputFile message"
		exit()

	df = pd.io.parsers.read_csv(sys.argv[2], sep='\t')
	df = df[['start', 'end', 'JobID', 'exec_host']]
	df = df[df['end'] < 1419897600]

	of = open(sys.argv[3], 'w')

	outbuffer = []
	with open(sys.argv[1]) as f:
		#alllines = f.readlines()
		#i = 0
		#for line in f:
		#	i += 1
		#	if i%10000 == 0:
		#		print i
			#if 'hansen' in line.lower():
			#	continue
			#cond = ['out of memory' in line.lower(), \
			#	 'oom-killer' in line.lower(), \
			#	 'lustreerror' in line.lower(), 'error' in line.lower()]
			#messages = ['out of memory', 'oom-killer', 'Lustre error', 'other error']
			#if any(cond):
    		while True:
			#print time.time()
		        next10k = list(islice(f, 100000))  # need list to do len, 3 lines down
		        for line in next10k:
		        #process(ln)
			#if True:
				#print "1", time.time()
				epochSec = cnvtTime(line[:15] + " 2014")
				#print "1", time.time()
				#raw_input()
				if line[16:21] == "conte" and line[23:26].isdigit():
					#print "2", time.time()
					jlist = getJobAt(df, epochSec, line[16:26], None)
					#print "2", time.time()
					#raw_input()
					if len(jlist) != 0:
						jlistStr = '['+','.join(str(e) for e in jlist)+']'
						outLine = '\t'.join([jlistStr, line[26:]])
						outbuffer.append(outLine)
		        if len(next10k) < 100000:
		        	break
			
			if len(outbuffer) > 1000:
				for l in outbuffer:
					print >> of, l
				outbuffer = []
			print "Slice Done"
			#print time.time()
		for l in outbuffer:
			print >> of, l
		outbuffer = []
	of.close()
