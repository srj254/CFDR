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

# Users on X Axis
patterns	= [ '', '', '','/','\\','o','.','' ]

gray = 0.5
red  = 'r'
green= 'g'
blue = 'b'
black= 'k'
white= 'w'
lightblue = 'lightblue'

outlinewgt	= [ 1 , 1 , 1 , 1 , 1  , 1 , 1 , 1.5 ]

bar_width	= 0.25
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
ImgDPI		= 700
ImgWidth	= 18.5
ImgHeight	= 10.5
ImgProp		= 'tight'
ImgNoteX	= 0.80
ImgNoteY	= 0.85

def usersVsJobs(df):
	### Plot with percentages
	userList  = df['user'].values.tolist()
	user2Jobs = []
	for user in list(set(userList)):
		user2Jobs.append((user, (100.00 * float(userList.count(user)))/(float(len(userList)))))

	user2Jobs = sorted(user2Jobs, key=lambda x:x[1], reverse=True)
	users, jobs = zip(*user2Jobs)

	topUsers 	= users
	topJobPcnt	= jobs

	pcntFltyJobs = []
	for usr in topUsers:
		totalUsrJobs = userList.count(usr)
		roi_df = df[df['user'] == usr]
		roi_df = roi_df[roi_df['Thrashing']==True]
		totalFltyJobs = len(roi_df['user'].values.tolist())
		pcntFltyJobs.append(float(totalFltyJobs)/float(totalUsrJobs))
	
	fltDiffPcnt = []
	normalJobPcnt = []
	for pcnt, fltPcnt in zip(topJobPcnt, pcntFltyJobs):
		val = pcnt*fltPcnt
		fltDiffPcnt.append(val)
		normalJobPcnt.append(pcnt - val)

	noOfBars = 50
	filename = "500TUsersVsJobs_Percentages.png"
	fig, ax = mplt.subplots()
	indices = np.arange(0, noOfBars*0.3, 0.3)

	bottomBar = ax.bar(indices, fltDiffPcnt[:noOfBars], bar_width, color=blue, \
			   linewidth=outlinewgt[-1], hatch='////')
	topBar    = ax.bar(indices, normalJobPcnt[:noOfBars], bar_width, \
			   bottom=fltDiffPcnt[:noOfBars], color=lightblue, \
			   linewidth=outlinewgt[-1], hatch='////')

	ax.text(ImgNoteX, ImgNoteY, 'Threshold: Peak major page fault > 500', \
		horizontalalignment='center', \
		verticalalignment='center', \
		transform=ax.transAxes, fontsize=ticksFontSZ, fontweight=labelFontWT)

	ax.set_xticks(indices+ 0.5*bar_width)
	ax.set_xticklabels([])
	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')
	mplt.yticks(fontsize=ticksFontSZ)
	ax.set_ylabel("% of jobs", fontweight=labelFontWT, fontsize=ticksFontSZ)
	ax.set_xlabel("Top "+str(noOfBars)+" users", fontweight=labelFontWT, fontsize=ticksFontSZ)		
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	mplt.legend((bottomBar[0], topBar[0]), ("% of Jobs > Threshold", "% of Jobs < Threshold"))
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)

	### Plot with Actual numbers
	userList  = df['user'].values.tolist()
	user2Jobs = []
	for user in list(set(userList)):
		user2Jobs.append((user, userList.count(user)))

	user2Jobs = sorted(user2Jobs, key=lambda x:x[1], reverse=True)
	users, jobs = zip(*user2Jobs)

	topUsers 	= users
	topJobCount	= jobs

	countFltyJobs = []
	for usr in topUsers:
		totalUsrJobs = userList.count(usr)
		roi_df = df[df['user'] == usr]
		roi_df = roi_df[roi_df['Thrashing']==True]
		totalFltyJobs = len(roi_df['user'].values.tolist())
		countFltyJobs.append(totalFltyJobs)
	
	fltDiffCount = []
	normalJobCount = []
	for count, fltCount in zip(topJobCount, countFltyJobs):
		val = fltCount
		fltDiffCount.append(val)
		normalJobCount.append(count - val)

	noOfBars = 50
	filename = "500TUsersVsJobs_RawNumbers.png"
	fig, ax = mplt.subplots()
	indices = np.arange(0, noOfBars*0.3, 0.3)

	bottomBar = ax.bar(indices, fltDiffCount[:noOfBars], bar_width, color=blue, \
			   linewidth=outlinewgt[-1], hatch='/////')
	topBar    = ax.bar(indices, normalJobCount[:noOfBars], bar_width, \
			   bottom=fltDiffCount[:noOfBars], color=lightblue, linewidth=outlinewgt[-1], hatch='/////')

	ax.text(ImgNoteX, ImgNoteY, 'Threshold: Peak major page fault > 500', \
		horizontalalignment='center', \
		verticalalignment='center', \
		transform=ax.transAxes, fontsize=ticksFontSZ, fontweight=labelFontWT)

	ax.set_xticks(indices+ 0.5*bar_width)
	ax.set_xticklabels([])
	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')
	mplt.yticks(fontsize=ticksFontSZ)
	ax.set_ylabel("Number of jobs", fontweight=labelFontWT, fontsize=ticksFontSZ)
	ax.set_xlabel("Top "+str(noOfBars)+" users", fontweight=labelFontWT, fontsize=ticksFontSZ)		
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	mplt.legend((bottomBar[0], topBar[0]), ("Number of Jobs > Threshold", "Number of Jobs < Threshold"))
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)
	
	#####################################################################################################
	### Third Plot.
	### Users vs (No. of Jobs with Peak Major Page fault > Threshold)
	roi_df = df[['user', 'Thrashing']]
	roi_df = roi_df[(roi_df['Thrashing'] == True)]
	users  = roi_df['user'].values.tolist()
	
	thrashingUserJobs = users

	jobs = []
	for user in list(set(users)):
		jobs.append((user, users.count(user)))
	jobs = sorted(jobs, key=lambda x: x[1], reverse=True)
	users, jobs = zip(*jobs)
	
	noOfBars = 100
	filename = "500TUsersVsNoOfFaultyJobs.png"
	fig, ax = mplt.subplots()
	indices = np.arange(0, noOfBars*0.3, 0.3)

	ax.text(ImgNoteX, ImgNoteY, 'Threshold: Peak major page fault > 500', \
		horizontalalignment='center', \
		verticalalignment='center', \
		transform=ax.transAxes, fontsize=ticksFontSZ, fontweight=labelFontWT)
	
	ax.bar(indices, jobs[:noOfBars], bar_width/2, color=blue)
	ax.set_xticks(indices+ 0.5*bar_width)
	ax.set_xticklabels(users[:noOfBars])
	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')
	mplt.yticks(fontsize=ticksFontSZ)
	ax.set_ylabel("No of jobs > Threshold major page fault", fontweight=labelFontWT, fontsize=ticksFontSZ)
	ax.set_xlabel("Top "+str(noOfBars)+" users", fontweight=labelFontWT, fontsize=ticksFontSZ)
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)
	
	### Fourth Plot. 
	### Users vs (% of Jobs (out of Jobs submitted by the user)
	### 		with Peak Major Page fault > Threshold)
	roi_df = df[['user', 'Thrashing']]
	users  = roi_df['user'].values.tolist()
	
	jobs = []
	for user in list(set(users)):
		if users.count(user) < 100:
			continue # Filter of minimum number of jobs
		percent = (float(thrashingUserJobs.count(user))/float(users.count(user)))*100
		jobs.append((user, percent))
	users, percent  = zip(*sorted(jobs, key=lambda x:x[1], reverse=True))
	
	noOfBars = len(users)
	filename = "500TUsersVsPcntOfUsersFltyJobs.png"
	fig, ax = mplt.subplots()
	indices = np.arange(0, noOfBars*0.3, 0.3)

	ax.text(ImgNoteX, ImgNoteY, 'Threshold: Peak major page fault > 500', \
		horizontalalignment='center', \
		verticalalignment='center', \
		transform=ax.transAxes, fontsize=ticksFontSZ, fontweight=labelFontWT)
	ax.bar(indices, percent[:noOfBars], bar_width/2, color=blue)
	ax.set_xticks(indices+ 0.5*bar_width)
	ax.set_xticklabels([])
	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')
	mplt.yticks(fontsize=ticksFontSZ)
	ax.set_ylabel("% of User's Jobs > Threshold", fontweight=labelFontWT, fontsize=ticksFontSZ)
	ax.set_xlabel("Top "+str(noOfBars)+" Users", fontweight=labelFontWT, fontsize=ticksFontSZ)
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)
	
	### Fifth Plot. 
	### Users vs (% of Jobs with Peak Major Page fault > Threshold)

	roi_df = df[['user', 'Thrashing']]
	users  = roi_df['user'].values.tolist()
	
	jobs = []
	for user in list(set(users)):
		if users.count(user) < 100:
			continue # Filter of minimum number of jobs
		percent = (float(thrashingUserJobs.count(user))/len(users))*100
		jobs.append((user, percent))
	users, percent  = zip(*sorted(jobs, key=lambda x:x[1], reverse=True))
	
	noOfBars = len(users)
	filename = "500TUsersVsPcntOfFltyJobsPerUser.png"
	fig, ax = mplt.subplots()
	indices = np.arange(0, noOfBars*0.3, 0.3)

	ax.text(ImgNoteX, ImgNoteY, 'Threshold: Peak major page fault > 500', \
		horizontalalignment='center', \
		verticalalignment='center', \
		transform=ax.transAxes, fontsize=ticksFontSZ, fontweight=labelFontWT)
	ax.bar(indices, percent[:noOfBars], bar_width/2, color=blue)
	ax.set_xticks(indices+ 0.5*bar_width)
	ax.set_xticklabels([])
	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')
	mplt.yticks(fontsize=ticksFontSZ)
	ax.set_ylabel("% of jobs > Threshold (For each user)", fontweight=labelFontWT, fontsize=ticksFontSZ)
	ax.set_xlabel("Top "+str(noOfBars)+" Users", fontweight=labelFontWT, fontsize=ticksFontSZ)
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)

	return 
