#!/usr/bin/python
import time
from   datetime import date
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
import uniqHosts as uniqHostsOnX
import appGroupTrendsPerSec
'''
['Unnamed: 0', 'AvgPgFltJumps', 'Error_Path', 'Exit_status', 'JobID', 'JobStatus', 'LogTS', 'LoggerHostName', 'MajPgFlt', 'Output_Path', 'PeakPgFlt', 'Resource_List.gres', 'Resource_List.mem', 'Resource_List.naccesspolicy', 'Resource_List.ncpus', 'Resource_List.neednodes', 'Resource_List.nodect', 'Resource_List.nodes', 'Resource_List.pmem', 'Resource_List.walltime', 'account', 'ctime', 'end', 'etime', 'exec_host', 'group', 'jobDensity', 'jobname', 'majPgFltRate', 'owner', 'qtime', 'queue', 'resources_used.cput', 'resources_used.mem', 'resources_used.vmem', 'resources_used.walltime', 'session', 'start', 'totalCores', 'uniqHosts', 'user', 'JobGrp']
'''
'''
patterns	= [ '', '', '','/','\\','o','.','' ]
colors		= ['b','r','g','b','r' ,'g','k','w']
outlinewgt	= [ 1 , 1 , 1 , 1 , 1  , 1 , 1 , 2 ]

bar_width	= 0.1
barSpacing	= 0.05

xlabelFontSZ	= 20
ylabelFontSZ	= 20
labelFontSZ	= 20
legendFontSZ	= 15

xticksFontSZ	= 16
yticksFontSZ	= 16
ticksFontSZ	= 16

ylabelFontWT	= 'normal'
xlabelFontWT	= 'normal'
labelFontWT	= 'normal'

ImgFormat	= 'png'
ImgDPI		= 700
ImgWidth	= 15
ImgHeight	= 8
ImgProp		= 'tight'
'''
'''
def labelBar(axis, bar, text, factor):
	ht = bar.get_height()
	axis.text(bar.get_x()+bar.get_width()/2., (1.03+factor)*ht, ' '+text,
                ha='center', va='bottom' )
	return
'''
def jobsPerDay(df):
	a = df['start'].values.tolist()
	a = [str(date.fromtimestamp(item)) for item in a]
        counts1, bin_edges1 = np.histogram(a, bins=10000)
        ssum1 = float(counts1.sum())
        counts1 = counts1/ssum1
        cdf1 = np.cumsum(counts1)

	plt.plot(bin_edges1[1:], cdf1, linewidth=outlinewgt[-1])
	#plt.xlim(0, 1000)
	plt.xticks(fontsize=ticksFontSZ)
	plt.xlabel("Major page faults/10 mins", fontweight=labelFontWT, fontsize=labelFontSZ)
	plt.ylabel("CDF (zoomed in from 0-1000)", fontweight=labelFontWT, fontsize=labelFontSZ)
	filename = "JobsTrend"
	plt.savefig(sys.argv[2] + "/"+filename + ".png")

	'''
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
	'''

	return 	

def jobsPerHourInADay():
	pass

if len(sys.argv) != 3:
	print "Usage: ./Script.sh <Accounting file> <Path to save Plots>"
	exit()

df = pd.io.parsers.read_csv(sys.argv[1], sep = '\t')
df = pd.DataFrame.sort (df, columns = 'JobID')

#jobsPerDay(df)

usersOnX.usersVsJobs(df)
'''
appGrpOnX.grpVsJobs(df)
appGrpOnX.grpVsUniqUsers(df)
appGrpOnX.grpVsNJobs(df)
coreCntOnX.coresVsJobs(df)
jdensityOnX.jobDensityVsJobs(df)
uniqHostsOnX.uniqHostsVsJobs(df)
'''
#appGroupTrends.appGroupTrends(df)
#appGroupTrendsPerSec.appGroupTrends(df)

#jobsPerDay(df)
