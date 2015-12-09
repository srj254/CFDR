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
red  = 'r'
green= 'g'
blue = 'b'
black= 'k'
white= 'w'
yellow='y'
lightblue = 'lightblue'

outlinewgt	= [ 1 , 1 , 1 , 1 , 1  , 1 , 1 , 3 ]

bar_width	= 0.25
barSpacing	= 0.05

xlabelFontSZ	= 16
ylabelFontSZ	= 16
labelFontSZ	= 22

xticksFontSZ	= 12
yticksFontSZ	= 12
ticksFontSZ	= 20

ylabelFontWT	= 'normal'
xlabelFontWT	= 'normal'
labelFontWT	= 'normal'

ImgFormat	= 'png'
ImgDPI		= 1000
ImgWidth	= 7
ImgHeight	= 4

with open(sys.argv[1]) as f:
	a = f.readline()
	a = a.split(',')
	a = [int(item) for item in a]
#	a = filter(lambda x: int(x)<50 and int(x)>0, a)
	a = filter(lambda x: int(x)<100000 and int(x)>0, a)
	#a = filter(lambda x: int(x)>0, a)
#	print np.mean(a)
#	print np.std(a)

	counts, bin_edges = np.histogram(a, bins=10000)
	ssum = float(counts.sum())
	counts = counts/ssum

	cdf = np.cumsum(counts)
	plt.plot(bin_edges[1:], cdf, linewidth=outlinewgt[-1])
	plt.xlim(0, 1000)
	plt.xticks(fontsize=ticksFontSZ)
	plt.yticks(fontsize=ticksFontSZ)
	plt.xlabel("Major page faults/10 mins", fontweight=labelFontWT, fontsize=labelFontSZ)
	plt.ylabel("CDF (zoomed in from 0-1000)", fontweight=labelFontWT, fontsize=labelFontSZ)
#	n, bins, patches = plt.hist(a, 20, histtype='stepfilled')
#	print bins
#	plt.setp(patches, 'facecolor', 'g', 'alpha', 0.75)
#	l = plt.plot(bins, 'k--', linewidth=1.5)
	filename = "cdfPageFlt"
	plt.savefig(sys.argv[2] + "/"+filename + ".png", bbox_inches="tight")
		
