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
from   collections import Counter

patterns	= [ '', '', '','/','\\','o','.','' ]
outlinewgt	= [ 1 , 1 , 1 , 1 , 1  , 1 , 1 , 1.5 ]

gray = 0.5
red  = 'r'
green= 'g'
blue = 'b'
black= 'k'
white= 'w'
lightblue = 'lightblue'

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
ImgDPI		= 600
ImgWidth	= 18.5
ImgHeight	= 10.5
ImgProp		= 'tight'
ImgNoteX	= 0.80
ImgNoteY	= 0.85

def extractUserInfo(df, fakeUname):
	# First Plot
	userTable 	= df[df['user'] == fakename]
	majPgFltTable 	= userTable[userTable['Thrashing'] == True]
	majPgFltTable	= pd.DataFrame.sort(majPgFltTable, columns="start")
	majPgFltTable['date'] = ['']*len(majPgFltTable['start'].values.tolist())

	for index, row in majPgFltTable.iterrows():
		majPgFltTable.ix[index, 'date'] = str(date.fromtimestamp(majPgFltTable.ix[index, 'start']))

	labels, values = zip(*Counter(majPgFltTable['date']).items())
	ind = np.arange(len(labels))

	mplt.bar(ind, values, bar_width)
	xticklabels = list(labels)
	for idx, tick in enumerate(xticklabels):
		if (idx%2) != 0:
			xticklabels[idx] = ''
	
	mplt.xticks(ind + bar_width* 0.5, xticklabels, rotation='vertical')
	mplt.savefig(sys.argv[2]+"/500T"+fakename+"_FaultyJobs.png", format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)

	# Second Plot
	userTable 	= df[df['user'] == fakename]
	majPgFltTable	= userTable
	majPgFltTable	= pd.DataFrame.sort(majPgFltTable, columns="start")
	majPgFltTable['date'] = ['']*len(majPgFltTable['start'].values.tolist())

	for index, row in majPgFltTable.iterrows():
		majPgFltTable.ix[index, 'date'] = str(date.fromtimestamp(majPgFltTable.ix[index, 'start']))

	labels, values = zip(*Counter(majPgFltTable['date']).items())
	
	ind = np.arange(len(labels))
	width = 0.3

	mplt.bar(ind, values, width)
	xticklabels = list(labels)
	for idx, tick in enumerate(xticklabels):
		if (idx%2) != 0:
			xticklabels[idx] = ''
	
	mplt.xticks(ind + width * 0.5, xticklabels, rotation='vertical')			
	mplt.savefig(sys.argv[2]+"/500T"+fakename+"_AllJobs.png", format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)

	#Third Plot
	userTable 	= df[df['user'] == fakename]
	majPgFltTable	= userTable
	totalCoresAllJobs = majPgFltTable['totalCores'].values.tolist()
	#print len(totalCoresAllJobs)	

	majPgFltTable 	= userTable[userTable['Thrashing'] == True]
	totalCoresFltJobs = majPgFltTable['totalCores'].values.tolist()

	ziplist = []
	for coreNo in list(set(totalCoresAllJobs)):
		ziplist.append((coreNo, (totalCoresAllJobs.count(coreNo)), (totalCoresFltJobs.count(coreNo)),\
				 (totalCoresAllJobs.count(coreNo))-(totalCoresFltJobs.count(coreNo))))
	coreNo, totalCnt, bottomCnt, topCnt = zip(*sorted(ziplist, key=lambda x: x[0], reverse=True))
	
	noOfBars = len(coreNo)
	filename = "500T"+fakename+"_Usage.png"
	fig, ax = mplt.subplots()
	indices = np.arange(0, noOfBars*0.3, 0.3)

	bottomBar = ax.bar(indices, bottomCnt[:noOfBars], bar_width, color=blue, \
			   linewidth=outlinewgt[-1], hatch='/')
	topBar    = ax.bar(indices, topCnt[:noOfBars], bar_width, \
			   bottom=bottomCnt[:noOfBars], color=lightblue, \
			   linewidth=outlinewgt[-1], hatch='////')

	ax.text(ImgNoteX, ImgNoteY, 'Threshold: Peak major page fault > 500', \
		horizontalalignment='center', \
		verticalalignment='center', \
		transform=ax.transAxes, fontsize=ticksFontSZ, fontweight=labelFontWT)

	ax.set_xticks(indices+ 0.5*bar_width)
	ax.set_xticklabels(coreNo[:noOfBars])
	mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')
	mplt.yticks(fontsize=ticksFontSZ)
	ax.set_ylabel("Number of jobs", fontweight=labelFontWT, fontsize=ticksFontSZ)
	ax.set_xlabel("Total Cores", fontweight=labelFontWT, fontsize=ticksFontSZ)		
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(ImgWidth, ImgHeight)
	mplt.legend((bottomBar[0], topBar[0]), ("No of Jobs > Threshold", "No of Jobs < Threshold"))
	mplt.savefig(sys.argv[2]+"/"+filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)
	
	return  

if __name__ == "__main__":
	if len(sys.argv) != 5:
		print "Usage: ./<script> <Accounting Statistics> <Userplots Path> [..Options..]"
		print "Options"
		print "-f <fakename>"
		print "-r <realName>"
		exit()

	if (sys.argv[3] != '-f') and (sys.argv[3] != "-r"):
		print "Usage: ./<script> <Accounting Statistics> <Userplots>[..Options..]"
		print "Options"
		print "-f <fakename>"
		print "-r <realName>"
		exit()
 
	df  = pd.io.parsers.read_csv(sys.argv[1], sep='\t')
	#print (list(set(df['user'].values.tolist())))
	#print (list(set(df['OriginalUser'].values.tolist())))
	
	if (sys.argv[3] == '-r'):
		fakename = df[df['OriginalUser'] == sys.argv[4]]

		if len(list(set(fakename['user'].values.tolist()))) != 1:
			print "Something wrong in the table for ", \
				list(set(fakename['user'].values.tolist())), \
				"One fake username", sys.argv[4]
			exit()

		fakename = (fakename.values.tolist())[0]
		print fakename
	else:
		fakename = sys.argv[4]
		
	extractUserInfo(df, fakename)
