#!/usr/bin/python
# JobDensity on X Axis
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
red  = 'r'
green= 'g'
blue = 'b'
black= 'k'
white= 'w'
yellow='y'
lightblue = 'lightblue'

outlinewgt	= [ 1 , 1 , 1 , 1 , 1  , 1 , 1 , 0.5]

bar_width	= 0.25
barSpacing	= 0.05

xlabelFontSZ	= 14
ylabelFontSZ	= 14
labelFontSZ	= 14
legendFontSZ	= 12

xticksFontSZ	= 10
yticksFontSZ	= 10
ticksFontSZ	= 10

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

def jobDensityVsJobs(mydf):
	'''
	# Filtering Data
	df = mydf[(mydf['Resource_List.naccesspolicy'] == "shared") | (mydf['Resource_List.naccesspolicy'] == "share")]
	df = df[(df['end'] - df['start']) >=30 ]

	for jobGrp in list(set(df['JobGrp'].values.tolist())):
		dt = df[(df['JobGrp'] == jobGrp)]
		if np.amax(dt['PeakPgFlt'].values.tolist()) < 50:
			df = df[(df['JobGrp'] != jobGrp)]
	
	roi_df    = df[['jobDensity', 'Thrashing']]
	jdensity  = roi_df['jobDensity'].values.tolist()
	roi_df    = roi_df[roi_df['Thrashing'] == True]
	jDensityFaulty = roi_df['jobDensity'].values.tolist()
	
	ziplist = []
	for number in list(set(jdensity)):
		total    = float(len(jdensity))
		normCnt  = float(jdensity.count(number))
		fltCnt   = float(jDensityFaulty.count(number))
		fltPcnt  = fltCnt*100.00/normCnt
		normPcnt = normCnt*100.00/total
		ziplist.append((number, normPcnt, normPcnt*fltPcnt/100.00, (normPcnt - normPcnt*fltPcnt/100.00)))

	jDnsTicks, normPcnt, bottomPcnt, topPcnt = zip(*sorted(ziplist, key=lambda x: x[0]))

	jDnsTicks = [(item/100) for item in jDnsTicks]	
	noOfBars = len(list(set(jDnsTicks)))
	filename = "500TJobDensityVsJobs_Percentages.png"
	fig, ax = mplt.subplots()
	indices = np.arange(0, noOfBars*0.3, 0.3)

	topBar    = ax.bar(indices[:noOfBars], normPcnt[:noOfBars], bar_width, \
			   color=lightblue, \
			   linewidth=outlinewgt[-1], hatch='/')
	bottomBar = ax.bar(indices[:noOfBars] + 0.25, bottomPcnt[:noOfBars], 0.5*bar_width, color=blue, \
			   linewidth=outlinewgt[-1], hatch='/')

	#ax.text(ImgNoteX, ImgNoteY, 'Threshold: Peak major page fault > 500', \
	#	horizontalalignment='center', \
	#	verticalalignment='center', \
	#	transform=ax.transAxes, fontsize=ticksFontSZ, fontweight=labelFontWT)
	for i  in range(5):
		labelBar(ax, topBar[i], None, str(int(float(normPcnt)))+'%')

	ax.set_xticks(indices+ 0.5*bar_width)
	ax.set_xticklabels(jDnsTicks[:noOfBars])
	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')
	mplt.yticks(fontsize=ticksFontSZ)

	ax.set_ylabel("% of jobs > Threshold", fontweight=labelFontWT, fontsize=ticksFontSZ)
	ax.set_xlabel("ppn (shared)", fontweight=labelFontWT, fontsize=ticksFontSZ)		
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	# mplt.legend((bottomBar[0], topBar[0]), ("% of Jobs < Threshold", "% of Jobs > Threshold"))
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)
	'''
	# Filtering Data
	df = mydf[(mydf['Resource_List.naccesspolicy'] == "shared") | (mydf['Resource_List.naccesspolicy'] == "share")]
	df = df[(df['end'] - df['start']) >=30 ]

	for jobGrp in list(set(df['JobGrp'].values.tolist())):
		dt = df[(df['JobGrp'] == jobGrp)]
		if np.amax(dt['PeakPgFlt'].values.tolist()) < 50:
			df = df[(df['JobGrp'] != jobGrp)]
	
	roi_df    = df[['jobDensity', 'Thrashing']]
	jdensity  = roi_df['jobDensity'].values.tolist()
	roi_df    = roi_df[roi_df['Thrashing'] == True]
	jDensityFaulty = roi_df['jobDensity'].values.tolist()
	
	ziplist = []
	for number in list(set(jdensity)):
		total    = (len(jdensity))
		normCnt  = (jdensity.count(number))
		fltCnt   = (jDensityFaulty.count(number))
		#fltPcnt  = fltCnt*100.00/normCnt
		#normPcnt = normCnt*100.00/total
		ziplist.append((number, normCnt, fltCnt, normCnt-fltCnt))

	jDnsTicks, normCnt, bottomCnt, topCnt = zip(*sorted(ziplist, key=lambda x: x[0]))

	jDnsTicks = [(item/100) for item in jDnsTicks]	
	noOfBars = len(list(set(jDnsTicks)))
	filename = "500TJobDensityVsJobs_RawNumbers.png"
	fig, ax = mplt.subplots()
	indices = np.arange(0, noOfBars*0.3, 0.3)

	topBar    = ax.bar(indices[:noOfBars], normCnt[:noOfBars], bar_width, \
			   color=yellow, \
			   linewidth=outlinewgt[-1])# hatch='/')
	bottomBar = ax.bar(indices[:noOfBars], bottomCnt[:noOfBars], 0.75*bar_width, color=red, \
			   linewidth=outlinewgt[-1])#, hatch='/')
	for i in range(5):
		labelBar.labelBar(ax, topBar[i], None, \
			 str(int(float(normCnt[i])*100.00/len(jdensity)))+'%', 0.03, 0)
		labelBar.labelBar(ax, bottomBar[i], None, \
			 str(int(float(bottomCnt[i])*100.00/normCnt[i]))+'%', 0, 0)

	#ax.text(ImgNoteX, ImgNoteY, 'Threshold: Peak major page fault > 500', \
	#	horizontalalignment='center', \
	#	verticalalignment='center', \
	#	transform=ax.transAxes, fontsize=ticksFontSZ, fontweight=labelFontWT)

	ax.set_xticks(indices+ 0.5*bar_width)
	ax.set_xticklabels(jDnsTicks[:noOfBars])
	mplt.xticks(fontsize=ticksFontSZ)
	mplt.yticks(fontsize=ticksFontSZ)
	plt.tick_params(
		axis  ='both',       # changes apply to the x-axis
		which ='both',      # both major and minor ticks are affected
    		bottom='off',      # ticks along the bottom edge are off
    		top   ='off',         # ticks along the top edge are off
		right ='off',	   # ticks along the left edge are off
		left  ='off')        # ticks along the right edge are off
	ax.set_ylabel("No. of jobs", fontweight=labelFontWT, fontsize=labelFontSZ)
	ax.set_xlabel("ppn (shared jobs)", fontweight=labelFontWT, fontsize=labelFontSZ)		
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	mplt.legend((bottomBar[0], topBar[0]), ("No. of jobs > Threshold", "No. of jobs"))
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)
	
	'''
	# Filtering Data
	df = mydf[(mydf['Resource_List.naccesspolicy'] == "shared") | (mydf['Resource_List.naccesspolicy'] == "share")]
	df = df[(df['end'] - df['start']) >=30 ]

	for jobGrp in list(set(df['JobGrp'].values.tolist())):
		dt = df[(df['JobGrp'] == jobGrp)]
		if np.amax(dt['PeakPgFlt'].values.tolist()) < 50:
			df = df[(df['JobGrp'] != jobGrp)]
	
	roi_df    = df[['jobDensity', 'Thrashing']]
	jdensity  = roi_df['jobDensity'].values.tolist()
	roi_df    = roi_df[roi_df['Thrashing'] == True]
	jDensityFaulty = roi_df['jobDensity'].values.tolist()
	
	ziplist = []
	for number in list(set(jdensity)):
		total    = float(len(jdensity))
		normCnt  = float(jdensity.count(number))
		fltCnt   = float(jDensityFaulty.count(number))
		fltPcnt  = fltCnt*100.00/normCnt
		normPcnt = normCnt*100.00/total
		ziplist.append((number, normPcnt, normPcnt*fltPcnt/100.00, (normPcnt - normPcnt*fltPcnt/100.00)))

	jDnsTicks, normPcnt, bottomPcnt, topPcnt = zip(*sorted(ziplist, key=lambda x: x[2], reverse=True))

	jDnsTicks= [(item/100) for item in jDnsTicks]	
	noOfBars = len(list(set(jDnsTicks)))
	filename = "500TJobDensityVsPcntOfJDnstysFaultyJobs.png"
	fig, ax  = mplt.subplots()
	indices  = np.arange(0, noOfBars*0.3, 0.3)

	bottomBar = ax.bar(indices[:noOfBars], bottomPcnt[:noOfBars], bar_width, color=blue, \
			   linewidth=outlinewgt[-1], hatch='/')
	#topBar   = ax.bar(indices[:noOfBars], topPcnt[:noOfBars], bar_width, \
	#		   bottom=bottomPcnt[:noOfBars], color=lightblue, \
	#		   linewidth=outlinewgt[-1], hatch='/')

	ax.text(ImgNoteX, ImgNoteY, 'Threshold: Peak major page fault > 500', \
		horizontalalignment='center', \
		verticalalignment='center', \
		transform=ax.transAxes, fontsize=ticksFontSZ, fontweight=labelFontWT)

	ax.set_xticks(indices+ 0.5*bar_width)
	ax.set_xticklabels(jDnsTicks[:noOfBars])
	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')
	mplt.yticks(fontsize=ticksFontSZ)
	
	ax.set_ylabel("% of jobs of each jobDensity > Threshold", fontweight=labelFontWT, fontsize=ticksFontSZ)
	ax.set_xlabel("ppn (shared)", fontweight=labelFontWT, fontsize=ticksFontSZ)		
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	# mplt.legend((bottomBar[0], topBar[0]), ("% of Jobs < Threshold", "% of Jobs > Threshold"))
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)
	'''
	'''
	# Filtering Data
	df = mydf[(mydf['Resource_List.naccesspolicy'] == "shared") | (mydf['Resource_List.naccesspolicy'] == "share")]
	df = df[(df['end'] - df['start']) >=30 ]

	for jobGrp in list(set(df['JobGrp'].values.tolist())):
		dt = df[(df['JobGrp'] == jobGrp)]
		if np.amax(dt['PeakPgFlt'].values.tolist()) < 50:
			df = df[(df['JobGrp'] != jobGrp)]
	
	roi_df    = df[['jobDensity', 'Thrashing']]
	jdensity  = roi_df['jobDensity'].values.tolist()
	roi_df    = roi_df[roi_df['Thrashing'] == True]
	jDensityFaulty = roi_df['jobDensity'].values.tolist()
	
	ziplist = []
	for number in list(set(jdensity)):
		total    = float(len(jdensity))
		normCnt  = float(jdensity.count(number))
		fltCnt   = float(jDensityFaulty.count(number))
		fltPcnt  = fltCnt*100.00/total
		normPcnt = normCnt*100.00/total
		ziplist.append((number, normPcnt, fltPcnt))

	jDnsTicks, normPcnt, bottomPcnt = zip(*sorted(ziplist, key=lambda x: x[2], reverse=True))

	jDnsTicks= [(item/100) for item in jDnsTicks]	
	noOfBars = len(list(set(jDnsTicks)))
	filename = "500TJobDensityVsPcntOfFaultyJobsOfJDnsty.png"
	fig, ax  = mplt.subplots()
	indices  = np.arange(0, noOfBars*0.3, 0.3)

	bottomBar = ax.bar(indices[:noOfBars], bottomPcnt[:noOfBars], bar_width, color=blue, \
			   linewidth=outlinewgt[-1], hatch='/')
	#topBar   = ax.bar(indices[:noOfBars], topPcnt[:noOfBars], bar_width, \
	#		   bottom=bottomPcnt[:noOfBars], color=lightblue, \
	#		   linewidth=outlinewgt[-1], hatch='/')

	ax.text(ImgNoteX, ImgNoteY, 'Threshold: Peak major page fault > 500', \
		horizontalalignment='center', \
		verticalalignment='center', \
		transform=ax.transAxes, fontsize=ticksFontSZ, fontweight=labelFontWT)

	ax.set_xticks(indices+ 0.5*bar_width)
	ax.set_xticklabels(jDnsTicks[:noOfBars])
	
	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')
	mplt.yticks(fontsize=ticksFontSZ)
	ax.set_ylabel("% out of total jobs > Threshold", fontweight=labelFontWT, fontsize=ticksFontSZ)
	ax.set_xlabel("ppn (shared)", fontweight=labelFontWT, fontsize=ticksFontSZ)		
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	# mplt.legend((bottomBar[0], topBar[0]), ("% of Jobs < Threshold", "% of Jobs > Threshold"))
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)
	'''
