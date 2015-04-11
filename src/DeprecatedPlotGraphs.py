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

# Percentage of Jobs requesting certain number of Cores
def coresVsJobs(df):
	totalCores = (df['totalCores'].values.tolist())
	
	roi_df = df[['totalCores', 'Thrashing']]
	roi_df = roi_df[(roi_df['Thrashing'] == True)]
	thrashingCores = roi_df['totalCores'].values.tolist()

	thrashingCoresPcnt = defaultdict(float)
	for coreNo in list(set(thrashingCores)):
		percent = (float(thrashingCores.count(coreNo))/float(len(totalCores)))*100
		thrashingCoresPcnt[coreNo] = percent

	core2Jobs = defaultdict(int)
	
	for coreNo in list(set(totalCores)):
		core2Jobs[coreNo] = (float(totalCores.count(coreNo))*100/float(len(totalCores)))
	cores = core2Jobs.keys()
	jobs  = core2Jobs.values()
	ziplist = zip(cores, jobs)
	ziplist = sorted(ziplist, key=lambda x: x[1], reverse=True)
	cores, jobs = zip(*ziplist)
	pcntThrashJobs = [((core2Jobs[coreNo]*thrashingCoresPcnt[coreNo])/100.00) for coreNo in cores]
	jobs = map(operator.sub, jobs, pcntThrashJobs)
	# Plotting related data
	noOfBars = 10
	filename = "CoresVSPercentageOfJobs.png"
	fig, ax = mplt.subplots()
	indices = np.arange(0, 0.3*noOfBars, 0.3)
	bar1    = ax.bar(indices, pcntThrashJobs[:noOfBars], bar_width, color='b', linewidth=outlinewgt[-1])
	bar2    = ax.bar(indices, jobs[:noOfBars], bar_width, bottom=pcntThrashJobs[:noOfBars], color='w', linewidth=outlinewgt[-1], hatch="o")
	bar1[0].set_color('r')


	ax.set_xticks(indices + 0.5*(bar_width))
	ax.set_xticklabels(cores[:noOfBars])
	ax.set_xlabel('No of cores', fontsize=labelFontSZ, fontweight=labelFontWT)
	ax.set_ylabel('% of jobs', fontsize=labelFontSZ, fontweight=labelFontWT)

	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')	
	mplt.yticks(fontsize=ticksFontSZ)	
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	mplt.legend( (bar1[0], bar1[1], bar2[0]), ("Highest % Major Page fault", "Major Page Fault > Threshold", "Major Page Fault < Threshold"))
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)

	# Plotting related data
	noOfBars = 10
	filename = "CoresVSPercentageOfFaultyJobsForTopTotalCores.png"
	fig, ax = mplt.subplots()
	indices = np.arange(0, 0.3*noOfBars, 0.3)
	bars    = ax.bar(indices, pcntThrashJobs[:noOfBars], bar_width, color='b', linewidth=outlinewgt[-1])

	ax.set_xticks(indices + 0.5*(bar_width))
	ax.set_xticklabels(cores[:noOfBars])
	ax.set_xlabel('No of cores', fontsize=labelFontSZ, fontweight=labelFontWT)
	ax.set_ylabel('% of jobs > Threshold major page faults', fontsize=labelFontSZ, fontweight=labelFontWT)

	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')	
	mplt.yticks(fontsize=ticksFontSZ)	
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)

	return

