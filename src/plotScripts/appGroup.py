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

# AppGroup on X Axis
patterns        = [ '', '', '','/','\\','o','.','' ]
outlinewgt      = [ 1 , 1 , 1 , 1 , 1  , 1 , 0.5]

gray = 0.5
red  = 'Crimson'
green= 'g'
blue = 'b'
black= 'k'
white= 'w'
yellow='y'
lightblue = 'lightblue'

bar_width       = 0.25
barSpacing      = 0.05

xlabelFontSZ    = 14
ylabelFontSZ    = 14
labelFontSZ     = 14
legendFontSZ	= 12

xticksFontSZ    = 10
yticksFontSZ    = 10
ticksFontSZ     = 10

ylabelFontWT    = 'normal'
xlabelFontWT    = 'normal'
labelFontWT     = 'normal'

ImgFormat       = 'png'
ImgDPI          = 1000
ImgWidth        = 7
ImgHeight       = 4
ImgProp         = 'tight'
ImgNoteX	= 0.80
ImgNoteY	= 0.85
'''
def labelBar(axis, bar, bottombar, text, factor):
	ht = bar.get_height()
	if bottombar is not None:
		ht += bottombar.get_height()
	axis.text(bar.get_x()+bar.get_width()/2.0, (1.02+factor)*ht, '   '+text,
                ha='center', va='bottom', fontsize=10)
	return
	'''