#return
#def jobDensityVsJobs(mydf):
	'''
	#Filtering Data
	df = mydf[(mydf['Resource_List.naccesspolicy'] != "shared") & (mydf['Resource_List.naccesspolicy'] != "share")]
	df = df[(df['end'] - df['start']) >=30 ]

	for jobGrp in list(set(df['JobGrp'].values.tolist())):
		dt = df[(df['JobGrp'] == jobGrp)]
		if np.amax(dt['PeakPgFlt'].values.tolist()) < 50:
			df = df[(df['JobGrp'] != jobGrp)]
	
	roi_df    = df[['jobDensity', 'Thrashing']]
	jdensity  = roi_df['jobDensity'].values.tolist()
	roi_df    = roi_df[roi_df['Thrashing'] == True]
	jDensityFaulty = roi_df['jobDensity'].values.tolist()
	
	ziplist = []
	for number in list(set(jdensity)):
		total    = float(len(jdensity))
		normCnt  = float(jdensity.count(number))
		fltCnt   = float(jDensityFaulty.count(number))
		fltPcnt  = fltCnt*100.00/normCnt
		normPcnt = normCnt*100.00/total
		ziplist.append((number, normPcnt, normPcnt*fltPcnt/100.00, (normPcnt - normPcnt*fltPcnt/100.00)))

	jDnsTicks, normPcnt, bottomPcnt, topPcnt = zip(*sorted(ziplist, key=lambda x: x[0]))

	jDnsTicks = [(item/100) for item in jDnsTicks]	
	noOfBars = len(list(set(jDnsTicks)))
	filename = "500TNSJobDensityVsJobs_Percentages.png"
	fig, ax = mplt.subplots()
	indices = np.arange(0, noOfBars*0.3, 0.3)

	bottomBar = ax.bar(indices[:noOfBars], bottomPcnt[:noOfBars], bar_width, color=blue, \
			   linewidth=outlinewgt[-1], hatch='/')
	topBar    = ax.bar(indices[:noOfBars], topPcnt[:noOfBars], bar_width, \
			   bottom=bottomPcnt[:noOfBars], color=lightblue, \
			   linewidth=outlinewgt[-1], hatch='/')

	ax.text(ImgNoteX, ImgNoteY, 'Threshold: Peak major page fault > 500', \
		horizontalalignment='center', \
		verticalalignment='center', \
		transform=ax.transAxes, fontsize=ticksFontSZ, fontweight=labelFontWT)

	ax.set_xticks(indices+ 0.5*bar_width)
	ax.set_xticklabels(jDnsTicks[:noOfBars])
	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')
	mplt.yticks(fontsize=ticksFontSZ)
	ax.set_ylabel("% of jobs > Threshold", fontweight=labelFontWT, fontsize=ticksFontSZ)
	ax.set_xlabel("ppn (not shared)", fontweight=labelFontWT, fontsize=ticksFontSZ)		
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	# mplt.legend((bottomBar[0], topBar[0]), ("% of Jobs < Threshold", "% of Jobs > Threshold"))
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)
	'''

	# Filtering Data
	df = mydf[(mydf['Resource_List.naccesspolicy'] != "shared") & (mydf['Resource_List.naccesspolicy'] != "share")]
	df = df[(df['end'] - df['start']) >=30 ]

	for jobGrp in list(set(df['JobGrp'].values.tolist())):
		dt = df[(df['JobGrp'] == jobGrp)]
		if np.amax(dt['PeakPgFlt'].values.tolist()) < 50:
			df = df[(df['JobGrp'] != jobGrp)]
	
	roi_df    = df[['jobDensity', 'Thrashing']]
	jdensity  = roi_df['jobDensity'].values.tolist()
	roi_df    = roi_df[roi_df['Thrashing'] == True]
	jDensityFaulty = roi_df['jobDensity'].values.tolist()
	
	ziplist = []
	for number in list(set(jdensity)):
		total    = (len(jdensity))
		normCnt  = (jdensity.count(number))
		fltCnt   = (jDensityFaulty.count(number))
		#fltPcnt  = fltCnt*100.00/normCnt
		#normPcnt = normCnt*100.00/total
		ziplist.append((number, normCnt, fltCnt, normCnt-fltCnt))

	jDnsTicks, normCnt, bottomCnt, topCnt = zip(*sorted(ziplist, key=lambda x: x[0]))

	jDnsTicks = [(item/100) for item in jDnsTicks]	
	noOfBars = len(list(set(jDnsTicks)))
	filename = "500TNSJobDensityVsJobs_RawNumbers.png"
	fig, ax = mplt.subplots()
	indices = np.arange(0, noOfBars*0.3, 0.3)

	topBar    = ax.bar(indices[:noOfBars], topCnt[:noOfBars], bar_width, \
			   color=yellow, \
			   linewidth=outlinewgt[-1])# hatch='/')
	bottomBar = ax.bar(indices[:noOfBars], bottomCnt[:noOfBars], 0.75*bar_width, color=red, \
			   linewidth=outlinewgt[-1])#hatch='/')
	for i in range(noOfBars):
		labelBar.labelBar(ax, topBar[i], None, \
			 str(int(float(normCnt[i])*100.00/len(jdensity)))+'%', 0.03, 0)
		labelBar.labelBar(ax, bottomBar[i], None, \
			 str(int(float(bottomCnt[i])*100.00/normCnt[i]))+'%', 0.0, 0)

	#ax.text(ImgNoteX, ImgNoteY, 'Threshold: Peak major page fault > 500', \
	#	horizontalalignment='center', \
	#	verticalalignment='center', \
	#	transform=ax.transAxes, fontsize=ticksFontSZ, fontweight=labelFontWT)

	ax.set_xticks(indices+ 0.5*bar_width)
	ax.set_xticklabels(jDnsTicks[:noOfBars])
	mplt.xticks(fontsize=ticksFontSZ)
	mplt.yticks(fontsize=ticksFontSZ)
	plt.tick_params(
		axis  ='both',       # changes apply to the x-axis
		which ='both',      # both major and minor ticks are affected
    		bottom='off',      # ticks along the bottom edge are off
    		top   ='off',         # ticks along the top edge are off
		right ='off',	   # ticks along the left edge are off
		left  ='off')        # ticks along the right edge are off
	ax.set_ylabel("No. of jobs", fontweight=labelFontWT, fontsize=labelFontSZ)
	ax.set_xlabel("ppn (not shared jobs)", fontweight=labelFontWT, fontsize=labelFontSZ)		
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	mplt.legend((bottomBar[0], topBar[0]), ("No. of jobs > Threshold", "No. of jobs"), loc=2)
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)

	'''
	# Filtering Data
	df = mydf[(mydf['Resource_List.naccesspolicy'] != "shared") & (mydf['Resource_List.naccesspolicy'] != "share")]
	df = df[(df['end'] - df['start']) >=30 ]

	for jobGrp in list(set(df['JobGrp'].values.tolist())):
		dt = df[(df['JobGrp'] == jobGrp)]
		if np.amax(dt['PeakPgFlt'].values.tolist()) < 50:
			df = df[(df['JobGrp'] != jobGrp)]
	
	roi_df    = df[['jobDensity', 'Thrashing']]
	jdensity  = roi_df['jobDensity'].values.tolist()
	roi_df    = roi_df[roi_df['Thrashing'] == True]
	jDensityFaulty = roi_df['jobDensity'].values.tolist()
	
	ziplist = []
	for number in list(set(jdensity)):
		total    = float(len(jdensity))
		normCnt  = float(jdensity.count(number))
		fltCnt   = float(jDensityFaulty.count(number))
		fltPcnt  = fltCnt*100.00/normCnt
		normPcnt = normCnt*100.00/total
		ziplist.append((number, normPcnt, normPcnt*fltPcnt/100.00, (normPcnt - normPcnt*fltPcnt/100.00)))

	jDnsTicks, normPcnt, bottomPcnt, topPcnt = zip(*sorted(ziplist, key=lambda x: x[2], reverse=True))

	jDnsTicks= [(item/100) for item in jDnsTicks]	
	noOfBars = len(list(set(jDnsTicks)))
	filename = "500TNSJobDensityVsPcntOfJDnstysFaultyJobs.png"
	fig, ax  = mplt.subplots()
	indices  = np.arange(0, noOfBars*0.3, 0.3)

	bottomBar = ax.bar(indices[:noOfBars], bottomPcnt[:noOfBars], bar_width, color=blue, \
			   linewidth=outlinewgt[-1], hatch='/')
	#topBar   = ax.bar(indices[:noOfBars], topPcnt[:noOfBars], bar_width, \
	#		   bottom=bottomPcnt[:noOfBars], color=lightblue, \
	#		   linewidth=outlinewgt[-1], hatch='/')

	ax.text(ImgNoteX, ImgNoteY, 'Threshold: Peak major page fault > 500', \
		horizontalalignment='center', \
		verticalalignment='center', \
		transform=ax.transAxes, fontsize=ticksFontSZ, fontweight=labelFontWT)

	ax.set_xticks(indices+ 0.5*bar_width)
	ax.set_xticklabels(jDnsTicks[:noOfBars])
	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')
	mplt.yticks(fontsize=ticksFontSZ)
	ax.set_ylabel("% of jobs of each jobDensity > Threshold", fontweight=labelFontWT, fontsize=ticksFontSZ)
	ax.set_xlabel("ppn (not shared)", fontweight=labelFontWT, fontsize=ticksFontSZ)		
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	# mplt.legend((bottomBar[0], topBar[0]), ("% of Jobs < Threshold", "% of Jobs > Threshold"))
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)

	# Filtering Data
	df = mydf[(mydf['Resource_List.naccesspolicy'] != "shared") & (mydf['Resource_List.naccesspolicy'] != "share")]
	df = df[(df['end'] - df['start']) >=30 ]

	for jobGrp in list(set(df['JobGrp'].values.tolist())):
		dt = df[(df['JobGrp'] == jobGrp)]
		if np.amax(dt['PeakPgFlt'].values.tolist()) < 50:
			df = df[(df['JobGrp'] != jobGrp)]
	
	roi_df    = df[['jobDensity', 'Thrashing']]
	jdensity  = roi_df['jobDensity'].values.tolist()
	roi_df    = roi_df[roi_df['Thrashing'] == True]
	jDensityFaulty = roi_df['jobDensity'].values.tolist()
	
	ziplist = []
	for number in list(set(jdensity)):
		total    = float(len(jdensity))
		normCnt  = float(jdensity.count(number))
		fltCnt   = float(jDensityFaulty.count(number))
		fltPcnt  = fltCnt*100.00/total
		normPcnt = normCnt*100.00/total
		ziplist.append((number, normPcnt, fltPcnt))

	jDnsTicks, normPcnt, bottomPcnt = zip(*sorted(ziplist, key=lambda x: x[2], reverse=True))

	jDnsTicks= [(item/100) for item in jDnsTicks]	
	noOfBars = len(list(set(jDnsTicks)))
	filename = "500TNSJobDensityVsPcntOfFaultyJobsOfJDnsty.png"
	fig, ax  = mplt.subplots()
	indices  = np.arange(0, noOfBars*0.3, 0.3)

	bottomBar = ax.bar(indices[:noOfBars], bottomPcnt[:noOfBars], bar_width, color=blue, \
			   linewidth=outlinewgt[-1], hatch='/')
	#topBar   = ax.bar(indices[:noOfBars], topPcnt[:noOfBars], bar_width, \
	#		   bottom=bottomPcnt[:noOfBars], color=lightblue, \
	#		   linewidth=outlinewgt[-1], hatch='/')

	ax.text(ImgNoteX, ImgNoteY, 'Threshold: Peak major page fault > 500', \
		horizontalalignment='center', \
		verticalalignment='center', \
		transform=ax.transAxes, fontsize=ticksFontSZ, fontweight=labelFontWT)

	ax.set_xticks(indices+ 0.5*bar_width)
	ax.set_xticklabels(jDnsTicks[:noOfBars])
	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')
	mplt.yticks(fontsize=ticksFontSZ)
	ax.set_ylabel("% out of total jobs > Threshold", fontweight=labelFontWT, fontsize=ticksFontSZ)
	ax.set_xlabel("ppn (not shared)", fontweight=labelFontWT, fontsize=ticksFontSZ)		
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	# mplt.legend((bottomBar[0], topBar[0]), ("% of Jobs < Threshold", "% of Jobs > Threshold"))
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)
	'''
	return


'''	
def Newfunction_UNWANTED(df):
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
'''

