#!/usr/bin/python

import re
import sys
import os
import string
import operator
import pandas as pd
from collections import defaultdict
import getUniqueScripts as gUS
import liblistAnalysis as lla 
import math 

def getJobID2FNameMap(liblistPath):
	j2F = defaultdict(str)
	for root, subd, fnames in os.walk(liblistPath):
                for fname in fnames:
		        baseFileName = os.path.basename(fname)
		        try:
                		user_jobid = baseFileName.split('.')[0]
		                fields = user_jobid.split('_')
		                userName = fields[0]
		                jobid = int(fields[1])
				j2F[jobid] = os.path.join(root, fname)
				#print jobid, j2F[jobid]
			except:
				continue
	return j2F

def getJobIdFrmUniqScrpts(uniqScripts):
	jobID = []
	for key in uniqScripts:
		#print (uniqScripts[key])[0]
		fname = ((uniqScripts[key])[0])
		baseFileName = os.path.basename(fname)
		#print int(baseFileName.split('.')[0])
		jobID.append(int(baseFileName.split('.')[0]))
		#raw_input()
	return jobID

def getLList(fname):
	libs, libwithPath = lla.getAllLibraryNames(fname)
	return libs

def getIDF(libname, llist):
	count =0
	for k in llist.keys():
		if libname in llist[k]:
			count += 1
	#print float(len(llist.keys())), float(count)
	x = float(len(llist.keys()))/float(count)
	y = math.log10(x)
	print libname, '\t', len(llist.keys()), '\t', count, '\t', x, '\t', y
	return y

def getTfidfPerJob(idf, jid, liblist):
	d = defaultdict(float)
	
	for lib in liblist:
		tf = (1.00/float(len(liblist)))
		d[lib] = idf[lib] * tf
	return d

def tfIdf_llist(llist):
	libnames = [item for sublist in llist.values() for item in sublist]
	idf = defaultdict(float)
	print "libraryName", '\t', "Numerator", '\t', "Denominator", '\t', "Numertr/Denmntr", '\t', "log(Num/Den)"
	for lib in set(libnames):
		idf[lib] = getIDF(lib, llist)
	exit()
	tfidf = defaultdict(dict)
	for j in llist.keys():
		tfidf[j] = getTfidfPerJob(idf, j, llist[j])

	#idfSorted = sorted(idf.items(), key=operator.itemgetter(1), reverse=False)
	#for n, v in idfSorted:
	#	print n,'\t', v
	'''
	for job in tfidf.keys():
		d = tfidf[job]
		tup = sorted(d.items(), key=operator.itemgetter(1), reverse=True)
		print job, '\t',
		for n, v in tup[:5]:
			print n+'('+str(v)+')', 
		print '\n'
	'''
	return 0

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "Usage ./script.sh liblistPath UniqueScripts"
		exit()
	
	liblistPath	= sys.argv[1]
	UniqueScripts 	= sys.argv[2] 

	unqScr  = gUS.getSameSizeFiles(UniqueScripts)
	#print len(unqScr.keys())
	#for k in unqScr.keys():
	#	print unqScr[k][0]
	#	raw_input()

	j2F 	= getJobID2FNameMap(liblistPath)
	#for j in j2F.keys():
	#	print j2F[j]
	#	raw_input()

	jlist 	= getJobIdFrmUniqScrpts(unqScr)
	llist 	= defaultdict(list)
	for j in set(jlist):
		if j2F[j] == '':
			continue
		llist[j] = getLList(j2F[j])
		#print j2F[j]

	result = tfIdf_llist(llist)
			