def grpVsJobs(df):
	'''
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

        ax.text(ImgNoteX, ImgNoteY, 'Threshold: Peak major page fault > 500', \
                horizontalalignment='center', \
                verticalalignment='center', \
		transform=ax.transAxes, fontweight=labelFontWT, fontsize=ticksFontSZ)

	ax.set_xticks(indices+ 0.5*bar_width)
	#ax.set_xticklabels(groups[:noOfBars])
	ax.set_xticklabels([])
	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')
	mplt.yticks(fontsize=ticksFontSZ)

	ax.set_ylabel("% of jobs", fontweight=labelFontWT, fontsize=ticksFontSZ)
	ax.set_xlabel("Top "+str(noOfBars)+" app group", fontweight=labelFontWT, fontsize=ticksFontSZ)

        fig = matplotlib.pyplot.gcf()

	mplt.legend( (bottomBar[0], topBar[0]), ("% of jobs >  Threshold", "% of jobs > Threshold"))
	fig.set_size_inches(ImgWidth, ImgHeight)
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)
	'''

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

	topBar 	  = ax.bar(indices, grpNums[:noOfBars], bar_width,\
			   color=yellow, linewidth=outlinewgt[-1])#, hatch='/')
	bottomBar = ax.bar(indices, grpFltNums[:noOfBars], 0.75*bar_width, \
			   color=red, linewidth=outlinewgt[-1])#, hatch='/')

        #ax.text(ImgNoteX, ImgNoteY, \
	#	'Threshold for peak major page fault = 500', \
        #       horizontalalignment='center', \
        #       verticalalignment='center', \
	#	transform=ax.transAxes, fontweight=labelFontWT, fontsize=ticksFontSZ)
	
	for i in range(6):
		s = labelBar.labelBar(ax, topBar[i], None, \
			 str(int(float(grpNums[i])*100.00/len(grps)))+'%', 0.03, 0)
		if s == 0:
			continue
		labelBar.labelBar(ax, bottomBar[i], None, \
			 str(int(float(grpFltNums[i])*100.00/grpNums[i]))+'%', 0.0, 1)

	ax.set_xticks(indices+ 0.5*bar_width)
	#ax.set_xticklabels(groups[:noOfBars])
	ax.set_xticklabels([])
	#mplt.xticks(fontsize=ticksFontSZ, rotation='vertical' )
	#mplt.yticks(fontsize=ticksFontSZ)
	plt.xticks(fontsize=ticksFontSZ, rotation='vertical')
	plt.yticks(fontsize=ticksFontSZ)
	#ax.set_ylabel("No. of jobs", fontweight=labelFontWT, fontsize=labelFontSZ)
	#ax.set_xlabel("App groups", fontweight=labelFontWT, fontsize=labelFontSZ)
	#ax.set_ylabel("No. of jobs", fontsize=labelFontSZ)
	#ax.set_xlabel("App groups", fontsize=labelFontSZ)
	plt.ylabel("No. of jobs", fontsize=labelFontSZ)
	plt.xlabel("Top "+ str(noOfBars) +" App groups", fontsize=labelFontSZ)
        fig = matplotlib.pyplot.gcf()
	plt.tick_params(
		axis  ='both',       # changes apply to the x-axis
		which ='both',      # both major and minor ticks are affected
    		bottom='off',      # ticks along the bottom edge are off
    		top   ='off',         # ticks along the top edge are off
		right ='off',	   # ticks along the left edge are off
		left  ='off')        # ticks along the right edge are off
	mplt.legend( (bottomBar[0], topBar[1]),\
		     ("No. of app group jobs > Threshold", "No. of app group jobs"))
	fig.set_size_inches(ImgWidth, ImgHeight)
	#mplt.setp(plt.gca().get_legend().get_texts(), fontsize=legendFontSZ)
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)
	mplt.close()	
	
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
	
	noOfBars = len(groups)
	filename = "500TAppGrpsVsPcntOfAppGrpsFaultyJobs.png"
	fig, ax = mplt.subplots()
	indices = np.arange(0, noOfBars*0.3, 0.3)

	bottomBar = ax.bar(indices, fltPcnt[:noOfBars], bar_width/2, color=red, \
			   linewidth=outlinewgt[-1], hatch='/')
	#topBar = ax.bar(indices, pcntges[:noOfBars], bar_width, bottom=fltPcnt[:noOfBars],
	#	         color=lightblue, linewidth=outlinewgt[-1], hatch='/////')

        #ax.text(ImgNoteX, ImgNoteY, 'Threshold for peak major page fault = 500', \
        #        horizontalalignment='center', \
        #        verticalalignment='center', \
	#	transform=ax.transAxes, fontweight=labelFontWT, fontsize=ticksFontSZ)

	ax.set_xticks(indices+ 0.5*bar_width/2)

	plt.tick_params(
		axis  ='both',       # changes apply to the x-axis
		which ='both',      # both major and minor ticks are affected
    		bottom='off',      # ticks along the bottom edge are off
    		top   ='off',         # ticks along the top edge are off
		right ='off',	   # ticks along the left edge are off
		left  ='off')        # ticks along the right edge are off

	#ax.set_xticklabels(groups[20:])
	ax.set_xticklabels([])
	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')
	mplt.yticks(fontsize=ticksFontSZ)
	ax.set_ylabel("% of app group jobs\nwhich crossed threshold", fontweight=labelFontWT, fontsize=labelFontSZ)
	ax.set_xlabel("AppGroups with atleast 100 jobs", fontweight=labelFontWT, fontsize=labelFontSZ)
        fig = matplotlib.pyplot.gcf()
	#mplt.legend( (bottomBar[0], topBar[1]), ("% of Jobs < Threshold", "% of Jobs > Threshold") )
	fig.set_size_inches(ImgWidth, ImgHeight)
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)

	'''
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
		'Threshold: Peak major page fault > 500', \
                horizontalalignment='center', \
                verticalalignment='center', \
		transform=ax.transAxes, fontweight=labelFontWT, fontsize=ticksFontSZ)

	ax.set_xticks(indices+ 0.5*bar_width)
	#ax.set_xticklabels(groups[:noOfBars])
	ax.set_xticklabels([])
	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')
	mplt.yticks(fontsize=ticksFontSZ)
	ax.set_ylabel("Number of jobs crossed threshold", fontweight=labelFontWT, fontsize=ticksFontSZ)
	ax.set_xlabel("AppGroups", fontweight=labelFontWT, fontsize=ticksFontSZ)
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

        ax.text(ImgNoteX, ImgNoteY, 'Threshold: Peak major page fault > 500', \
                horizontalalignment='center', \
                verticalalignment='center', \
		transform=ax.transAxes, fontweight=labelFontWT, fontsize=ticksFontSZ)

	ax.set_xticks(indices+ 0.5*bar_width)
	#ax.set_xticklabels(groups[:noOfBars])
	ax.set_xticklabels([])
	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')
	mplt.yticks(fontsize=ticksFontSZ)
	ax.set_ylabel("% of total jobs which crossed Threshold", fontweight=labelFontWT, fontsize=ticksFontSZ)
	ax.set_xlabel("Top "+str(noOfBars)+" AppGroup", fontweight=labelFontWT, fontsize=ticksFontSZ)
        fig = matplotlib.pyplot.gcf()
	#mplt.legend( (bottomBar[0], topBar[1]), ("% of Jobs < Threshold", "% of Jobs > Threshold") )
	fig.set_size_inches(ImgWidth, ImgHeight)
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)
	'''
	return
