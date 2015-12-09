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
import splitAxes
from   scipy import stats

patterns        = [ '', '', '','/','\\','o','.','' ]

gray = 0.5
red  = 'r'
green= 'g'
blue = 'b'
black= 'k'
white= 'w'
lightblue = 'lightblue'

outlinewgt      = [ 1 , 1 , 1 , 1 , 1  , 1 , 1 , 1.5, 3.0]

bar_width       = 0.25
barSpacing      = 0.05

xlabelFontSZ    = 16
ylabelFontSZ    = 14
labelFontSZ     = 14

xticksFontSZ    = 12
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
ImgNoteX        = 0.80
ImgNoteY        = 0.85

def cdfPlotAvgMem(mydf):
	
	df = mydf
	#df[''] = (df['ibPeakReadInB'] + df['ibPeakWriteInB'])*(1.00/600)

	a = df['avgMemInKB'].values.tolist()

	a1 = a
	v = stats.scoreatpercentile(a, 90)

	#a = filter(lambda x: x<100000 and x>0, a)
	counts1, bin_edges1 = np.histogram(a1, bins=10000)
	ssum1 = float(counts1.sum())
	counts1 = counts1/ssum1
	cdf1 = np.cumsum(counts1)

        counts, bin_edges = np.histogram(a, bins=10000)
        ssum = float(counts.sum())
        counts = counts/ssum
        cdf = np.cumsum(counts)


	#plt.plot(bin_edges[1:], counts, color=red, linewidth=outlinewgt[-1], label="Data Rate")
	filename = "cdfAvgMemInKB"
	#plt.xlim(0, 1000)
	#plt.xlabel("KB/sec")
	#plt.ylabel("CDF")
	#plt.xlim(0, (bin_edges[-1]))
	#plt.legend(loc=4)
	#plt.savefig(sys.argv[2] +"/"+ filename + ".png")
	#plt.close()
	#leg_pkIBRwRt = plt.plot(bin_edges[1:], cdf, color=blue, linewidth=outlinewgt[-1], label="Peak data rate for all jobs")
	#plt.xlim(0, 0.2*1000000000000)
	'''
	splitAxes.splitAxes(bin_edges1[1:], cdf1, bin_edges[1:], cdf, \
			    0, v, v, np.amax(a), \
			   "KB", "CDF", \
			   "KB", "CDF", \
			   "Average memory used", "Average memory used", \
			   filename)
	
	#plt.xlim(0, (bin_edges[-1]/5000))
	#plt.legend(loc=4)
	#plt.xlabel("In bytes per second")
	#plt.ylabel("CDF")
	#plt.savefig(sys.argv[2] +"/"+ filename + ".png")
	#plt.close()
	'''
	'''
	df = mydf
	df['Runtime'] = df['end'] - df['start']
	df['avgIBRwRt'] = (df['ibReadInB'] + df['ibWriteInB'])/df['Runtime']
	a = df['avgIBRwRt'].values.tolist()
	a = filter(lambda x: x>0, a)
	counts, bin_edges = np.histogram(a, bins=10000)
	ssum = float(counts.sum())
	counts = counts/ssum
	cdf = np.cumsum(counts)
	leg_IBRwRt = plt.plot(bin_edges[1:], cdf, color=red, linewidth=outlinewgt[-1], label="Data Rate")
	#plt.xlim(0, 1000)
	filename = "cdfIBRwRt"
	plt.xlabel("In bytes per second")
	plt.ylabel("CDF")
	plt.xlim(0, (bin_edges[-1]/5000))
	plt.legend(loc=4)
	plt.savefig(sys.argv[2] +"/"+ filename + ".png")
	plt.close()
	'''	
	
	df = mydf
	peakRWRtList = []
	for grp in list(set(df['JobGrp'])):
		if grp == "-NA-":
			continue
		dt = df[df['JobGrp']== grp]
		peakRWRt = (np.mean(dt['avgMemInKB'].values.tolist()))
		peakRWRtList.append(peakRWRt)

	a = peakRWRtList
	peakRWRtList1 = filter(lambda x: x<v, a)
	v = stats.scoreatpercentile(a, 90)
	a1 = peakRWRtList1

	counts1, bin_edges1 = np.histogram(peakRWRtList1, bins=10000)
	ssum1 = float(counts1.sum())
	counts1 = counts1/(ssum1)
	cdf1 = np.cumsum(counts1)
	#leg_IBRwRt = plt.plot(bin_edges[1:], cdf, color=blue, linewidth=outlinewgt[-1], label="Peak data rate for jobs in app groups")
	
	counts, bin_edges = np.histogram(peakRWRtList, bins=10000)
	ssum = float(counts.sum())
	counts = counts/(ssum)
	cdf = np.cumsum(counts)
	
	leg_IBRwRt = plt.plot(bin_edges[1:], cdf, color=blue, linewidth=outlinewgt[-1], label="Data Rate")
	#plt.xlim(0, 1000)
	filename = "cdfAvegMemVsAppGrp"
	plt.xlabel("KB", fontsize=22)
	plt.ylabel("CDF", fontsize=22)
	mplt.xticks(fontsize=20)
	mplt.yticks(fontsize=20)
	#plt.xlim(0, (bin_edges[-1]))
	#plt.legend(loc=4)
	plt.savefig(sys.argv[2] +"/"+ filename + ".png")
	plt.close()
	exit()
	'''
	filename = "cdfAvgMemVsAppGrp"
	splitAxes.splitAxes(bin_edges1[1:], cdf1, bin_edges[1:], cdf, \
			    0, v, np.mean(a), np.amax(bin_edges[1:]), \
			   "Bytes/sec", "CDF", \
			   "Bytes/sec", "CDF", \
			   "Average memory", "Average memory", \
			   filename)

	#leg_IBRwRt = plt.plot(bin_edges[1:], cdf, color=blue, linewidth=outlinewgt[-1], label="Peak data rate for jobs in app groups")
	#plt.xlim(0, (bin_edges[-1]/5000))
	#plt.legend(loc=4)
	#plt.xlabel("In bytes per second")
	#plt.ylabel("CDF")
	#plt.savefig(sys.argv[2] +"/"+ filename + ".png")
	#plt.close()
	'''

	return

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "Usage ./Script.sh <AccountingTable> <Path to save plots>"
		exit()
	
	df = pd.io.parsers.read_csv(sys.argv[1], sep='\t')
	df = pd.DataFrame.sort (df, columns = 'JobID')
	cdfPlotAvgMem(df)

'''
with open(sys.argv[1]) as f:
	a = f.readline()
	a = a.split(',')
	a = [int(item) for item in a]
#	a = filter(lambda x: int(x)<50 and int(x)>0, a)
	a = filter(lambda x: int(x)<100000 and int(x)>0, a)
#	print np.mean(a)
#	print np.std(a)

	counts, bin_edges = np.histogram(a, bins=10000)
	ssum = float(counts.sum())
	counts = counts/ssum

	cdf = np.cumsum(counts)
	plt.plot(bin_edges[1:], cdf)
	plt.xlim(0, 1000)
#	n, bins, patches = plt.hist(a, 20, histtype='stepfilled')
#	print bins
#	plt.setp(patches, 'facecolor', 'g', 'alpha', 0.75)
#	l = plt.plot(bins, 'k--', linewidth=1.5)
	filename = "cdfPageFlt"
	plt.savefig(filename + ".png")
'''		
