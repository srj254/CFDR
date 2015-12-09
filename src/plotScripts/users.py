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
import labelBar

# Users on X Axis
patterns	= [ '', '', '','/','\\','o','.','' ]

gray = 0.5
red  = 'Crimson'
green= 'g'
blue = 'b'
black= 'k'
white= 'w'
yellow='y'
lightblue = 'lightblue'

outlinewgt	= [ 1 , 1 , 1 , 1 , 1  , 1 , 1 , 0.5 ]

bar_width	= 0.25
barSpacing	= 0.05

xlabelFontSZ	= 14
ylabelFontSZ	= 14
labelFontSZ	= 14

xticksFontSZ	= 10
yticksFontSZ	= 10
ticksFontSZ	= 10
legendFontSZ	= 12

ylabelFontWT	= 'normal'
xlabelFontWT	= 'normal'
labelFontWT	= 'normal'

ImgFormat	= 'png'
ImgDPI		= 1000
ImgWidth	= 7
ImgHeight	= 4
ImgProp		= 'tight'
ImgNoteX	= 0.80
ImgNoteY	= 0.85

'''
def labelBar(axis, bar, bottombar, text, factor):
	ht = bar.get_height()
	if bottombar is not None:
		ht += bottombar.get_height()
	axis.text(bar.get_x()+bar.get_width()/2.0, (factor+1.02)*ht, ' '+text,
                ha='center', va='bottom', fontsize=10)
	return
'''
def usersVsJobs(df):
	'''
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
	'''
	
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
	for usr in topUsers[:10]:
		totalUsrJobs = userList.count(usr)
		roi_df = df[df['user'] == usr]
		roi_df = roi_df[roi_df['Thrashing']==True]
		totalFltyJobs = len(roi_df['user'].values.tolist())
		countFltyJobs.append(totalFltyJobs)
		print usr, totalFltyJobs

	#print topUsers[:10], list(topUsers[:10]).sum()
	print user2Jobs[:10]
	exit()
	
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

	topBar    = ax.bar(indices, topJobCount[:noOfBars], bar_width, \
			   color=yellow, linewidth=outlinewgt[-1])
	bottomBar = ax.bar(indices, fltDiffCount[:noOfBars], 0.75*bar_width, color=red, \
			   linewidth=outlinewgt[-1])

	for i in range(6):
		s = labelBar.labelBar(ax, topBar[i], None, \
			 str(int(float(topJobCount[i])*100.00/len(userList)))+'%', 0.03, 0)
		if s == 0:
			continue
		labelBar.labelBar(ax, bottomBar[i], None, \
			 str(int(float(fltDiffCount[i])*100.00/topJobCount[i]))+'%', 0.0, 1)

	#ax.text(ImgNoteX, ImgNoteY, 'Threshold: Peak major page fault > 500', \
	#	horizontalalignment='center', \
	#	verticalalignment='center', \
	#	transform=ax.transAxes, fontsize=ticksFontSZ, fontweight=labelFontWT)

	ax.set_xticks(indices+ 0.5*bar_width)
	ax.set_xticklabels([])
	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')
	mplt.yticks(fontsize=ticksFontSZ)
	plt.tick_params(
		axis  ='both',       # changes apply to the x-axis
		which ='both',      # both major and minor ticks are affected
    		bottom='off',      # ticks along the bottom edge are off
    		top   ='off',         # ticks along the top edge are off
		right ='off',	   # ticks along the left edge are off
		left  ='off')        # ticks along the right edge are off

	ax.set_ylabel("No. of jobs", fontweight=labelFontWT, fontsize=labelFontSZ)
	ax.set_xlabel("Top "+str(noOfBars)+" users", fontweight=labelFontWT, fontsize=labelFontSZ)		
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	mplt.legend((bottomBar[0], topBar[0]), ("No. of users jobs > Threshold", "No. of users jobs"))
	#mplt.setp(plt.gca().get_legend().get_texts(), fontsize='20')
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)
	
	#####################################################################################################
	### Third Plot.
	### Users vs (No. of Jobs with Peak Major Page fault > Threshold)
	roi_df = df[['user', 'Thrashing']]
	allUserJobs = roi_df['user'].values.tolist()	
	roi_df = roi_df[(roi_df['Thrashing'] == True)]
	thrashingUserJobs  = roi_df['user'].values.tolist()
	users = thrashingUserJobs

	jobs = []
	for user in list(set(users)):
		jobs.append((user, users.count(user)))
	jobs = sorted(jobs, key=lambda x: x[1], reverse=True)
	users, jobs = zip(*jobs)
	'''	
	noOfBars = 100
	filename = "500TUsersVsNoOfFaultyJobs.png"
	fig, ax = mplt.subplots()
	indices = np.arange(0, noOfBars*0.3, 0.3)

	#ax.text(ImgNoteX, ImgNoteY, 'Threshold: Peak major page fault > 500', \
	#	horizontalalignment='center', \
	#	verticalalignment='center', \
	#	transform=ax.transAxes, fontsize=ticksFontSZ, fontweight=labelFontWT)
	topBar = ax.bar(indices, jobs[:noOfBars], bar_width/2, color=blue)
	#for i in range(5):
	#	labelBar(ax, topBar[i], None, str(int(jobs[i])))

	ax.set_xticks(indices+ 0.5*bar_width)
	ax.set_xticklabels([])
	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')
	mplt.yticks(fontsize=ticksFontSZ)
	plt.tick_params(
		axis  ='both',       # changes apply to the x-axis
		which ='both',      # both major and minor ticks are affected
    		bottom='off',      # ticks along the bottom edge are off
    		top   ='off',         # ticks along the top edge are off
		right ='off',	   # ticks along the left edge are off
		left  ='off')        # ticks along the right edge are off

	ax.set_ylabel("No. of users jobs\ngreater than threshold", \
		       fontweight=labelFontWT, fontsize=labelFontSZ)
	ax.set_xlabel("Users with atleast 100 jobs", \
			fontweight=labelFontWT, fontsize=labelFontSZ)
        fig = matplotlib.pyplot.gcf()
	#mplt.setp(plt.gca().get_legend().get_texts(), fontsize='20')
	fig.set_size_inches(ImgWidth, ImgHeight)
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)
	'''
	
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
	plt.tick_params(
		axis  ='both',       # changes apply to the x-axis
		which ='both',      # both major and minor ticks are affected
    		bottom='off',      # ticks along the bottom edge are off
    		top   ='off',         # ticks along the top edge are off
		right ='off',	   # ticks along the left edge are off
		left  ='off')        # ticks along the right edge are off

	#ax.text(ImgNoteX, ImgNoteY, 'Threshold: Peak major page fault > 500', \
	#	horizontalalignment='center', \
	#	verticalalignment='center', \
	#	transform=ax.transAxes, fontsize=ticksFontSZ, fontweight=labelFontWT)

	ax.bar(indices, percent[:noOfBars], bar_width/2, color=red, alpha = 0.5)
	ax.set_xticks(indices+ 0.5*bar_width)
	ax.set_xticklabels([])
	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')
	mplt.yticks(fontsize=ticksFontSZ)
	ax.set_ylabel("% of user jobs greater than threshold", fontweight=labelFontWT, fontsize=labelFontSZ)
	ax.set_xlabel("Users with atleast 100 jobs", fontweight=labelFontWT, fontsize=labelFontSZ)
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)

	'''
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
	'''
	return 
