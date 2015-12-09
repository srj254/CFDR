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
from   collections import *
#from Levenshtein import *
import hashlib


class libListFileInfo:
	liblistKey = ""
	username = ""
	jobid = 0
	def __init__(self, lkey, uname, jid):
		self.liblistKey = lkey
		self.username = uname
		self.jobid = jid
	

def doClustering(mylist, threshold):
	clusters = defaultdict(list)
	numb = range(len(mylist))
        for i in numb:
                for j in range(i+1, len(numb)):
			if distance(mylist[i].liblistKey,mylist[j].liblistKey) <= threshold:
						clusters[i].append(mylist[j].liblistKey)
						clusters[j].append(mylist[i].liblistKey)
	return clusters

def getLibKey(fileName):
	 with open(fileName, 'r') as infile:
	 	lines = []
	 	for line in infile:
	 		line = line.strip()
			line = (line.rsplit('/', 1)[1]).split('.so')[0]+ '.so'
			if (line == ""):
				continue
			lines.append(line)
	 #sort the library list to normalize. this is to take care of address space randomization
    	 lines.sort()
	 libkey = ','.join(lines)
	 hash_object = hashlib.md5(libkey.encode())
	 hashkey = hash_object.hexdigest()
	 hashkeyStr = str(hashkey)
	 return hashkey
	 
def getAllLibraryNames(fileName):
	 libs = []
	 libWithPath = []
	 with open(fileName, 'r') as infile:
	 	for line in infile:
				
			libWithPath.append(line.strip())
	 		line = line.strip()
			try:
				line = (line.rsplit('/', 1)[1]).split('.so')[0]+ '.so'
			except:
				continue
			if (line == ""):
				continue
			libs.append(line)
	 return libs, libWithPath
 
def makeLibListKey(fileName):
	baseFileName = os.path.basename(fileName)
	try:
		user_jobid = baseFileName.split('.')[0]
		fields = user_jobid.split('_')
		userName = fields[0]
		jobid = int(fields[1])
		libraryKey = getLibKey(fileName)
		libinfo = libListFileInfo(libraryKey, userName, jobid)
		return libraryKey, libinfo
	except:
		return "",None
 	
def getAllFiles(dirName, keyword):
	libraryList = []
	libraryNames= []
	libraryPaths= []
	for root, dirnames, filenames in os.walk(dirName):
		for filename in filenames:
			f = (os.path.join(root, filename))
			baseFileName = os.path.basename(f)
			if(baseFileName.find("liblist") == -1):
				continue
			libraryKey, libinfo = makeLibListKey(f)
			if(libraryKey == ""):
				continue
			libraryList.append(libinfo)

			libnames, libpaths = getAllLibraryNames(os.path.join(root, filename))
			libraryNames.extend(libnames)
			libraryPaths.extend(libpaths)
	libraryNames = sorted(list(set(libraryNames)))
	librartPaths = sorted(list(set(libraryPaths)))
	return libraryList, libraryNames, libraryPaths

def identify_similar_jobs(libList):
	jobMap = {}
	for l in libList:
        	lkey = l.liblistKey
		if lkey in jobMap.keys():
			jobMap[lkey].append(l.jobid)
		else:	
			jobMap[lkey] = []
			jobMap[lkey].append(l.jobid)
	return jobMap


def groupJobs(dirName, keyword, writeToFile, whereToWrite):
	dName = dirName
	libList, libraryNames, libraryPaths = getAllFiles(dName, keyword)

	#for item in list(set(libraryNames)):
	#	pass #print item
	
	#for i in set(libraryPaths):
	#	pass #print i
	#exit()

	jMap = identify_similar_jobs(libList)
	with open("grouped_jobs.txt", 'w') as outfile:
		outfile.write("========= same jobs ==========\n")
		for k in jMap.keys():
			jobstr= ""
			set(jMap[k])
			for j in jMap[k]:
				jobstr += str(j) + ", "
			outfile.write(jobstr)
			outfile.write("\n----------- next set ------------------\n")
		outfile.flush()
	
	with open("grouped_jobs.txt", 'r') as tempFile:
		lines = tempFile.readlines()
	os.remove('grouped_jobs.txt')

	if int(writeToFile) is 1:
		with open(whereToWrite + "/allLibraryNames", 'w') as f:
			print >> f, "\n".join(libName for libName in libraryNames)

	jobGroup = {}
	groupNumber = 1
	for line in lines:
        	if 'next set' in line or 'same jobs' in line:
                	captureLine = False
                else:
                        captureLine = True
                if captureLine:
                	jobList = list(set([item.strip(' ') for item in line.strip().split(',') if item]))
			jobGroup[groupNumber] = jobList
			if int(writeToFile) is 1:
				with open(whereToWrite + "/G"+ str(groupNumber), 'w') as f:
	                        	print >> f, str(groupNumber) + ';' +  ','.join(jobID for jobID in jobList)
			groupNumber += 1
	alist = []
	for key in jobGroup.keys():
		alist.append(len(jobGroup.get(key)))

