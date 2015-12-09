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
from   scipy import stats
import splitAxes

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
ImgWidth        = 12 
ImgHeight       = 10
ImgProp         = 'tight'
ImgNoteX        = 0.80
ImgNoteY        = 0.85

def cdfPlotLliteR(mydf):
	'''
	df = mydf

	df['peakliteReadRt'] = df['lltePeakReadInB'] * (1.00/(600))

	a = df['peakliteReadRt'].values.tolist()
	v = 20*1000000000
        a = filter(lambda x: x<v, a)
	v = stats.scoreatpercentile(a, 80)

        #a = filter(lambda x: x<100000 and x>0, a)
        counts1, bin_edges1 = np.histogram(a, bins=100000000)
        ssum1 = float(counts1.sum())
        counts1 = counts1/ssum1
        cdf1 = np.cumsum(counts1)

        counts, bin_edges = np.histogram(a, bins=100000000)
        ssum = float(counts.sum())
        counts = counts/ssum
        cdf = np.cumsum(counts)
	
        #leg_pkIBRwRt = plt.plot(bin_edges[1:], cdf, color=blue, linewidth=outlinewgt[-1], label="Peak data rate for all jobs")
        #plt.xlim(0, 0.2*1000000000000)
        filename = "cdfllitePeakRdRt"
        splitAxes.splitAxes(bin_edges1[1:], cdf1, bin_edges[1:], cdf, \
                            0, v, v, np.amax(a), \
                           "Bytes/sec", "CDF", \
                           "Bytes/sec", "CDF", \
                           "Peak Lustre write rate", "Peak Lustre write rate", \
                           filename)
	'''
	'''
	df = mydf

	df['peakliteReadRt'] = df['lltePeakReadInB'] * (1.00/600.00)
	a = df['peakliteReadRt'].values.tolist()
	v = stats.scoreatpercentile(a, 90)
	#v = 20*1000000000
        a = filter(lambda x: x<v, a)

        counts, bin_edges = np.histogram(a, bins=10000)
        ssum = float(counts.sum())
        counts = counts/ssum
        cdf = np.cumsum(counts)
	print cdf, bin_edges	

        filename = "cdfllitePeakReadRt-1"

	plt.plot(bin_edges[1:], cdf, linewidth=outlinewgt[-1])
	plt.xlim(0, stats.scoreatpercentile(a, 75))

	plt.tick_params(
		axis  ='y',       # changes apply to the x-axis
		which ='both',      # both major and minor ticks are affected
		right ='off',	   # ticks along the left edge are off
		left  ='on')        # ticks along the right edge are off

	plt.xticks(fontsize=ticksFontSZ)
	plt.xlabel("Peak Lustre read (bytes/sec)", fontweight=labelFontWT, fontsize=labelFontSZ)
	plt.ylabel("CDF", fontweight=labelFontWT, fontsize=labelFontSZ)
	plt.savefig(sys.argv[2] + "/"+filename + ".png")
	plt.close()

        filename = "cdfllitePeakReadRt-2"

	plt.plot(bin_edges[1:], cdf, linewidth=outlinewgt[-1])
	plt.xlim(stats.scoreatpercentile(a, 50), np.amax(a))
	plt.xticks(fontsize=ticksFontSZ)
	plt.tick_params(
		axis  ='y',       # changes apply to the x-axis
		which ='both',      # both major and minor ticks are affected
		right ='on',	   # ticks along the left edge are off
		left  ='off')        # ticks along the right edge are off

	plt.savefig(sys.argv[2] + "/"+filename + ".png")
	plt.close()
	'''

	df = mydf
	peakRdRtList = []
	#peakWrtRtList= []
	for grp in list(set(df['JobGrp'])):
		if grp == "-NA-":
			continue
		dt = df[df['JobGrp']== grp]
		peakRdRt = (np.mean(dt['lltePeakReadInB'].values.tolist()))/(600.00)
		#peakWrtRt= (np.mean(dt['lltePeakWriteInB'].values.tolist()))/600.00 
		peakRdRtList.append(peakRdRt)
		#peakWrtRtList.append(peakWrtRt)

	a = peakRdRtList
	v = 20*1000000000
        a = filter(lambda x: x<v, a)
	v = stats.scoreatpercentile(a, 90)	

	#a = filter(lambda x: x<100000 and x>0, a)

        counts1, bin_edges1 = np.histogram(a, bins=len(a)/2)
        ssum1 = float(counts1.sum())
        counts1 = counts1/ssum1
        cdf1 = np.cumsum(counts1)

        counts, bin_edges = np.histogram(a, bins=len(a)/2)
        ssum = float(counts.sum())
        counts = counts/ssum
        cdf = np.cumsum(counts)
	print cdf, bin_edges

        #leg_pkIBRwRt = plt.plot(bin_edges[1:], cdf, color=blue, linewidth=outlinewgt[-1], label="Peak data rate for all jobs")
        #plt.xlim(0, 0.2*1000000000000)
        filename = "cdfllitePeakRdRtVsAppGroup"
        splitAxes.splitAxes(bin_edges1[1:], cdf1, bin_edges[1:], cdf, \
                            0, v, v, np.amax(a), \
                           "Bytes/sec", "CDF ", \
                           "Bytes/sec", "CDF", \
                           "Peak Lustre read rate (app groups)", "Peak Lustre read rate (app groups)", \
                           filename)

	'''
        counts, bin_edges = np.histogram(a, bins=10000)
        ssum = float(counts.sum())
        counts = counts/ssum
        cdf = np.cumsum(counts)
	print cdf, bin_edges	
        filename = "cdfllitePeakReadRtVsAppGrp-1"
	plt.plot(bin_edges[1:], cdf, linewidth=outlinewgt[-1])
	plt.xlim(0, stats.scoreatpercentile(a, 75))
	plt.tick_params(
		axis  ='y',       # changes apply to the x-axis
		which ='both',      # both major and minor ticks are affected
		right ='off',	   # ticks along the left edge are off
		left  ='on')        # ticks along the right edge are off

	plt.xticks(fontsize=ticksFontSZ)
	plt.xlabel("Peak Lustre read (bytes/sec)", fontweight=labelFontWT, fontsize=labelFontSZ)
	plt.ylabel("CDF", fontweight=labelFontWT, fontsize=labelFontSZ)
	plt.savefig(sys.argv[2] + "/"+filename + ".png")
	plt.close()

        filename = "cdfllitePeakReadRtVsAppGrp-2"

	plt.plot(bin_edges[1:], cdf, linewidth=outlinewgt[-1])
	plt.tick_params(
		axis  ='y',       # changes apply to the x-axis
		which ='both',      # both major and minor ticks are affected
		right ='on',	   # ticks along the left edge are off
		left  ='off')        # ticks along the right edge are off

	plt.xlim(stats.scoreatpercentile(a, 75), np.amax(a))
	plt.xticks(fontsize=ticksFontSZ)
	plt.savefig(sys.argv[2] + "/"+filename + ".png")
	plt.close()

	splitAxes.splitAxes(bin_edges1[1:], cdf1, bin_edges[1:], cdf, \
                            0, v, np.mean(a), np.amax(bin_edges[1:]), \
                           "Bytes/sec", "CDF (points below 90 percentile)", \
                           "Bytes/sec", "CDF (all points)", \
                           "Peak lustre read rate", "Peak lustre read rate", \
                           filename)
	'''
	'''
	df = mydf

	df['peakliteWriteRt'] = df['lltePeakWriteInB'] * (1.00/600)
	a = df['peakliteWriteRt'].values.tolist()

	v = stats.scoreatpercentile(a, 90)
	v = 20*1000000000
        a1 = filter(lambda x: x<v, a)

        #a = filter(lambda x: x<100000 and x>0, a)
        counts1, bin_edges1 = np.histogram(a1, bins=10000)
        ssum1 = float(counts1.sum())
        counts1 = counts1/ssum1
        cdf1 = np.cumsum(counts1)

        counts, bin_edges = np.histogram(a, bins=10000)
        ssum = float(counts.sum())
        counts = counts/ssum
        cdf = np.cumsum(counts)

        #leg_pkIBRwRt = plt.plot(bin_edges[1:], cdf, color=blue, linewidth=outlinewgt[-1], label="Peak data rate for all jobs")
        #plt.xlim(0, 0.2*1000000000000)
        filename = "cdfllitePeakWrtRt"
        splitAxes.splitAxes(bin_edges1[1:], cdf1, bin_edges[1:], cdf, \
                            0, v, np.mean(a), np.amax(bin_edges[1:]), \
                           "Bytes/sec", "CDF (jobs below 90 percentile)", \
                           "Bytes/sec", "CDF (all jobs)", \
                           "Peak lustre write rate", "Peak lustre write rate", \
                           filename)

	'''
	'''
	v = stats.scoreatpercentile(a, 90)
        a1 = filter(lambda x: x<v, a)

        counts1, bin_edges1 = np.histogram(a1, bins=10000)
        ssum1 = float(counts1.sum())
        counts1 = counts1/ssum1
        cdf1 = np.cumsum(counts1)

        counts11, bin_edges11 = np.histogram(a, bins=10000)
        ssum11 = float(counts11.sum())
        counts11 = counts11/ssum11
        cdf11 = np.cumsum(counts11)
        
	#df['peakliteWriteRt'] = df['lltePeakWriteInB'] * (1.00/600)
	#a = df['peakliteWriteRt'].values.tolist()

        v = stats.scoreatpercentile(a, 90)
        a1 = filter(lambda x: x<v, a)

	counts0, bin_edges0 = np.histogram(a1, bins=100)
	ssum0 = float(counts0.sum())
	counts0 = counts0/ssum0
	cdf0 = np.cumsum(counts0)
	
	counts00, bin_edges00 = np.histogram(a, bins=100)
	ssum00 = float(counts00.sum())
	counts00 = counts00/ssum00
	cdf00 = np.cumsum(counts00)
        splitAxes.splitAxes(bin_edges1[1:], cdf1, bin_edges11[1:], cdf11, \
			    bin_edges0[1:], cdf0, bin_edges00[1:], cdf00, \
                            0, v, np.mean(a), np.amax(bin_edges00[1:]), \
                           "Bytes/sec", "CDF (points below 90 percentile)", \
                           "Bytes/sec", "CDF (all points)", \
                           "Peak lustre read", "Peak lustre write", \
                           filename)
	'''
	'''
	counts, bin_edges = np.histogram(a, bins=10000)
	ssum = float(counts.sum())
	counts = counts/(ssum)
	cdf = np.cumsum(counts)
	leg_pkllrb = plt.plot(bin_edges[1:], cdf, color=blue, label="Peak lustre read", linewidth=outlinewgt[-1])
	
	df['peakliteWriteRt'] = df['lltePeakWriteInB'] * (1.00/600)
	a = df['peakliteWriteRt'].values.tolist()
	#a = filter(lambda x: x<100000 and x>0, a)
	counts, bin_edges = np.histogram(a, bins=100)
	ssum = float(counts.sum())
	counts = counts/ssum
	cdf = np.cumsum(counts)
	leg_pkllwb = plt.plot(bin_edges[1:], cdf, color=red, label="Peak lustre write", linewidth=outlinewgt[-1])
	'''
	'''
	#plt.xlim(0, np.mean(a))
	plt.xlabel("Bytes/sec")
	plt.ylabel("CDF")
	filename = "cdfllitePeakRdRt"
	plt.legend(loc=4)
	plt.savefig(sys.argv[2] +"/"+ filename + ".png")
	plt.close()

	df = mydf
	df['Runtime'] = df['end'] - df['start']
	df['avglliteReadRt'] = df['llteReadInB']/df['Runtime']
	a = df['avglliteReadRt'].values.tolist()
	a = filter(lambda x: x>0, a)
	counts, bin_edges = np.histogram(a, bins=100)
	ssum = float(counts.sum())
	counts = counts/ssum
	cdf = np.cumsum(counts)
	leg_llrb = plt.plot(bin_edges[1:], cdf, color=blue, label="Total lustre read", linewidth=outlinewgt[-1])
	#plt.xlim(0, 1000)
	plt.xlim(0, (bin_edges[-1]/50))
	plt.xlabel("In bytes per second")
	plt.ylabel("CDF")
	filename = "cdflliteReadRt"

	plt.legend(loc=4)
	plt.savefig(sys.argv[2] +"/"+ filename + ".png")
	plt.close()

	'''


        #leg_pkIBRwRt = plt.plot(bin_edges[1:], cdf, color=blue, linewidth=outlinewgt[-1], label="Peak data rate for all jobs")
        #plt.xlim(0, 0.2*1000000000000)
	'''
	counts, bin_edges = np.histogram(peakRdRtList, bins=100)
	ssum = float(counts.sum())
	counts = counts/ssum
	cdf = np.cumsum(counts)
	leg_pkllrb = plt.plot(bin_edges[1:], cdf, color=blue, label='Peak lustre read', linewidth=outlinewgt[-1])
	
	counts, bin_edges = np.histogram(peakWrtRtList, bins=100)
	ssum = float(counts.sum())
	counts = counts/ssum
	cdf = np.cumsum(counts)
	leg_pkllwb = plt.plot(bin_edges[1:], cdf, color=red, linewidth=outlinewgt[-1], label="Peak lustre write")
	plt.xlabel("In bytes per second")
	plt.ylabel("CDF")
	plt.legend(loc=4)
	plt.xlim(0, (bin_edges[-1]/50))
	filename = "cdfllitePeakRWRtVsAppGrp"
	plt.savefig(sys.argv[2] +"/"+ filename + ".png")
	plt.close()
	'''
	return
