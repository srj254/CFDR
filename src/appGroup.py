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

# AppGroup on X Axis
patterns        = [ '', '', '','/','\\','o','.','' ]
outlinewgt      = [ 1 , 1 , 1 , 1 , 1  , 1 , 1 , 1.5 ]

gray = 0.5
red  = 'r'
green= 'g'
blue = 'b'
black= 'k'
white= 'w'
lightblue = 'lightblue'

bar_width       = 0.25
barSpacing      = 0.05

xlabelFontSZ    = 16
ylabelFontSZ    = 16
labelFontSZ     = 16

xticksFontSZ    = 12
yticksFontSZ    = 12
ticksFontSZ     = 12

ylabelFontWT    = 'bold'
xlabelFontWT    = 'bold'
labelFontWT     = 'bold'

ImgFormat       = 'png'
ImgDPI          = 700
ImgWidth        = 18.5
ImgHeight       = 10.5
ImgProp         = 'tight'
ImgNoteX	= 0.80
ImgNoteY	= 0.85

def grpVsJobs(df):
	# First plot
	gf = df[df['JobGrp'] != "-NA-"]

	grps 	  = (gf['JobGrp'].values.tolist())
	thrshGrps = (gf[gf['Thrashing'] == True]['JobGrp'].values.tolist())

	groups 		= []
	thrshGroups 	= []
	for grp in list(set(grps)):
		grpPcnt = float(grps.count(grp))*100.00/float(len(grps))
		grpFltPcnt = float(thrshGrps.count(grp))*100.00/float(grps.count(grp))
		groups.append((grp, grpPcnt, (grpPcnt - (grpPcnt*grpFltPcnt/100.00)), \
							(grpPcnt*grpFltPcnt/100.00)))
	groups, grpPcnt, pcntges, fltPcnt = zip(*sorted(groups, key=lambda x:x[1], reverse=True))
	
	noOfBars = 50
	filename = "500TAppGrpsVsJobs_Percentages.png"
	fig, ax = mplt.subplots()
	indices = np.arange(0, noOfBars*0.3, 0.3)

	bottomBar = ax.bar(indices, fltPcnt[:noOfBars], bar_width, color=blue, linewidth=outlinewgt[-1], hatch='/////')
	topBar 	  = ax.bar(indices, pcntges[:noOfBars], bar_width, bottom=fltPcnt[:noOfBars], color=lightblue, linewidth=outlinewgt[-1], hatch='/////')

        ax.text(ImgNoteX, ImgNoteY, 'Threshold: Peak major page fault > 200', \
                horizontalalignment='center', \
                verticalalignment='center', \
		transform=ax.transAxes, fontweight=labelFontWT, fontsize=ticksFontSZ)

	ax.set_xticks(indices+ 0.5*bar_width)
	ax.set_xticklabels(groups[:noOfBars])
	# ax.set_xticklabels([])
	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')
	mplt.yticks(fontsize=ticksFontSZ)
	ax.set_ylabel("% of jobs", fontweight=labelFontWT, fontsize=ticksFontSZ)
	ax.set_xlabel("Top "+str(noOfBars)+" AppGroup", fontweight=labelFontWT, fontsize=ticksFontSZ)
        fig = matplotlib.pyplot.gcf()
	mplt.legend( (bottomBar[0], topBar[1]), ("% of Jobs < Threshold", "% of Jobs > Threshold") )
	fig.set_size_inches(ImgWidth, ImgHeight)
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)

	# Second plot 
	gf 	  = df[df['JobGrp'] != "-NA-"]
	grps 	  = (gf['JobGrp'].values.tolist())
	thrshGrps = (gf[gf['Thrashing'] == True]['JobGrp'].values.tolist())

	groups 		= []
	thrshGroups 	= []
	for grp in list(set(grps)):
		grpNums = grps.count(grp)
		grpFltNums = thrshGrps.count(grp)
		groups.append((grp, grpNums, (grpNums - grpFltNums), grpFltNums))
		
	groups, grpNums, numbers, grpFltNums = zip(*sorted(groups, key=lambda x:x[1], reverse=True))
	
	noOfBars = 50
	filename = "500TAppGrpsVsJobs_RawNumbers.png"
	fig, ax = mplt.subplots()
	indices = np.arange(0, noOfBars*0.3, 0.3)

	bottomBar = ax.bar(indices, grpFltNums[:noOfBars], bar_width, color=blue, linewidth=outlinewgt[-1], hatch='/')
	topBar 	  = ax.bar(indices, numbers[:noOfBars], bar_width, bottom=grpFltNums[:noOfBars],\
			   color=lightblue, linewidth=outlinewgt[-1], hatch='/')

        ax.text(ImgNoteX, ImgNoteY, \
		'Threshold: Peak major page fault > 200', \
                horizontalalignment='center', \
                verticalalignment='center', \
		transform=ax.transAxes, fontweight=labelFontWT, fontsize=ticksFontSZ)

	ax.set_xticks(indices+ 0.5*bar_width)
	ax.set_xticklabels(groups[:noOfBars])
	# ax.set_xticklabels([])
	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical', )
	mplt.yticks(fontsize=ticksFontSZ)
	ax.set_ylabel("Number of jobs", fontweight=labelFontWT, fontsize=ticksFontSZ)
	ax.set_xlabel("Top "+str(noOfBars)+" AppGroup", fontweight=labelFontWT, fontsize=ticksFontSZ)
        fig = matplotlib.pyplot.gcf()
	mplt.legend( (bottomBar[0], topBar[1]), ("Number of Jobs < Threshold", "Number of Jobs > Threshold") )
	fig.set_size_inches(ImgWidth, ImgHeight)
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)

	# Third plot
	gf 	  = df[df['JobGrp'] != "-NA-"]
	grps 	  = (gf['JobGrp'].values.tolist())
	thrshGrps = (gf[gf['Thrashing'] == True]['JobGrp'].values.tolist())

	groups 		= []
	thrshGroups 	= []
	for grp in list(set(grps)):
		if grps.count(grp) < 100:
			continue
		grpPcnt = float(grps.count(grp))*100.00/float(len(grps))
		grpFltPcnt = float(thrshGrps.count(grp))*100.00/float(grps.count(grp))
		groups.append((grp, grpPcnt, grpFltPcnt))

	groups, grpPcnt, fltPcnt = zip(*sorted(groups, key=lambda x:x[2], reverse=True))
	
	noOfBars = 100
	filename = "500TAppGrpsVsPcntOfAppGrpsFaultyJobs.png"
	fig, ax = mplt.subplots()
	indices = np.arange(0, noOfBars*0.3, 0.3)

	bottomBar = ax.bar(indices, fltPcnt[:noOfBars], bar_width, color=blue, \
			   linewidth=outlinewgt[-1], hatch='/')
	#topBar = ax.bar(indices, pcntges[:noOfBars], bar_width, bottom=fltPcnt[:noOfBars],
	#	         color=lightblue, linewidth=outlinewgt[-1], hatch='/////')

        ax.text(ImgNoteX, ImgNoteY, 'Threshold: Peak major page fault > 200', \
                horizontalalignment='center', \
                verticalalignment='center', \
		transform=ax.transAxes, fontweight=labelFontWT, fontsize=ticksFontSZ)

	ax.set_xticks(indices+ 0.5*bar_width)
	ax.set_xticklabels(groups[:noOfBars])
	# ax.set_xticklabels([])
	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')
	mplt.yticks(fontsize=ticksFontSZ)
	ax.set_ylabel("% of jobs Of AppGroup > Threshold", fontweight=labelFontWT, fontsize=ticksFontSZ)
	ax.set_xlabel("Top "+str(noOfBars)+" AppGroup", fontweight=labelFontWT, fontsize=ticksFontSZ)
        fig = matplotlib.pyplot.gcf()
	#mplt.legend( (bottomBar[0], topBar[1]), ("% of Jobs < Threshold", "% of Jobs > Threshold") )
	fig.set_size_inches(ImgWidth, ImgHeight)
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)

	# Fourth plot 
	gf 	  = df[df['JobGrp'] != "-NA-"]
	grps 	  = (gf['JobGrp'].values.tolist())
	thrshGrps = (gf[gf['Thrashing'] == True]['JobGrp'].values.tolist())

	groups 		= []
	thrshGroups 	= []
	for grp in list(set(grps)):
		grpNums = grps.count(grp)
		grpFltNums = thrshGrps.count(grp)
		groups.append((grp, grpNums, (grpNums - grpFltNums), grpFltNums))
		
	groups, grpNums, numbers, grpFltNums = zip(*sorted(groups, key=lambda x:x[3], reverse=True))
	
	noOfBars = 50
	filename = "500TAppGrpsVsNoOfFaultyJobsPerAppGrp.png"
	fig, ax = mplt.subplots()
	indices = np.arange(0, noOfBars*0.3, 0.3)

	bottomBar = ax.bar(indices, grpFltNums[:noOfBars], bar_width, color=blue,\
			   linewidth=outlinewgt[-1], hatch='/')
	#topBar   = ax.bar(indices, pcntges[:noOfBars], bar_width, bottom=fltPcnt[:noOfBars],\
	#		   color=lightblue, linewidth=outlinewgt[-1], hatch='/////')

        ax.text(ImgNoteX, ImgNoteY, \
		'Threshold: Peak major page fault > 200', \
                horizontalalignment='center', \
                verticalalignment='center', \
		transform=ax.transAxes, fontweight=labelFontWT, fontsize=ticksFontSZ)

	ax.set_xticks(indices+ 0.5*bar_width)
	ax.set_xticklabels(groups[:noOfBars])
	# ax.set_xticklabels([])
	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')
	mplt.yticks(fontsize=ticksFontSZ)
	ax.set_ylabel("Number of jobs", fontweight=labelFontWT, fontsize=ticksFontSZ)
	ax.set_xlabel("Top "+str(noOfBars)+" AppGroup", fontweight=labelFontWT, fontsize=ticksFontSZ)
        fig = matplotlib.pyplot.gcf()
	#mplt.legend( (bottomBar[0], topBar[1]), ("Number of Jobs < Threshold", "Number of Jobs > Threshold") )
	fig.set_size_inches(ImgWidth, ImgHeight)
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)

	# Fifth plot
	gf 	  = df[df['JobGrp'] != "-NA-"]
	grps 	  = (gf['JobGrp'].values.tolist())
	thrshGrps = (gf[gf['Thrashing'] == True]['JobGrp'].values.tolist())

	groups 		= []
	thrshGroups 	= []
	for grp in list(set(grps)):
		if grps.count(grp) < 100:
			continue
		grpPcnt = float(grps.count(grp))*100.00/float(len(grps))
		grpFltPcnt = float(thrshGrps.count(grp))*100.00/float(len(grps))
		groups.append((grp, grpPcnt, grpFltPcnt))

	groups, grpPcnt, fltPcnt = zip(*sorted(groups, key=lambda x:x[2], reverse=True))
	
	noOfBars = 50
	filename = "500TAppGrpsVsPcntOfFaultyJobsPerAppGrp.png"
	fig, ax = mplt.subplots()
	indices = np.arange(0, noOfBars*0.3, 0.3)

	bottomBar = ax.bar(indices, fltPcnt[:noOfBars], bar_width, color=blue, \
			   linewidth=outlinewgt[-1], hatch='/')
	#topBar = ax.bar(indices, pcntges[:noOfBars], bar_width, bottom=fltPcnt[:noOfBars],
	#	         color=lightblue, linewidth=outlinewgt[-1], hatch='/////')

        ax.text(ImgNoteX, ImgNoteY, 'Threshold: Peak major page fault > 200', \
                horizontalalignment='center', \
                verticalalignment='center', \
		transform=ax.transAxes, fontweight=labelFontWT, fontsize=ticksFontSZ)

	ax.set_xticks(indices+ 0.5*bar_width)
	ax.set_xticklabels(groups[:noOfBars])
	# ax.set_xticklabels([])
	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')
	mplt.yticks(fontsize=ticksFontSZ)
	ax.set_ylabel("% of jobs > Threshold (In each AppGroup)", fontweight=labelFontWT, fontsize=ticksFontSZ)
	ax.set_xlabel("Top "+str(noOfBars)+" AppGroup", fontweight=labelFontWT, fontsize=ticksFontSZ)
        fig = matplotlib.pyplot.gcf()
	#mplt.legend( (bottomBar[0], topBar[1]), ("% of Jobs < Threshold", "% of Jobs > Threshold") )
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