#	print "SD ", numpy.std(alist)
#	print "Mean", numpy.mean(alist)
#	print "Median", numpy.median(alist)
#	print "Mode", numpy.argmax((numpy.bincount(alist)))
#	print "Groups ", len(jobGroup.keys())
	
	if int(writeToFile) is 1:
		job2Grp = {}
		for key in jobGroup.keys():
			jobList = jobGroup.get(key)
			for job in jobList:
				job2Grp[job] = key
		print len(job2Grp.keys())
		with open(whereToWrite + "/liblistTable.tsv", 'w') as writeFile:
			for job in job2Grp.keys():
				print >> writeFile, job, '\t', job2Grp.get(job)

	return jobGroup	

def histogramPlot(d, n, string):
	libnames = d.keys()
	jcount 	 = d.values()

	lib2Jobs = sorted(zip(libnames, jcount), key=lambda x:x[1], reverse=True)
	libnames, jcount = zip(*lib2Jobs)

	for i, tup in enumerate(lib2Jobs):
		print tup[0], '\t', tup[1]
	exit()

	noOfBars = n
	filename = string+"_TOPLibs2Jobs"+str(n)+".png"
	fig, ax = mplt.subplots()
	
	indices = np.arange(0, noOfBars*0.2, 0.2)
	'''
	indices1= np.arange(0, len(d.keys())*0.001, 0.05)
	ind = indices.tolist()
	ind1= indices1.tolist()
	ftick = []
	tlabel= []
	for i, v in enumerate(ind):
		if v < 0.35*6:
			ftick.append(v)
			tlabel.append(libnames[i])
		else:
			break
	tlabel[-1] = ''
	ind1 = sorted(ind1)
	v = ftick[-1]
	for i in ind1:
		if i > v:
			ftick.append(i)
			tlabel.append('')

	print ftick[:10]
	print tlabel[:10]
	indices = ftick[:noOfBars]
	indices = np.array(indices)
	x = 0
	#print noOfBars, len(indices), len(ftick[:noOfBars])
	indices = np.arange(0, noOfBars*0.3, 0.3) 
	'''
	topBar    = ax.bar(indices, jcount[:noOfBars], 0.1, \
			   color='Crimson', linewidth=0.5, alpha=0.3)

	#	verticalalignment='center', \
	#	transform=ax.transAxes, fontsize=ticksFontSZ, fontweight=labelFontWT)

	ax.set_xticks(indices+ 0.5*0.05)
	ax.set_xticklabels([])
	mplt.xticks(fontsize=6, rotation='vertical')
	mplt.yticks(fontsize=10)
	plt.tick_params(
		axis  ='both',       # changes apply to the x-axis
		which ='both',      # both major and minor ticks are affected
    		bottom='off',      # ticks along the bottom edge are off
    		top   ='off',         # ticks along the top edge are off
		right ='off',	   # ticks along the left edge are off
		left  ='off')        # ticks along the right edge are off

	ax.set_ylabel("No. of jobs", fontsize=14)
	ax.set_xlabel("Top "+ str(n)+" application libraries", fontsize=14)	
        fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(7, 4)
	#mplt.legend((bottomBar[0], topBar[0]), ("No. of users jobs > Threshold", "No. of users jobs"))
	#mplt.setp(plt.gca().get_legend().get_texts(), fontsize='20')
	mplt.savefig(filename, format='png', dpi=1000, bbox_inches='tight')
	
	return 

def checkmatch(find, inlist):
	substr   = find.split('-')[0]
	findlist = []
	for item in inlist:
		val = (item.split('.so')[0].split('-'))[0]
		findlist.append(val)

	for item in findlist:
		if substr in item:
			return True
	return False