'''
def cdfPlotBlockR(mydf):
	df = mydf
	df['peakBlkReadRt'] = df['blkPeakReadInB'] * (1.00/600)
	a = df['peakBlkReadRt'].values.tolist()
	#a = filter(lambda x: x<100000 and x>0, a)
	counts, bin_edges = np.histogram(a, bins=10000)
	ssum = float(counts.sum())
	counts = counts/ssum
	cdf = np.cumsum(counts)
	leg_pkBlkRd = plt.plot(bin_edges[1:], cdf, color=blue, linewidth=outlinewgt[-1], label="Peak Sectors read")

	df['peakBlkWriteRt'] = df['blkPeakWriteInB'] * (1.00/600)
	a = df['peakBlkWriteRt'].values.tolist()
	#a = filter(lambda x: x<100000 and x>0, a)
	counts, bin_edges = np.histogram(a, bins=10000)
	ssum = float(counts.sum())
	counts = counts/ssum
	cdf = np.cumsum(counts)
	leg_pkBlkWtRt = plt.plot(bin_edges[1:], cdf, color=red, linewidth=outlinewgt[-1], label="Peak sectors write")

	filename = "cdfBlkPeakRWRt"
	plt.xlim(0, (bin_edges[-1]/50))
	plt.legend(loc=4)
	plt.savefig(sys.argv[2] +"/"+ filename + ".png")
	plt.close()

	df = mydf
	df['Runtime'] = df['end'] - df['start']
	df['avgBlkReadRt'] = df['blkReadInB']/df['Runtime']
	a = df['avgBlkReadRt'].values.tolist()
	#a = filter(lambda x: x<100000 and x>0, a)
	counts, bin_edges = np.histogram(a, bins=10000)
	ssum = float(counts.sum())
	counts = counts/ssum
	cdf = np.cumsum(counts)
	leg_blkRd = plt.plot(bin_edges[1:], cdf, color=blue, linewidth=outlinewgt[-1], label="Sectors Read (In bytes)")
	filename = "cdfBlkReadRt"
	plt.xlim(0, (bin_edges[-1]/50))
	plt.legend(loc=4)
	plt.savefig(sys.argv[2] +"/"+ filename + ".png")
	plt.close()

	return
'''

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "Usage ./Script.sh <AccountingTable> <Path to save plots>"
		exit()
	
	df = pd.io.parsers.read_csv(sys.argv[1], sep='\t')
	df = pd.DataFrame.sort (df, columns = 'JobID')
	cdfPlotLliteR(df)
#	cdfPlotBlockR(df)

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