def coresVsPageFaults(df):
	roi_df = df[['totalCores', 'Thrashing']]
	roi_df = roi_df[(roi_df['Thrashing'] == True)]

	coreCount = roi_df['totalCores'].values.tolist()
	thrashingCores = coreCount
	
	cores = []
	for core in list(set(coreCount)):
		cores.append((core, coreCount.count(core)))
	
	core, count = zip(*sorted(cores, key=lambda x:x[1], reverse=True))

	noOfBars = 50
	filename = "CoresVsNoOfFaultyJobs.png"
	fig, ax = mplt.subplots()

	indices = np.arange(0, noOfBars*0.3, 0.3)
	ax.set_xticks(indices + 0.5*bar_width)
	ax.set_xticklabels(core[:noOfBars])
	ax.bar(indices, count[:noOfBars], bar_width, color='b')
	ax.set_xlabel('No of cores required',  fontsize=labelFontSZ, fontweight=labelFontWT)
	ax.set_ylabel('No of jobs > Threshold major page fault', fontsize=labelFontSZ, fontweight=labelFontWT)
	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')	
	mplt.yticks(fontsize=ticksFontSZ)	
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)
	

	roi_df = df[['totalCores', 'Thrashing']]
	coreCount  = roi_df['totalCores'].values.tolist()
	
	jobs = []
	for core in list(set(coreCount)):
		percent = (float(thrashingCores.count(core))/float(coreCount.count(core)))*100
		jobs.append((core, percent))
	cores, percent  = zip(*sorted(jobs, key=lambda x:x[1], reverse=True))
	
	noOfBars = 50
	filename = "CoresVsPercentOfFaultyJobs.png"
	fig, ax = mplt.subplots()
	indices = np.arange(0, noOfBars*0.3, 0.3)

	ax.bar(indices, percent[:noOfBars], bar_width, color='b')
	ax.set_xticks(indices+ 0.5*bar_width)
	ax.set_xticklabels(cores[:noOfBars])
	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')
	mplt.yticks(fontsize=ticksFontSZ)
	ax.set_ylabel("% of jobs > Threshold major page fault ", fontweight=labelFontWT, fontsize=ticksFontSZ)
	ax.set_xlabel("No of cores required", fontweight=labelFontWT, fontsize=ticksFontSZ)
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	fig.subplots_adjust(wspace=0)
	mplt.legend()
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)

	return

def usersVsJobs(df):
	userList  = df['user'].values.tolist()
	user2Jobs = []
	for user in list(set(userList)):
		user2Jobs.append((user, (100.00 * float(userList.count(user)))/(float(len(userList)))))

	user2Jobs = sorted(user2Jobs, key=lambda x:x[1], reverse=True)
	users, jobs = zip(*user2Jobs)
	
	noOfBars = 50
	filename = "UsersVsPercentageOfJobs.png"
	fig, ax = mplt.subplots()
	indices = np.arange(0, noOfBars*0.3, 0.3)

	ax.bar(indices, jobs[:noOfBars], bar_width, color='b')
	ax.set_xticks(indices+ 0.5*bar_width)
	ax.set_xticklabels([])
	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')
	mplt.yticks(fontsize=ticksFontSZ)
	ax.set_ylabel("% of jobs", fontweight=labelFontWT, fontsize=ticksFontSZ)
	ax.set_xlabel("Top "+str(noOfBars)+" users", fontweight=labelFontWT, fontsize=ticksFontSZ)		
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)

	return 

def usersVsPgFlt(df):
	roi_df = df[['user', 'Thrashing']]
	roi_df = roi_df[(roi_df['Thrashing'] == True)]
	users  = roi_df['user'].values.tolist()
	
	thrashingUserJobs = users

	jobs = []
	for user in list(set(users)):
		jobs.append((user, users.count(user)))
	jobs = sorted(jobs, key=lambda x: x[1], reverse=True)
	print jobs[:20]
	raw_input()
	users, jobs = zip(*jobs)
	noOfBars = 50
	filename = "UsersVsNoOfFaultyJobs.png"
	fig, ax = mplt.subplots()
	indices = np.arange(0, noOfBars*0.3, 0.3)

	ax.bar(indices, jobs[:noOfBars], bar_width, color='b')
	ax.set_xticks(indices+ 0.5*bar_width)
	ax.set_xticklabels(users[:noOfBars])
	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')
	mplt.yticks(fontsize=ticksFontSZ)
	ax.set_ylabel("No of jobs > Threshold major page fault", fontweight=labelFontWT, fontsize=ticksFontSZ)
	ax.set_xlabel("Top "+str(noOfBars)+" users", fontweight=labelFontWT, fontsize=ticksFontSZ)
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)

	roi_df = df[['user', 'Thrashing']]
	users  = roi_df['user'].values.tolist()
	
	jobs = []
	for user in list(set(users)):
		percent = (float(thrashingUserJobs.count(user))/float(users.count(user)))*100
		jobs.append((user, percent))
	users, percent  = zip(*sorted(jobs, key=lambda x:x[1], reverse=True))
	
	noOfBars = 100
	filename = "UsersVsPercentOfFaultyJobs.png"
	fig, ax = mplt.subplots()
	indices = np.arange(0, noOfBars*0.3, 0.3)

	ax.bar(indices, percent[:noOfBars], bar_width, color='b')
	ax.set_xticks(indices+ 0.5*bar_width)
	ax.set_xticklabels([])
	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')
	mplt.yticks(fontsize=ticksFontSZ)
	ax.set_ylabel("% of jobs > Threshold major page fault", fontweight=labelFontWT, fontsize=ticksFontSZ)
	ax.set_xlabel("Top "+str(noOfBars)+" Users", fontweight=labelFontWT, fontsize=ticksFontSZ)
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)
		
	return 

