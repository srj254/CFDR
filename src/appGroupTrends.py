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
ImgDPI		= 500
ImgWidth	= 18.5
ImgHeight	= 10.5
ImgProp		= 'tight'
ImgNoteX	= 0.80
ImgNoteY	= 0.85

'''
Unnamed: 0      AvgPgFltJumps   Error_Path      Exit_status     JobID   JobStatus       LogTS   LoggerHostName  MajPgFlt        Output_Path     PeakPgFlt       Resource_List.gres      Resource_List.mem       Resource_List.naccesspolicy     Resource_List.ncpus     Resource_List.neednodes Resource_List.nodect    Resource_List.nodes     Resource_List.pmem      Resource_List.walltime  Thrashing       account avgMemInKB      avgPeakMemInKB  blkPeakReadInB  blkPeakWriteInB blkReadInB      blkWriteInB     ctime   end     etime   exec_host       group   ibPeakReadInB   ibPeakWriteInB  ibReadInB       ibWriteInB      jobDensity      jobname lltePeakReadInB lltePeakWriteInB        llteReadInB     llteWriteInB    majPgFltRate    owner   qtime   queue   resources_used.cput     resources_used.mem      resources_used.vmem     resources_used.walltime session start   totalCores      uniqHosts       user    JobGrp  OriginalUser
'''

def appGroupTrends(df):
	# Filter Data
	df = df[(df['JobGrp'] != "-NA-")]
	df = df[(df['Resource_List.naccesspolicy'] != "shared") & (df['Resource_List.naccesspolicy'] != "share")]
	df = df[(df['end'] - df['start']) >= 30]
	
	appGrp = list(set(df['JobGrp'].values.tolist()))

	for grpNum in appGrp:
		dtAppGrp = df[(df['JobGrp'] == grpNum)]
		plotAppGrpTrend(dtAppGrp, sys.argv[2])
	return 

def plotAppGrpTrend(df, path):
	totCoreReqs = list(set(df['totalCores'].values.tolist()))
	if len(totCoreReqs) < 3:
		return

	if len(list(set(df['JobGrp'].values.tolist()))) != 1:
		print "Wrong dataframe, all jobs should have same AppGroup"
		print list(set(df['JobGrp'].values.tolist()))
		return
	else:
		filename = str(list(set(df['JobGrp'].values.tolist()))[0])
		#print "Group: ", filename, " Cores list: ", totCoreReqs

	ziplist = []
	for coreReq in totCoreReqs:
		roi_df = df[df['totalCores'] == coreReq]
		#print coreReq
		avgMemInKB 	= np.mean(roi_df['avgMemInKB'].values.tolist())
		#print avgMemInKB
		avgPeakMemInKB	= np.mean(roi_df['avgPeakMemInKB'].values.tolist())
		#print avgPeakMemInKB
		blkPeakReadInB 	= np.mean(roi_df['blkPeakReadInB'].values.tolist())
		#print blkPeakReadInB
		blkPeakWriteInB	= np.mean(roi_df['blkPeakWriteInB'].values.tolist())
		#print blkPeakWriteInB
		blkReadInB 	= np.mean(roi_df['blkReadInB'].values.tolist())
		#print blkReadInB
		blkWriteInB 	= np.mean(roi_df['blkWriteInB'].values.tolist())
		#print blkWriteInB

		ibPeakReadInB	= np.mean(roi_df['ibPeakReadInB'].values.tolist())
		#print ibPeakReadInB
		ibPeakWriteInB	= np.mean(roi_df['ibPeakWriteInB'].values.tolist())
		#print ibPeakWriteInB
		ibReadInB	= np.mean(roi_df['ibReadInB'].values.tolist())
		#print ibReadInB
		ibWriteInB	= np.mean(roi_df['ibWriteInB'].values.tolist())
		#print ibWriteInB

		lltePeakReadInB = np.mean(roi_df['lltePeakReadInB'].values.tolist())
		#print lltePeakReadInB
		lltePeakWriteInB= np.mean(roi_df['lltePeakWriteInB'].values.tolist())
		#print lltePeakWriteInB
		llteReadInB	= np.mean(roi_df['llteReadInB'].values.tolist())
		#print llteReadInB
		llteWriteInB 	= np.mean(roi_df['llteWriteInB'].values.tolist())
		#print llteWriteInB
		#print "Loop Complete"
		ziplist.append((coreReq, avgMemInKB, avgPeakMemInKB, blkPeakReadInB, blkPeakWriteInB, blkReadInB, blkWriteInB, ibPeakReadInB, ibPeakWriteInB, ibReadInB, ibWriteInB, lltePeakReadInB, lltePeakWriteInB, llteReadInB, llteWriteInB))

	coreReq, avgMemInKB, avgPeakMemInKB, blkPeakReadInB, blkPeakWriteInB, blkReadInB, blkWriteInB, ibPeakReadInB, ibPeakWriteInB, ibReadInB, ibWriteInB, lltePeakReadInB, lltePeakWriteInB, llteReadInB, llteWriteInB = zip(*sorted(ziplist, key=lambda x:x[0]))

	cores, avgMem 		= discardValues(coreReq, avgMemInKB)
	if cores is None:
		return
