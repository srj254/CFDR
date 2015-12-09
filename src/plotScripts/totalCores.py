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

outlinewgt	= [1 , 1 , 1 , 1 , 1  , 1 , 1 , 0.5]

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
# Total Cores on X Axis
def labelBar(axis, bar, bottombar, text, factor):
	ht = bar.get_height()
	if bottombar is not None:
		ht += bottombar.get_height()
	axis.text(bar.get_x()+bar.get_width()/2.0, (1.02+factor)*ht, ' '+text,
                ha='center', va='bottom', fontsize=10, )
	return
'''
# Percentage of Jobs requesting certain number of Cores
def coresVsJobs(df):
	'''
	roi_df = df[['totalCores', 'Thrashing']]
	roi_df = roi_df[(roi_df['Thrashing'] == True)]
	
	totalCores = (df['totalCores'].values.tolist())
	thrashingCores = roi_df['totalCores'].values.tolist()

	ziplist = []
	for coreNo in list(set(totalCores)):
		totFltCorePcnt	= (float(thrashingCores.count(coreNo))/float(totalCores.count(coreNo)))*100
		totCorePcnt	= (float(totalCores.count(coreNo))/float(len(totalCores)))*100
		
		pcnt = (totCorePcnt * totFltCorePcnt)/100.00
		ziplist.append((coreNo, totCorePcnt, pcnt, totCorePcnt-pcnt))
	coreNo, totalpcnt, bottompcnt, topPcnt = zip(*sorted(ziplist, key=lambda x: x[1], reverse=True))

	noOfBars = 30
	filename = "500TTotalCoresVSJobs_Percentages.png"
	fig, ax = mplt.subplots()
	indices = np.arange(0, 0.3*noOfBars, 0.3)
	bottomBar = ax.bar(indices, bottompcnt[:noOfBars], bar_width, color=blue, linewidth=outlinewgt[-1], hatch='////')
	topBar    = ax.bar(indices, topPcnt[:noOfBars], bar_width, bottom=bottompcnt[:noOfBars], color=lightblue, linewidth=outlinewgt[-1], hatch="////")

	ax.set_xticks(indices + 0.5*(bar_width))
	ax.set_xticklabels(coreNo[:noOfBars])
	ax.set_xlabel('Total Cores', fontsize=labelFontSZ, fontweight=labelFontWT)
	ax.set_ylabel('% of jobs', fontsize=labelFontSZ, fontweight=labelFontWT)

        ax.text(ImgNoteX, ImgNoteY, 'Threshold: Peak major page fault > 500', \
                horizontalalignment='center', \
                verticalalignment='center', \
                transform=ax.transAxes, fontsize=ticksFontSZ, fontweight=labelFontWT)

	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')	
	mplt.yticks(fontsize=ticksFontSZ)	
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	mplt.legend( (bottomBar[1], topBar[0]), ("% of Job > Threshold", "% of Jobs < Threshold"))
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)
	'''

	# Second plot
	roi_df = df[['totalCores', 'Thrashing']]
	totalCores = (df['totalCores'].values.tolist())
	roi_df = roi_df[(roi_df['Thrashing'] == True)]
	thrashingCores = roi_df['totalCores'].values.tolist()

	ziplist = []
	for coreNo in list(set(totalCores)):
		totFltCoreCnt	= thrashingCores.count(coreNo)
		totCoreCnt	= totalCores.count(coreNo)
		ziplist.append((coreNo, totCoreCnt, totFltCoreCnt, totCoreCnt-totFltCoreCnt))
	coreNo, totalCnt, bottomCnt, topCnt = zip(*sorted(ziplist, key=lambda x: x[1], reverse=True))

	noOfBars  = 20
	filename  = "500TTotalCoresVSJobs_RawNumbers.png"
	fig, ax   = mplt.subplots()
	indices   = np.arange(0, 0.3*noOfBars, 0.3)
	
	topBar    = ax.bar(indices, totalCnt[:noOfBars], bar_width, \
			   color=yellow, linewidth=outlinewgt[-1])# hatch="/")
	bottomBar = ax.bar(indices, bottomCnt[:noOfBars], 0.75*bar_width, \
			   color=red, linewidth=outlinewgt[-1])# hatch='/')

	for i in range(5):
		s = labelBar.labelBar(ax, topBar[i], None, \
			 str(int(float(totalCnt[i])*100.00/len(totalCores)))+'%', 0.03, 0)
		if s == 0:
			continue
		labelBar.labelBar(ax, bottomBar[i], None, \
			 str(int(float(bottomCnt[i])*100.00/totalCnt[i]))+'%', 0.0, 1)

	ax.set_xticks(indices + 0.5*(bar_width))
	ax.set_xticklabels(coreNo[:noOfBars])
	ax.set_xlabel('Total Cores', fontsize=labelFontSZ, fontweight=labelFontWT)
	ax.set_ylabel('No of jobs', fontsize=labelFontSZ, fontweight=labelFontWT)

	plt.tick_params(
		axis  ='both',       # changes apply to the x-axis
		which ='both',      # both major and minor ticks are affected
    		bottom='off',      # ticks along the bottom edge are off
    		top   ='off',         # ticks along the top edge are off
		right ='off',	   # ticks along the left edge are off
		left  ='off')        # ticks along the right edge are off
        #ax.text(ImgNoteX, ImgNoteY, 'Threshold: Peak major page fault > 500', \
        #        horizontalalignment='center', \
        #        verticalalignment='center', \
        #        transform=ax.transAxes, fontsize=ticksFontSZ, fontweight=labelFontWT)

	mplt.xticks(fontsize=ticksFontSZ, rotation=70)	
	mplt.yticks(fontsize=ticksFontSZ)	
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	mplt.legend( (bottomBar[0], topBar[0]), ("No of jobs > Threshold", "No of jobs"))
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)
	'''
	# Third Plot
	roi_df = df[['totalCores', 'Thrashing']]
	roi_df = roi_df[(roi_df['Thrashing'] == True)]
	
	totalCores = (df['totalCores'].values.tolist())
	thrashingCores = roi_df['totalCores'].values.tolist()

	ziplist = []
	for coreNo in list(set(totalCores)):
		totFltCoreCnt	= thrashingCores.count(coreNo)
		totCoreCnt	= totalCores.count(coreNo)
		ziplist.append((coreNo, totCoreCnt, totFltCoreCnt, totCoreCnt-totFltCoreCnt))
	coreNo, totalCnt, bottomCnt, topCnt = zip(*sorted(ziplist, key=lambda x: x[2], reverse=True))

	noOfBars  = 30
	filename  = "500TTotalCoresVSNoOfFaultyJobs.png"
	fig, ax   = mplt.subplots()
	indices   = np.arange(0, 0.3*noOfBars, 0.3)
	bottomBar = ax.bar(indices, bottomCnt[:noOfBars], bar_width, color=blue, linewidth=outlinewgt[-1], hatch='////')
	#topBar    = ax.bar(indices, topCnt[:noOfBars], bar_width, bottom=bottomCnt[:noOfBars], color=lightblue, linewidth=outlinewgt[-1], hatch="////")

	ax.set_xticks(indices + 0.5*(bar_width))
	ax.set_xticklabels(coreNo[:noOfBars])
	ax.set_xlabel('Total Cores', fontsize=labelFontSZ, fontweight=labelFontWT)
	ax.set_ylabel('Number of jobs > Threshold', fontsize=labelFontSZ, fontweight=labelFontWT)

        ax.text(ImgNoteX, ImgNoteY, 'Threshold: Peak major page fault > 500', \
                horizontalalignment='center', \
                verticalalignment='center', \
                transform=ax.transAxes, fontsize=ticksFontSZ, fontweight=labelFontWT)

	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')	
	mplt.yticks(fontsize=ticksFontSZ)	
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	#mplt.legend( (bottomBar[1], topBar[0]), ("No of Job > Threshold", "No of Jobs < Threshold"))
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)

	# Fourth Plot
	roi_df = df[['totalCores', 'Thrashing']]
	roi_df = roi_df[(roi_df['Thrashing'] == True)]
	
	totalCores = (df['totalCores'].values.tolist())
	thrashingCores = roi_df['totalCores'].values.tolist()

	ziplist = []
	for coreNo in list(set(totalCores)):
		totFltCorePcnt	= (float(thrashingCores.count(coreNo))/float(totalCores.count(coreNo)))*100
		totCorePcnt	= (float(totalCores.count(coreNo))/float(len(totalCores)))*100
		
		pcnt = (totCorePcnt * totFltCorePcnt)/100.00
		ziplist.append((coreNo, totCorePcnt, pcnt, totCorePcnt-pcnt))
	coreNo, totalpcnt, bottompcnt, topPcnt = zip(*sorted(ziplist, key=lambda x: x[2], reverse=True))

	noOfBars = 30
	filename = "500TTotalCoresVSPcntOfTotCoresFaultyJobs.png"
	fig, ax = mplt.subplots()
	indices = np.arange(0, 0.3*noOfBars, 0.3)
	bottomBar = ax.bar(indices, bottompcnt[:noOfBars], bar_width, color=blue, linewidth=outlinewgt[-1], hatch='////')
	#topBar    = ax.bar(indices, topPcnt[:noOfBars], bar_width, bottom=bottompcnt[:noOfBars], color=lightblue, linewidth=outlinewgt[-1], hatch="////")

	ax.set_xticks(indices + 0.5*(bar_width))
	ax.set_xticklabels(coreNo[:noOfBars])
	ax.set_xlabel('Total Cores', fontsize=labelFontSZ, fontweight=labelFontWT)
	ax.set_ylabel('% of jobs of TotalCore > Threshold', fontsize=labelFontSZ, fontweight=labelFontWT)

        ax.text(ImgNoteX, ImgNoteY, 'Threshold: Peak major page fault > 500', \
                horizontalalignment='center', \
                verticalalignment='center', \
                transform=ax.transAxes, fontsize=ticksFontSZ, fontweight=labelFontWT)

	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')	
	mplt.yticks(fontsize=ticksFontSZ)	
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	#mplt.legend( (bottomBar[1], topBar[0]), ("% of Job > Threshold", "% of Jobs < Threshold"))
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)

	# Fifth Plot
	roi_df = df[['totalCores', 'Thrashing']]
	roi_df = roi_df[(roi_df['Thrashing'] == True)]
	
	totalCores = (df['totalCores'].values.tolist())
	thrashingCores = roi_df['totalCores'].values.tolist()

	ziplist = []
	for coreNo in list(set(totalCores)):
		totFltCorePcnt	= (float(thrashingCores.count(coreNo))/float(totalCores.count(coreNo)))*100
		totCorePcnt	= (float(totalCores.count(coreNo))/float(len(totalCores)))*100
		
		pcnt = (totCorePcnt * totFltCorePcnt)/100.00
		ziplist.append((coreNo, totCorePcnt, pcnt, totCorePcnt-pcnt))
	coreNo, totalpcnt, bottompcnt, topPcnt = zip(*sorted(ziplist, key=lambda x: x[2], reverse=True))

	noOfBars = 30
	filename = "500TTotalCoresVSPcntOfFaultyJobsOfTotalCores.png"
	fig, ax = mplt.subplots()
	indices = np.arange(0, 0.3*noOfBars, 0.3)
	bottomBar = ax.bar(indices, bottompcnt[:noOfBars], bar_width, color=blue, linewidth=outlinewgt[-1], hatch='////')
	#topBar    = ax.bar(indices, topPcnt[:noOfBars], bar_width, bottom=bottompcnt[:noOfBars], color=lightblue, linewidth=outlinewgt[-1], hatch="////")

	ax.set_xticks(indices + 0.5*(bar_width))
	ax.set_xticklabels(coreNo[:noOfBars])
	ax.set_xlabel('Total Cores', fontsize=labelFontSZ, fontweight=labelFontWT)
	ax.set_ylabel('% of jobs > Threshold (For each TotalCores)', fontsize=labelFontSZ, fontweight=labelFontWT)

        ax.text(ImgNoteX, ImgNoteY, 'Threshold: Peak major page fault > 500', \
                horizontalalignment='center', \
                verticalalignment='center', \
                transform=ax.transAxes, fontsize=ticksFontSZ, fontweight=labelFontWT)

	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')	
	mplt.yticks(fontsize=ticksFontSZ)	
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	#mplt.legend( (bottomBar[1], topBar[0]), ("% of Job > Threshold", "% of Jobs < Threshold"))
	mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)

	return
'''
