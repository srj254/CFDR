#!/usr/bin/python

import re
import sys
import os
import string
from collections import defaultdict
import pandas as pd
import itertools 
import hashlib

def getSameSizeFiles(scriptPath):
	fSizeDict = defaultdict(list)
	count = 0
	for fName in os.listdir(scriptPath):
		#if 'No script found for jobid' in open(scriptPath+'/'+fName).read():
		#	continue
		#count += 1
		try:
			fSizeDict[os.path.getsize(scriptPath+'/'+fName)].append(scriptPath+'/'+fName)
		except:
			fSizeDict[os.path.getsize(scriptPath+'/'+fName)] = [scriptPath+'/'+fName]
	#print count
	return fSizeDict

def hashfile(path, blocksize = 65536):
    afile  = open(path, 'rb')
    hasher = hashlib.md5()
    buf    = afile.read(blocksize)
    while len(buf) > 0:
    	hasher.update(buf)
    	buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()

def getUniqueFiles(fileList, hashdict):
	for f in fileList:
		hashdict[hashfile(f)].append(f)

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print "Usage ./script.sh JobScriptPath"
		exit()

	fSizeDict = getSameSizeFiles(sys.argv[1])
	print len(fSizeDict.keys())
	#for key in fSizeDict.keys():
		#for f in fSizeDict[key]:
			#jobID = getJobID
	
	hashDict = defaultdict(list)
	count = 1
	for key in fSizeDict.keys():
	#	print "Starts Here"
		getUniqueFiles(fSizeDict[key], hashDict)
	#	print count, len(hashDict.keys())
		count += 1
	#	print "Ends Here"
	#	raw_input()

	print len(hashDict.keys())
	#for i in hashDict.keys():
	#	print (hashDict[i])[0]
