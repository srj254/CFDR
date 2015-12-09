#!/usr/bin/python

import numpy as np
import pylab as plt
import os
import sys
import math
import pandas as pd
import matplotlib
from   mpl_toolkits.mplot3d import Axes3D
from   matplotlib.axes import Axes
import matplotlib.pyplot as mplt
import csv
import sys
import os
import math
import operator
from   collections import defaultdict
import liblistAnalysis as llA

def whoUsesTheLibs(jobgroups, path):
       	libJobs	 = defaultdict(list)
        libUsers = defaultdict(list)
	jobLibs	 = defaultdict(list)
	userLibs = defaultdict(list)
        for root, subd, fnames in os.walk(path):
                for fname in fnames:
                        with open(os.path.join(root, fname)) as f:
				try:
	                                uj 	= fname.split('.')[0]
        	                        uname 	= uj.split('_')[0]
					jobID 	= uj.split('_')[1]
				except:
					continue

                                for line in f:
                                        try:
                                                line 	= line.strip()
                                                libName = (line.rsplit('/', 1)[1]).split('.so')[0]+ '.so'
                                                if (libName == ""):
                                                        continue
                                                libJobs[libName].append(int(jobID))
                                                libUsers[libName].append(uname)
						jobLibs[jobID].append(libName)
						userLibs[uname].append(libName)
                                        except:
                                                continue
	return libJobs, libUsers, jobLibs, userLibs
	
def getGrp_TfIdf_Score(jobgroups, libJobs, libUsers, jobLibs, userLibs):
	libScorePerGrp = defaultdict(dict)

	jobgrpLibs = defaultdict(list)
	for group in jobgroups.keys():
		for job in jobgroups[group]:
			jobgrpLibs[group].extend(jobLibs[job])

	nAppGrps = len(jobgroups.keys()) # Number of documents
	libOccurence = defaultdict(int)
	for group in jobgrpLibs.keys():
		for lib in set(jobgrpLibs[group]):
			libOccurence[lib] += 1

	for group in jobgrpLibs.keys():
		score = defaultdict(float)
		for lib in set(jobgrpLibs[group]):
			score[lib] = jobgrpLibs[group].count(lib)
		for lib in score.keys():
			score[lib] = float(float(score[lib])/len(jobgrpLibs[group])) * \
					   math.log10(nAppGrps/libOccurence[lib])
		libScorePerGrp[group] = score
		for lib in score.keys():
			print lib, '\t', score[lib]
	return

if __name__ == "__main__":
        if len(sys.argv) != 2:
                print "Usage: ./liblistAnalysis <Path to top level folder of liblist>"
                exit()

	jobgroups = llA.groupJobs(sys.argv[1], 'conte', 0, "./")
	libJobs, libUsers, jobLibs, userLibs = whoUsesTheLibs(jobgroups, sys.argv[1])
	getGrp_TfIdf_Score(jobgroups, libJobs, libUsers, jobLibs, userLibs)