def grpVsJobs(df):
	grps = df['JobGrp'].values.tolist()
	grps = filter(lambda x: x != "-NA-", grps)

	groups = []
	for grp in list(set(grps)):
		groups.append((grp, float(grps.count(grp))*100/float(len(grps))))
	
	groups, jobs = zip(*sorted(groups, key=lambda x:x[1], reverse=True))

	noOfBars = 50
	filename = "AppGrpsVsPercentageOfJobs.png"
	fig, ax = mplt.subplots()
	indices = np.arange(0, noOfBars*0.3, 0.3)

	ax.bar(indices, jobs[:noOfBars], bar_width, color='b')
	ax.set_xticks(indices+ 0.5*bar_width)
	ax.set_xticklabels(groups[:noOfBars])
#	ax.set_xticklabels([])
	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')
	mplt.yticks(fontsize=ticksFontSZ)
	ax.set_ylabel("% of jobs", fontweight=labelFontWT, fontsize=ticksFontSZ)
	ax.set_xlabel("Top "+str(noOfBars)+" AppGroup", fontweight=labelFontWT, fontsize=ticksFontSZ)
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)

	return

def grpVsPgFlt(df):
	roi_df = df[['JobGrp', 'Thrashing']]
	roi_df = roi_df[(roi_df['Thrashing'] == True)]
	groups = roi_df['JobGrp'].values.tolist()
	groups = filter(lambda x: x != "-NA-", groups)
	
	thrashingGroups = groups

	jobs = []
	for group in list(set(groups)):
		jobs.append((group, groups.count(group)))
	jobs = sorted(jobs, key=lambda x: x[1], reverse=True)
	groups, jobs = zip(*jobs)
	
	noOfBars = 50
	filename = "AppGroupVsNoOfFaultyJobs.png"
	fig, ax = mplt.subplots()
	indices = np.arange(0, noOfBars*0.3, 0.3)

	ax.bar(indices, jobs[:noOfBars], bar_width, color='b')
	ax.set_xticks(indices+ 0.5*bar_width)
	ax.set_xticklabels(groups[:noOfBars])
#	ax.set_xticklabels([])
	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')
	mplt.yticks(fontsize=ticksFontSZ)
	ax.set_ylabel("No of jobs > Threshold major page fault", fontweight=labelFontWT, fontsize=ticksFontSZ)
	ax.set_xlabel("Top "+str(noOfBars)+" AppGroup", fontweight=labelFontWT, fontsize=ticksFontSZ)
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)

	roi_df = df[['JobGrp', 'Thrashing']]
	groups = roi_df['JobGrp'].values.tolist()
	groups = filter(lambda x: x != "-NA-", groups)


	jobs = []
	for group in list(set(groups)):
		percent = (float(thrashingGroups.count(group))/float(groups.count(group)))*100
		jobs.append((group, percent))
	groups, percent  = zip(*sorted(jobs, key=lambda x:x[1], reverse=True))
	
	
	noOfBars = 10
	b_width  = bar_width
	filename = "AppGroupVsPercentOfFaultyJobs.png"
	fig, ax = mplt.subplots()
	indices = np.arange(0, noOfBars*0.3, 0.3)

	ax.bar(indices, percent[:noOfBars], b_width, color='b')
	ax.set_xticks(indices+ 0.5*b_width)
	ax.set_xticklabels(groups[:noOfBars])
	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')
	mplt.yticks(fontsize=ticksFontSZ)
	ax.set_ylabel("% of jobs > Threshold major page fault", fontweight=labelFontWT, fontsize=ticksFontSZ)
	ax.set_xlabel("Top "+str(noOfBars)+" groups", fontweight=labelFontWT, fontsize=ticksFontSZ)
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)
		
	return 

