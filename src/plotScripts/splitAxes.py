#!/usr/bin/python

import numpy as np
import pylab as plt
from   pylab import *
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
from   matplotlib import ticker
'''
formatter = ticker.ScalarFormatter(useMathText=True)
formatter.set_scientific(True) 
formatter.set_powerlimits((-2,2))

ax.w_xaxis.set_ticklabels(column_names)
ax.w_yaxis.set_ticklabels(row_names)
ax.w_zaxis.set_major_formatter(formatter)
'''

def splitAxes(binedge1, cdf1, binedge, cdf, xlim1, xlim2, xlim3, xlim4, xlabel1, ylabel1, xlabel2, ylabel2, leg1, leg0, filename):
	#fig,(ax,ax2) = plt.subplots(1, 2, sharey=True)
	fig,(ax,ax2) = plt.subplots(1, 2)
	# plot the same data on both axes
	#formatter = ticker.ScalarFormatter(useMathText=True)
	#formatter.set_scientific(True) 
	#formatter.set_powerlimits((-2,2))


	ax.plot(binedge1, cdf1, linewidth=3.0)
#	if binedge0 is not None:
#		print "Here 1"
#		ax.plot(binedge0, cdf0, label=leg0)
	ax2.plot(binedge, cdf, linewidth=3.0)
#	if binedge_0 is not None:
#		print "Here 2"
#		ax.plot(binedge_0, cdf_0, label=leg0)
	ax.set_xticklabels(ax.get_xticks(), fontsize=20)
	ax.set_yticklabels(ax.get_yticks(), fontsize=20)
	ax2.set_xticklabels(ax2.get_xticks(), fontsize=20)
	ax2.set_yticklabels(ax2.get_yticks(), fontsize=20)
	#ax.set_major_formatter(ScalarFormatter())
	#ax2.set_major_formatter(ScalarFormatter())
		
	#print binedge1/(1000*1000)
	#print binedge/(1000*1000)
	#b1 = np.around(binedge1/(1000*1000), decimals = 3)
	#b  = np.around(binedge/(1000*1000), decimals = 3)
	#ax.set_xticklabels(rotation=70)
	#ax2.set_xticklabels(rotation=70)
	setp( ax.xaxis.get_majorticklabels(), fontsize=20, rotation=70 )
	setp( ax2.xaxis.get_majorticklabels(), fontsize=20, rotation=70 )

	ax.spines['right'].set_visible(False)
	ax2.spines['left'].set_visible(False)
	
	# zoom-in / limit the view to different portions of the data
	ax.set_xlim(xlim1, xlim2) # most of the data
	ax2.set_xlim(xlim3, xlim4) # outliers only
	#ax.set_ylim(0, 0.8) # outliers only
	#ax2.set_ylim(0.8, 1) # outliers only
	#ax.ticklabel_format(style = 'sci', axis='x', scilimits=(-2,2))
	#ax2.ticklabel_format(style = 'sci', axis='x', scilimits=(-2,2))
	ax.set_xlabel(xlabel1, fontsize=22)
	ax2.set_xlabel(xlabel2,fontsize=22)
	ax.set_ylabel(ylabel1, fontsize=22)
	#ax2.set_ylabel(ylabel2, fontsize=22)
	#ax2.set_ylabel(ylabel2)

	#plt.setp( ax.xaxis.get_majorticklabels(), rotation='vertical' )
	#plt.setp( ax2.xaxis.get_majorticklabels(), rotation='vertical')
	
	#ax.set_xticks(rotation='vertical')
	# hide the spines between ax and ax2
	#ax.spines['right'].set_visible(False)
	#ax2.spines['left'].set_visible(False)
	ax.yaxis.tick_left()
	#ax.set_yticks(np.arange(0, 0.92, 0.3))
	#ax.set_yticklabels(np.arange(0, 0.92, 0.3))
	ax.tick_params(labeltop='off') # don't put tick labels at the top
	ax2.yaxis.tick_right()

	# Make the spacing between the two axes a bit smaller
	#plt.subplots_adjust(wspace=0.15)

	# This looks pretty good, and was fairly painless, but you can get that
	# cut-out diagonal lines look with just a bit more work. The important
	# thing to know here is that in axes coordinates, which are always
	# between 0-1, spine endpoints are at these locations (0,0), (0,1),
	# (1,0), and (1,1). Thus, we just need to put the diagonals in the
	# appropriate corners of each of our axes, and so long as we use the
	# right transform and disable clipping.

	#d = .015 # how big to make the diagonal lines in axes coordinates
	# arguments to pass plot, just so we don't keep repeating them
	#kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
	#ax.plot((1-d,1+d),(-d,+d), **kwargs) # top-left diagonal
	#ax.plot((1-d,1+d),(1-d,1+d), **kwargs) # bottom-left diagonal

	#kwargs.update(transform=ax2.transAxes) # switch to the bottom axes
	#ax2.plot((-d,d),(-d,+d), **kwargs) # top-right diagonal
	#ax2.plot((-d,d),(1-d,1+d), **kwargs) # bottom-right diagonal
	
	#plt.legend(loc=4)
	mplt.gcf().subplots_adjust(bottom=0.15)
        plt.savefig(sys.argv[2] +"/"+ filename+ ".png", bbox_inches='tight')
        plt.close()

	return

