#!/usr/bin/python

import os
import sys
import re
import operator
import math
from collections import defaultdict
import string
import pandas as pd
import numpy as np
import pylab as plt
import matplotlib
from   mpl_toolkits.mplot3d import Axes3D
from   matplotlib.axes import Axes
import matplotlib.pyplot as mplt
import csv
import labelBar
import operator as op

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

bar_width	= 0.1
barSpacing	= 0.05

xlabelFontSZ	= 14
ylabelFontSZ	= 14
labelFontSZ	= 14

xticksFontSZ	= 14
yticksFontSZ	= 14
ticksFontSZ	= 14

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



def sliceDF(df, nodes, times):
	df1 = df[df['nodes'] == nodes]
	#print df1
	return df1


if __name__ == "__main__":
	if len(sys.argv) != 7:
		print "Usage ./script.sh <LLNLdatafile> <PathToPutOutputFile> <OutputFilename> <XaxisLabel> <YaxisLabel> <NumberofNodesFilter(64, 16, 128)>"
		exit()

	df = pd.io.parsers.read_csv(sys.argv[1], sep=',')
	df1 = sliceDF(df, int(sys.argv[6]), None)
	
        # Read the data
        tasks = df1['Req_time'].tolist()
        cpuHrs= df1['AvgQTime'].tolist()
        #for line in f:
        #        fields = [item.strip() for item in line.split(',')]
        #        tasks.append(int(fields[0]))
        #        cpuHrs.append(float(fields[1]))

        # Sort the data
        tasks, cpuHrs = zip(*sorted(zip(tasks, cpuHrs), key=op.itemgetter(0)))
        tasks = list(tasks)
        cpuHrs= list(cpuHrs)
        #print len(cpuHrs)
        #print len(tasks)

        # Plot the data
        noOfBars = len(tasks)
        filename = sys.argv[3]
        fig, ax = mplt.subplots()
        indices = np.arange(0, 0.15*noOfBars, 0.15)
        #print len(indices)
        bottomBar = ax.bar(indices[:noOfBars], cpuHrs[:noOfBars], bar_width, color=blue, linewidth=outlinewgt[0], hatch='////')
        #topBar    = ax.bar(indices, topPcnt[:noOfBars], bar_width, bottom=bottompcnt[:noOfBars], color=lightblue, linewidth=outlinewgt[-1], hatch="////")

        ax.set_xticks(indices + 0.5*(bar_width))
        xtickLabel = [''] * len(tasks)
        for i, num in enumerate(tasks):
                if i%2 == 0:
                        xtickLabel[i] = tasks[i]
        ax.set_xticklabels(xtickLabel[:noOfBars])
        #mplt.ticklabel_format(style='sci', axis='y', scilimits=(0,6))
        #ax.xaxis.get_major_formatter().set_powerlimits((0, 1))
        ax.ticklabel_format(axis='y', style='sci', scilimits=(-2,2))
        ax.set_xlabel(sys.argv[4], fontsize=labelFontSZ, fontweight=labelFontWT)
        ax.set_ylabel(sys.argv[5], fontsize=labelFontSZ, fontweight=labelFontWT)

        #ax.text(ImgNoteX, ImgNoteY, 'Total CPU hours vs Task count', \
        #        horizontalalignment='center', \
        #        verticalalignment='center', \
        #        transform=ax.transAxes, fontsize=ticksFontSZ, fontweight=labelFontWT)
        mplt.tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom='off',      # ticks along the bottom edge are off
            top='off')         # ticks along the top edge are off

        mplt.xticks(fontsize=ticksFontSZ, rotation='vertical')
        mplt.yticks(fontsize=ticksFontSZ)
        fig = matplotlib.pyplot.gcf()
        fig.set_size_inches(ImgWidth, ImgHeight)
        #mplt.legend( (bottomBar[1], topBar[0]), ("% of Job > Threshold", "% of Jobs < Threshold"))
        mplt.savefig(sys.argv[2]+"/"+ filename, format=ImgFormat, dpi=ImgDPI, bbox_inches=ImgProp)
	