def grpVsUniqUsers(df):
	roi_df = df[(df['JobGrp'] != "-NA-")]
	groups = list(set(roi_df['JobGrp'].values.tolist()))
	grp2UniqUsers  = []

	for group in groups:
		mydf = roi_df[roi_df['JobGrp'] == group]
		noOfUniqUsers = len(list(set(mydf['user'].values.tolist())))
		grp2UniqUsers.append((group, noOfUniqUsers))
	
	groups, noOfUniqUsers = zip(*sorted(grp2UniqUsers, key=lambda x:x[1], reverse=True))
	
	noOfBars = 100
	filename = "AppGroupVsUniqUsers.png"
	fig, ax = mplt.subplots()
	indices = np.arange(0, noOfBars*0.3, 0.3)

	ax.bar(indices,noOfUniqUsers[:noOfBars], bar_width, color='b')
	ax.set_xticks(indices+ 0.5*bar_width)
	ax.set_xticklabels([])
	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')
	mplt.yticks(fontsize=ticksFontSZ)
	ax.set_ylabel("No of unique users", fontweight=labelFontWT, fontsize=ticksFontSZ)
	ax.set_xlabel("Top "+str(noOfBars)+" groups", fontweight=labelFontWT, fontsize=ticksFontSZ)
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)

	return 	

def grpVsNJobs(df):
	jobGrp = df['JobGrp'].values.tolist()
	jobGrp = filter(lambda x: x != '-NA-', jobGrp)

	jobGrpVsJobs = []
	for jobGrpNum in list(set(jobGrp)):
		jobGrpVsJobs.append((jobGrpNum, jobGrp.count(jobGrpNum)))
	jobGrps, nJobs = zip(*sorted(jobGrpVsJobs, key=lambda x: x[1], reverse=True))
	
	noOfBars = 100
	filename = "AppGroupVsNJobs.png"
	fig, ax = mplt.subplots()
	indices = np.arange(0, noOfBars*0.3, 0.3)

	ax.bar(indices, nJobs[:noOfBars], bar_width, color='b')
	ax.set_xticks(indices+ 0.5*bar_width)
	ax.set_xticklabels([])
	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')
	mplt.yticks(fontsize=ticksFontSZ)
	ax.set_ylabel("No of jobs", fontweight=labelFontWT, fontsize=ticksFontSZ)
	ax.set_xlabel("Top "+str(noOfBars)+" groups", fontweight=labelFontWT, fontsize=ticksFontSZ)
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)

	return 	


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

def jobDensityVsMajPageFlt(df):
	roi_df = df[['jobDensity', 'PeakPgFlt']]
	
	jobDensity = roi_df['jobDensity'].values.tolist()
	PMajPgFlt   = roi_df['PeakPgFlt'].values.tolist()
	
	jobDensity = [(float(item)/100) for item in jobDensity]
	noOfBars = 100
	fig, ax = mplt.subplots()
	filename = "JobDensityVsPeakMajorPageFaults.png"
	
#	indices = np.arange(0, noOfBars*0.3, 0.3)
#	ax.set_xticks(indices+ 0.5*bar_width)
#	ax.set_xticklabels(jobDensity[:noOfBars])

        ax.set_ylabel("Value of peak Major page faults (in 10 mins)", fontweight=labelFontWT, fontsize=ticksFontSZ)
        ax.set_xlabel("Job Density", fontweight=labelFontWT, fontsize=ticksFontSZ)

	mplt.xticks(fontsize=ticksFontSZ)	
	mplt.yticks(fontsize=ticksFontSZ)
#	ax.set_ylim([-0.1, np.amax(PMajPgFlt)])
	mplt.scatter(jobDensity, PMajPgFlt)
        fig = matplotlib.pyplot.gcf()
        fig.set_size_inches(ImgWidth, ImgHeight)
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)

	roi_df = df[['jobDensity', 'MajPgFlt']]
	
	jobDensity = roi_df['jobDensity'].values.tolist()
	MajPgFlt   = roi_df['MajPgFlt'].values.tolist()
	jobDensity = [(float(item)/100) for item in jobDensity]
	
	noOfBars = 100
	fig, ax = mplt.subplots()
	filename = "JobDensityVsMajorPageFaults.png"
	
#	indices = np.arange(0, noOfBars*0.3, 0.3)
#	ax.set_xticks(indices+ 0.5*bar_width)
#	ax.set_xticklabels(jobDensity[:noOfBars])

        ax.set_ylabel("Value of total major page faults", fontweight=labelFontWT, fontsize=ticksFontSZ)
        ax.set_xlabel("Job Density", fontweight=labelFontWT, fontsize=ticksFontSZ)

	mplt.xticks(fontsize=ticksFontSZ)	
	mplt.yticks(fontsize=ticksFontSZ)