def libUsers(path):
	libdict = defaultdict(int)
	libdictUsers = defaultdict(list)
	for root, subd, fnames in  os.walk(path):
		for fname in  fnames:
			with open(os.path.join(root, fname)) as f:
				uj = fname.split('.')[0]
				uname = uj.split('_')[0]

				for line in f.readlines():
					if ("condor" in line.lower() or "lib64" in line.lower()):
						continue
					try:
		                        	line = line.strip()
	        		                line = (line.rsplit('/', 1)[1]).split('.so')[0]+ '.so'
        	        		        if (line == ""):
                	        		        continue
						libdict[line] += 1		
						libdictUsers[line].append(uname)
					except:
						continue

	with open("libVsJobs.tsv", 'w') as w:
		for key in libdict.keys():
			print >> w, key, '\t', libdict[key]

	with open("libVsUsers.tsv", 'w') as w1:
		for key in libdictUsers.keys():
			print >> w1, key, '\t', len(list(set(libdictUsers[key])))

	x = "../Results/non_rcacInstalled.txt"
	rhellibs = []
	with open(x) as f:
		for lib in f:
			lib = lib.strip()
			rhellibs.append(lib)
	'''
	count = 0
	with open("NonRHEL_LibsVsUsers.tsv", 'w') as rf:
		for key in libdictUsers.keys():
			if key in rhellibs:
				print "Out", key
				count += 1
				continue
			print >> rf, key, '\t', len(list(set(libdictUsers[key])))
	print count, len(rhellibs), len(libdictUsers.keys())
	raw_input()
	'''

	count = 0
	nonRHELLibs = defaultdict(int)
	with open("NonRHEL_LibsVsJobs.tsv", 'w') as jf:
		for key in libdict.keys():
			v = checkmatch(key, rhellibs)
			if v == True:
				count += 1
				continue
			nonRHELLibs[key] = libdict[key]
			print >> jf, key, '\t', libdict[key]
	
	#histogramPlot(nonRHELLibs,  500, "nonRHEL")
	#histogramPlot(nonRHELLibs, 1000, "nonRHEL")
	
	#nonrhelziplist = zip(nonRHELLibs.keys(), nonRHELLibs.values())
	#nonrhelziplist = sorted(nonrhelziplist, key=lambda x:x[1], reverse=True)
	#top100libraries= nonrhelziplist[:100]
	
	#top100libs, cts = zip(*top100libraries)

	count = 0
	nonRHELLibs = defaultdict(int)
	with open("NonRHEL_LibsVsUsers.tsv", 'w') as jf:
		for key in libdictUsers.keys():
			v = checkmatch(key, rhellibs)
			if v == True:
				count += 1
				continue
			nonRHELLibs[key] = len(set(libdictUsers[key]))
			print >> jf, key, '\t', libdictUsers[key]

        histogramPlot(nonRHELLibs,  500, "nonRHEL_user")
	'''
	zipped = []
	for key in libdictUsers.keys():
		zipped.append((key, len(list(set(libdictUsers[key])))))
	
	libvsUsers = sorted(zipped, key=lambda x: x[1], reverse=True)
	l, urs = zip(*libvsUsers)
	
	d = defaultdict(int)
	for lib, uc in libvsUsers:
		d[lib] = uc

        with open("NonRHEL_LibsVsUsers.tsv", 'w') as uf:
                for key in d.keys():
                        print >> uf, key, '\t', d[key]

        #histogramPlot(d,  500, "nonRHEL_user")
        #histogramPlot(d, 1000, "nonRHEL_user")
	'''
	
	'''
	rcaclibs = []
	x = "find_apps_rhel6_so.txt" 
	with open(x) as f:
		for line in f:
			try: 
				line = line.strip()
		        	line = (line.rsplit('/', 1)[1]).split('.so')[0]+ '.so'
        		        if (line == ""):
					continue
				rcaclibs.append(line)
			except:	
				continue

	print "Total RCAC lib:", len(rcaclibs)
	print "Intersection of top100 vs RCAC", len(list(set(top100libs) & set(rcaclibs)))
	print "Intersection of top50 vs RCAC", len(list(set(top100libs[:50]) & set(rcaclibs)))
	print "Intersection of top100 User libraries vs RCAC", len(list(set(l[:100]) & set(rcaclibs)))
	print "Intersection of top50 User Libraries vs RCAC", len(list(set(l[:50]) & set(rcaclibs)))

	count = 0
	with open("NonRCAC_LibsVsUsers.tsv", 'w') as rf:
		for key in libdictUsers.keys():
			if key in rcaclibs:
				print "Out", key
				count += 1		
				continue
			print >> rf, key, '\t', len(list(set(libdictUsers[key])))
	print count, len(rcaclibs), len(libdictUsers.keys())
	raw_input()
	'''

	'''
	count = 0
	nonrcaclibs = defaultdict(int)
	with open("NonRCAC_LibsVsJobs.tsv", 'w') as jf:
		for key in libdict.keys():
			if key in rcaclibs:
				count += 1
				continue
			print >> jf, key, '\t', libdict[key]
			nonrcaclibs[key] = libdict[key]
	print count, len(rcaclibs), len(libdictUsers.keys())
	
	nonrcacziplist = zip(nonrcaclibs.keys(), nonrcaclibs.values())
	nonrcacziplist = sorted(nonrcacziplist, key=lambda x:x[1], reverse=True)
	top100userlibs = nonrcacziplist[:100]

	top100Ulibs, top100cts = zip(*top100userlibs)
	top100Rlibs, top100cts = zip(*top100libraries)
	
	print len(list(set(top100Ulibs) & set(top100Rlibs)))
		
	histogramPlot(nonrcaclibs,  50, "nonRCAC")
	histogramPlot(nonrcaclibs, 100, "nonRCAC")
	'''
	return

if __name__ == "__main__":
        if len(sys.argv) < 4:
                print "Usage: ./liblistAnalysis <Path to top level folder of liblist> <conte | hansen> <Where to write>"
                exit()
        #groupJobs(sys.argv[1], sys.argv[2], 1, sys.argv[3])
	libUsers(sys.argv[1])

