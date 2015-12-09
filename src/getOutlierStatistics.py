#!/usr/bin/python

import os
import sys
import re
import math
import pandas as pd
import numpy as np
import scipy as sp
from   collections import defaultdict

def getOutlierStats(path, df):
	outlierDict = defaultdict(list)
	outlierDict['c'] = []
	outlierDict['w'] = []
	outlierDict['v'] = []
	outlierDict['m'] = []

	for filename in os.listdir(path):
		if 'N' in filename:
			continue
	 	with open(path+'/'+filename) as f:
			for line in f:
				outlierDict[filename[-1]].append(int(line.split()[0]))

	outlierDict['c'] = list(set(outlierDict['c']))
	outlierDict['w'] = list(set(outlierDict['w']))
	outlierDict['v'] = list(set(outlierDict['v']))
	outlierDict['m'] = list(set(outlierDict['m']))
	
	C = set(outlierDict['c'])
	W = set(outlierDict['w'])
	V = set(outlierDict['v'])
	M = set(outlierDict['m'])

	cwmv= set(outlierDict['c']) & set(outlierDict['w']) & set(outlierDict['m']) & set(outlierDict['v'])

	cwm = set(outlierDict['c']) & set(outlierDict['w']) & set(outlierDict['m'])
	cwv = set(outlierDict['c']) & set(outlierDict['w']) & set(outlierDict['v'])
	cmv = set(outlierDict['c']) & set(outlierDict['m']) & set(outlierDict['v'])
	wmv = set(outlierDict['w']) & set(outlierDict['m']) & set(outlierDict['v'])

	cw = set(outlierDict['c']) & set(outlierDict['w'])# & set(outlierDict['m']) & set(outlierDict['v'])
	cm = set(outlierDict['c']) & set(outlierDict['m'])# & set(outlierDict['m'])
	cv = set(outlierDict['c']) & set(outlierDict['v'])# & set(outlierDict['v'])
	mv = set(outlierDict['m']) & set(outlierDict['v'])# & set(outlierDict['v'])
	mw = set(outlierDict['m']) & set(outlierDict['w'])# & set(outlierDict['v'])
	vw = set(outlierDict['w']) & set(outlierDict['v'])# & set(outlierDict['v'])

	onlyCWMV = cwmv
	print "CWMV", len(list(onlyCWMV))

	onlyW = W-(M|V|C)
	print "W", len(list(onlyW))
	onlyM = M-(W|V|C)
	print "M", len(list(onlyM))
	onlyC = C-(M|W|V)
	print "C", len(list(onlyC))
	onlyV = V-(W|M|C)
	print "V", len(list(onlyV))
	
	onlyWM = W&M-(V|C)
	print "WM", len(list(onlyWM))
	onlyMV = M&V-(W|C)
	print "MV", len(list(onlyMV))
	onlyCV = V&C-(M|W)
	print "CV", len(list(onlyCV))
	onlyCW = C&W-(M|V)
	print "CW", len(list(onlyCW))
	onlyCM = C&M-(V|W)
	print "CM", len(list(onlyCM))
	onlyVW = V&W-(M|C)
	print "WV", len(list(onlyVW))
	
	onlyWMV = V&W&M-(C)
	print "WMV", len(list(onlyWMV))
	onlyMVC = M&V&C-(W)
	print "CMV", len(list(onlyMVC))
	onlyCVW = V&C&W-(M)
	print "CWV", len(list(onlyCVW))
	onlyCWM = C&W&M-(V)
	print "CWM", len(list(onlyCWM))
	
	print 'cwmv' , len(list(cwmv)) 
	print 'cwm'  , len(list(cwm)) 
	print 'cwv'  , len(list(cwv)) 
	print 'cmv'  , len(list(cmv)) 
	print 'wmv' , len(list(wmv)) 
	print "STARTS"
	print 'cw' , float(len(list(cw)))/len(list(set(C) | set(W)))
	print 'cm' , float(len(list(cm)))/len(list(set(C) | set(M))) 
	print 'cv' , float(len(list(cv)))/len(list(set(C) | set(V)))
	print 'mv' , float(len(list(mv)))/len(list(set(M) | set(V))) 
	print 'mw' , float(len(list(mw)))/len(list(set(M) | set(W))) 
	print 'vw' , float(len(list(vw)))/len(list(set(V) | set(W)))
	print "\n\n\n"
	print 'c' , len(outlierDict['c'])
	print 'w' , len(outlierDict['w'])
	print 'v' , len(outlierDict['v'])
	print 'm' , len(outlierDict['m'])

	mdf = pd.io.parsers.read_csv(sys.argv[2], sep='\t')
	mdf = mdf[mdf['JobID'].isin(outlierDict['w'])]
	#print mdf['totalCores'].values.tolist()
	a = mdf['totalCores'].values.tolist()
	for c in list(set(a)):
		print c, a.count(c)
	return
	#return len(list(C|M|W|V))


if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "Usage: ./script.sh <path to outliers> <Accounting Table>"
		exit()

df = pd.io.parsers.read_csv(sys.argv[2], sep='\t')

v = (len(df['JobID'].values.tolist()) - getOutlierStats(sys.argv[1], df))
print v