#	mplt.scatter(cores, avgMem, color = 'r')
#	mplt.savefig(path+"/GroupAvgMem"+ filename+".png", format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)	
#	mplt.close()
#	
#	cores, avgPeakMem 	= discardValues(coreReq, avgPeakMemInKB)
#	if cores is None:
#		return
#	mplt.scatter(cores, avgPeakMem, color = 'b')
#	mplt.savefig(path+"/GroupAvgPkMem"+ filename+".png", format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)	
#	mplt.close()

#	cores, blkPeakRead 	= discardValues(coreReq, blkPeakReadInB)
#	if cores is None:
#		return
#	mplt.scatter(cores, blkPeakRead, color = 'r')
#	mplt.savefig(path+"/GroupBlkPR"+ filename+".png", format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)	
#	mplt.close()
#
#	cores, blkPeakWrite 	= discardValues(coreReq, blkPeakWriteInB)
#	if cores is None:
#		return
#	mplt.scatter(cores, blkPeakWrite, color = 'b')
#	mplt.savefig(path+"/GroupBlkPW"+ filename+".png", format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)	
#	mplt.close()

	cores, blkRead	 	= discardValues(coreReq, blkReadInB)
	if cores is None:
		return
	mplt.scatter(cores, blkRead, color = 'g')
	mplt.savefig(path+"/GroupBlkR"+ filename+".png", format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)	
	mplt.close()

	cores, blkWrite 	= discardValues(coreReq, blkWriteInB)
	if cores is None:
		return
	mplt.scatter(cores, blkWrite, color = 'k')
	mplt.savefig(path+"/GroupBlkW"+ filename+".png", format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)	
	mplt.close()
	
#	cores, ibPeakRead 	= discardValues(coreReq, ibPeakReadInB)
#	if cores is None:
#		return
#	mplt.scatter(cores, ibPeakRead, color='r')
#	mplt.savefig(path+"/GroupibPR"+ filename+".png", format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)	
#	mplt.close()
#
#	cores, ibPeakWrite 	= discardValues(coreReq, ibPeakWriteInB)
#	if cores is None:
#		return
#	mplt.scatter(cores, ibPeakWrite, color='g')
#	mplt.savefig(path+"/GroupibPW"+ filename+".png", format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)	
#	mplt.close()

#	cores, ibRead	 	= discardValues(coreReq, ibReadInB)
#	if cores is None:
#		return
#	mplt.scatter(cores, ibRead, color='b')
#	mplt.savefig(path+"/GroupibR"+ filename+".png", format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)	
#	mplt.close()
#
#	cores, ibWrite  	= discardValues(coreReq, ibWriteInB)
#	if cores is None:
#		return
#	mplt.scatter(cores, ibWrite ,color='k')
#	mplt.savefig(path+"/GroupibW"+ filename+".png", format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)	
#	mplt.close()

	ibRWInB = [sum(x) for x in zip(ibReadInB, ibWriteInB)]
	cores, ibRW	 	= discardValues(coreReq, ibRWInB)
	if cores is None:
		return
	mplt.scatter(cores, ibRW, color='b')
	mplt.savefig(path+"/GroupibRW"+ filename+".png", format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)	
	mplt.close()

#	cores, lltePeakRead 	= discardValues(coreReq, lltePeakReadInB)
#	if cores is None:
#		return
#	mplt.scatter(cores, lltePeakRead, color='r')
#	mplt.savefig(path+"/GroupLlitePR"+ filename+".png", format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)	
#	mplt.close()
#	
#	cores, lltePeakWrite	= discardValues(coreReq, lltePeakWriteInB)
#	if cores is None:
#		return
#	mplt.scatter(cores, lltePeakWrite, color='g')
#	mplt.savefig(path+"/GroupLlitePW"+ filename+".png", format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)	
#	mplt.close()
	
	cores, llteRead 	= discardValues(coreReq, llteReadInB)
	if cores is None:
		return
	mplt.scatter(cores, llteRead, color='b')
	mplt.savefig(path+"/GroupLliteR"+ filename+".png", format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)	
	mplt.close()
	
	cores, llteWrite   	= discardValues(coreReq, llteWriteInB)
	if cores is None:
		return
	mplt.scatter(cores, llteWrite, color='k')
	mplt.savefig(path+"/GroupLliteW"+ filename+".png", format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)	
	mplt.close()

	print filename
	return


def discardValues(coreReList, numberList):
#	print "**************************************"
	ziplist2 = []
	for c, n in zip(coreReList, numberList):
		if n > 0:
			ziplist2.append((c, n))
	if len(ziplist2) == 0:
		return None, None

	a, b = zip(*ziplist2)
	meanVal = np.mean(b)
	ziplist3 = []
	for c, n in ziplist2:
		if n < meanVal*100:
			ziplist3.append((c, n))
	
#	print "**************************************"
	if len(ziplist3) < 3:
		return None, None

	return zip(*ziplist3)
	
