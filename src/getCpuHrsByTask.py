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

def cnvtTime(timeString):
        time = timeString.split(':')
        result = int(time[0])*3600 + int(time[1])*60 + int(time[0])
        return result

def getCpuHrsByTasks(df):
	walltimelist = df['resources_used.walltime'].tolist()
	totalCores   = df['uniqHosts'].tolist()
	
	task2Hrs = defaultdict(float)
	count = 0
	hrsByTask = zip(walltimelist, totalCores)
	for w, t in hrsByTask:
		try:
			task2Hrs[t] = task2Hrs[t] + float(float(cnvtTime(w))/3600.00)
		except:
			count += 1
			continue
	return task2Hrs

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print "Provide AccountingLogs"
		exit()
	df = pd.io.parsers.read_csv(sys.argv[1], sep='\t')
	task2Hrs = getCpuHrsByTasks(df)
	for t in task2Hrs.keys():
		print t, ',', task2Hrs[t]