'''
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
	ax.set_ylabel("No of jobs > Threshold of peak major page fault", fontweight=labelFontWT, fontsize=ticksFontSZ)
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
	ax.set_ylabel("% of jobs > Threshold", fontweight=labelFontWT, fontsize=ticksFontSZ)
	ax.set_xlabel("Top "+str(noOfBars)+"app groups", fontweight=labelFontWT, fontsize=ticksFontSZ)
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)
		
	return 
'''

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
	filename = "500TAppGroupVsUniqUsers.png"
	fig, ax = mplt.subplots()
	indices = np.arange(0, noOfBars*0.3, 0.3)

	ax.bar(indices,noOfUniqUsers[:noOfBars], bar_width/2, color=blue, linewidth=outlinewgt[-1])
	ax.set_xticks(indices+ 0.5*bar_width/2)
	ax.set_xticklabels([])
	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')
	mplt.yticks(fontsize=ticksFontSZ)
	ax.set_ylabel("No of unique users", fontsize=labelFontSZ, )
	ax.set_xlabel("Top"+ str(noOfBars) +"App groups", fontweight=labelFontWT, fontsize=labelFontSZ)
        fig = matplotlib.pyplot.gcf()
	plt.tick_params(
		axis  ='both',       # changes apply to the x-axis
		which ='both',      # both major and minor ticks are affected
    		bottom='off',      # ticks along the bottom edge are off
    		top   ='off',         # ticks along the top edge are off
		right ='off',	   # ticks along the left edge are off
		left  ='off')        # ticks along the right edge are off
	fig.set_size_inches(ImgWidth, ImgHeight)
	#mplt.setp(plt.gca().get_legend().get_texts(), fontsize=legendFontSZ)
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
	filename = "500TAppGroupVsNJobs.png"
	fig, ax = mplt.subplots()
	indices = np.arange(0, noOfBars*0.3, 0.3)

	ax.bar(indices, nJobs[:noOfBars], bar_width/2.0, color=blue, linewidth=outlinewgt[-1])
	ax.set_xticks(indices+ 0.5*bar_width/2.0)
	ax.set_xticklabels([])
	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')
	mplt.yticks(fontsize=ticksFontSZ)
	
	ax.set_ylabel("No of jobs", fontweight=labelFontWT, fontsize=labelFontSZ)
	ax.set_xlabel("Top "+ str(noOfBars) +" App groups", fontweight=labelFontWT, fontsize=labelFontSZ)
	plt.tick_params(
		axis  ='both',       # changes apply to the x-axis
		which ='both',      # both major and minor ticks are affected
    		bottom='off',      # ticks along the bottom edge are off
    		top   ='off',         # ticks along the top edge are off
		right ='off',	   # ticks along the left edge are off
		left  ='off')        # ticks along the right edge are off
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	#mplt.setp(plt.gca().get_legend().get_texts(), fontsize=legendFontSZ)
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)

	return 	
