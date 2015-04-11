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

def jobDensityVsJobs(mydf):
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
	ax.set_xlabel("Top "+str(noOfBars)+" users", fontweight=labelFontWT, fontsize=ticksFontSZ)		
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	# mplt.legend((bottomBar[0], topBar[0]), ("% of Jobs < Threshold", "% of Jobs > Threshold"))
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)

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

	bottomBar = ax.bar(indices[:noOfBars], bottomCnt[:noOfBars], bar_width, color=blue, \
			   linewidth=outlinewgt[-1], hatch='/')
	topBar    = ax.bar(indices[:noOfBars], topCnt[:noOfBars], bar_width, \
			   bottom=bottomCnt[:noOfBars], color=lightblue, \
			   linewidth=outlinewgt[-1], hatch='/')

	ax.text(ImgNoteX, ImgNoteY, 'Threshold: Peak major page fault > 500', \
		horizontalalignment='center', \
		verticalalignment='center', \
		transform=ax.transAxes, fontsize=ticksFontSZ, fontweight=labelFontWT)

	ax.set_xticks(indices+ 0.5*bar_width)
	ax.set_xticklabels(jDnsTicks[:noOfBars])
	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')
	mplt.yticks(fontsize=ticksFontSZ)
	ax.set_ylabel("No of jobs > Threshold", fontweight=labelFontWT, fontsize=ticksFontSZ)
	ax.set_xlabel("Top "+str(noOfBars)+" users", fontweight=labelFontWT, fontsize=ticksFontSZ)		
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	# mplt.legend((bottomBar[0], topBar[0]), ("% of Jobs < Threshold", "% of Jobs > Threshold"))
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)

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
	ax.set_xlabel("Top "+str(noOfBars)+" users", fontweight=labelFontWT, fontsize=ticksFontSZ)		
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	# mplt.legend((bottomBar[0], topBar[0]), ("% of Jobs < Threshold", "% of Jobs > Threshold"))
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)

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
	ax.set_xlabel("Top "+str(noOfBars)+" users", fontweight=labelFontWT, fontsize=ticksFontSZ)		
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	# mplt.legend((bottomBar[0], topBar[0]), ("% of Jobs < Threshold", "% of Jobs > Threshold"))
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)

	return

'''	
def Newfunction(df):
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