#	ax.set_ylim([-0.1, np.amax(MajPgFlt)])
	mplt.scatter(jobDensity, MajPgFlt)
        fig = matplotlib.pyplot.gcf()
        fig.set_size_inches(ImgWidth, ImgHeight)
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)

	roi_df = df[['jobDensity', 'majPgFltRate']]
	
	jobDensity 	= roi_df['jobDensity'].values.tolist()
	MajPgFltPerSec  = roi_df['majPgFltRate'].values.tolist()
	jobDensity      = [(float(item)/100) for item in jobDensity]
	
	noOfBars = 100
	fig, ax = mplt.subplots()
	filename = "JobDensityVsMajorPageFaultsPerSec.png"
	
#	indices = np.arange(0, noOfBars*0.3, 0.3)
#	ax.set_xticks(indices+ 0.5*bar_width)
#	ax.set_xticklabels(jobDensity[:noOfBars])
        ax.set_ylabel("Value of major page fault per second", fontweight=labelFontWT, fontsize=ticksFontSZ)
        ax.set_xlabel("Job Density", fontweight=labelFontWT, fontsize=ticksFontSZ)

	mplt.xticks(fontsize=ticksFontSZ)	
	mplt.yticks(fontsize=ticksFontSZ)
#	ax.set_ylim([-0.1, np.amax(MajPgFltPerSec)])
	mplt.scatter(jobDensity, MajPgFltPerSec)
        fig = matplotlib.pyplot.gcf()
        fig.set_size_inches(ImgWidth, ImgHeight)
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)

	avgMajPgFltRt 	= []
	jDensity 	= [100, 400, 800, 1600]
	for i in jDensity:
		roi_df     = df[['jobDensity', 'majPgFltRate']]
		roi_df     = roi_df[(roi_df['jobDensity'] == i)]
		vals 	   = roi_df['majPgFltRate'].values.tolist()
		vals       = [int(val) for val in vals]
		avgMajPgFltRt.append(np.mean(vals))
	
	noOfBars = len(jDensity)
	filename = "jobDensityVsAvgMajPgFltRt.png"
	fig, ax = mplt.subplots()
	indices = np.arange(0, noOfBars*0.3, 0.3)

	ax.bar(indices, avgMajPgFltRt[:noOfBars], bar_width, color='b')
	ax.set_xticks(indices+ 0.5*bar_width)
	ax.set_xticklabels(jDensity[:noOfBars])
	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')
	mplt.yticks(fontsize=ticksFontSZ)
	ax.set_ylabel("Average major page fault rate", fontweight=labelFontWT, fontsize=ticksFontSZ)
	ax.set_xlabel("Job Density", fontweight=labelFontWT, fontsize=ticksFontSZ)
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)

	pcntMajorPgFlts = []
	jDensity 	= [100, 400, 800, 1600]
	for i in jDensity:
		roi_df     = df[['jobDensity', 'Thrashing']]
		roi_df     = roi_df[(roi_df['jobDensity'] == i)]
		vals 	   = roi_df['Thrashing'].values.tolist()
		pcntMajorPgFlts.append(100.00*(float(vals.count(True)))/(float(len(vals))))
	
	noOfBars = len(jDensity)
	filename = "jobDensityVsPcntMajPgFlts.png"
	fig, ax = mplt.subplots()
	indices = np.arange(0, noOfBars*0.3, 0.3)

	ax.bar(indices, pcntMajorPgFlts[:noOfBars], bar_width, color='b')
	ax.set_xticks(indices+ 0.5*bar_width)
	ax.set_xticklabels(jDensity[:noOfBars])
	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')
	mplt.yticks(fontsize=ticksFontSZ)
	ax.set_ylabel("Percentage of Jobs with major page faults", fontweight=labelFontWT, fontsize=ticksFontSZ)
	ax.set_xlabel("Job Density", fontweight=labelFontWT, fontsize=ticksFontSZ)
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)

	return 
	
if len(sys.argv) != 3:
	print "Usage: ./Script.sh <Accounting file> <Path to save Plots>"
	exit()

df = pd.io.parsers.read_csv(sys.argv[1], sep = '\t')
df = pd.DataFrame.sort (df, columns = 'JobID')

#print df.columns.values.tolist()
coresVsJobs(df)
#usersVsPgFlt(df)
'''
grpVsNJobs(df)
coresVsPageFaults(df)
usersVsJobs(df)
grpVsJobs(df)
grpVsPgFlt(df)
grpVsUniqUsers(df)
jobDensityVsMajPageFlt(df)
'''
#jobsPerDay(df)
