#!/usr/bin/python


import sys
import os
import numpy as np
import scipy as sp
import pylab as plt

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
		
