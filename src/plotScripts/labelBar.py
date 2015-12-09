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

def labelBar(axis, bar, bottombar, text, factor, force):
	ht = bar.get_height()
	if bottombar is not None:
		ht += bottombar.get_height()
	fsize = 12
	if (ht < 1000) and (force == 0):
		fsize = 16
	
	#axis.text(bar.get_x()+bar.get_width()/2.0, ht*(1.01 + factor), ' '+text,
        #       ha='center', va='bottom', fontsize=fsize, fontweight='bold')
	return 1

