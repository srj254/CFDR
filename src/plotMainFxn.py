#!/usr/bin/python

import numpy as np
import pylab as plt
import os
import sys
import pandas as pd
import matplotlib
from   mpl_toolkits.mplot3d import Axes3D
from   matplotlib.axes import Axes
import matplotlib.pyplot as mplt
import csv
import sys
import os
import operator
from   collections import defaultdict

# custom imports
import users as usersOnX
import appGroup as appGrpOnX
import jobDensity as jdensityOnX
import totalCores as coreCntOnX
import appGroupTrends

'''
['Unnamed: 0', 'AvgPgFltJumps', 'Error_Path', 'Exit_status', 'JobID', 'JobStatus', 'LogTS', 'LoggerHostName', 'MajPgFlt', 'Output_Path', 'PeakPgFlt', 'Resource_List.gres', 'Resource_List.mem', 'Resource_List.naccesspolicy', 'Resource_List.ncpus', 'Resource_List.neednodes', 'Resource_List.nodect', 'Resource_List.nodes', 'Resource_List.pmem', 'Resource_List.walltime', 'account', 'ctime', 'end', 'etime', 'exec_host', 'group', 'jobDensity', 'jobname', 'majPgFltRate', 'owner', 'qtime', 'queue', 'resources_used.cput', 'resources_used.mem', 'resources_used.vmem', 'resources_used.walltime', 'session', 'start', 'totalCores', 'uniqHosts', 'user', 'JobGrp']
'''

patterns	= [ '', '', '','/','\\','o','.','' ]
colors		= ['b','r','g','b','r' ,'g','k','w']
outlinewgt	= [ 1 , 1 , 1 , 1 , 1  , 1 , 1 , 2 ]

bar_width	= 0.1
barSpacing	= 0.05

xlabelFontSZ	= 16
ylabelFontSZ	= 16
labelFontSZ	= 16

xticksFontSZ	= 14
yticksFontSZ	= 14
ticksFontSZ	= 14

ylabelFontWT	= 'bold'
xlabelFontWT	= 'bold'
labelFontWT	= 'bold'

ImgFormat	= 'png'
ImgDPI		= 1000
ImgWidth	= 18.5
ImgHeight	= 10.5
ImgProp		= 'tight'

def jobsPerDay(df):
	startTimes = df['start'].values.tolist()
	startTimes = [int(item) for item in startTimes]
	startTimes = sorted(startTimes)
	jobs       = [0] * ((startTimes[-1]+1) - startTimes[0])
	startTS    = np.arange(startTimes[0], (startTimes[-1]+1))

	for starts in list(set(startTimes)):
		try:
			jobs[starts-startTimes[0]]   += 1
		except:
			print (starts-startTimes[0])
			print (startTimes[-1] - startTimes[0])
			print len(jobs)
			raw_input()
			
	print len(jobs), len(startTS)	
#	noOfBars = 100
	filename = "startTimeVsNJobs.png"
	fig, ax = mplt.subplots()
#	indices = np.arange(0, noOfBars*0.3, 0.3)

	mplt.plot(startTimes, jobs)
#	ax.set_xticks(indices+ 0.5*bar_width)
	mplt.xticks(fontsize=ticksFontSZ)
	mplt.yticks(fontsize=ticksFontSZ)
	ax.set_ylabel("No of jobs", fontweight=labelFontWT, fontsize=ticksFontSZ)
	ax.set_xlabel("Time line", fontweight=labelFontWT, fontsize=ticksFontSZ)
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)

	return 	

def jobsPerHourInADay():
	pass

if len(sys.argv) != 3:
	print "Usage: ./Script.sh <Accounting file> <Path to save Plots>"
	exit()

df = pd.io.parsers.read_csv(sys.argv[1], sep = '\t')
df = pd.DataFrame.sort (df, columns = 'JobID')

#usersOnX.usersVsJobs(df)
#appGrpOnX.grpVsJobs(df)
#coreCntOnX.coresVsJobs(df)
#jdensityOnX.jobDensityVsJobs(df)
appGroupTrends.appGroupTrends(df)
#jobsPerDay(df)
