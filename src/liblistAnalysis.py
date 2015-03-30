#!/usr/bin/python
import sys
import os
from collections import *
#from Levenshtein import *
import hashlib
import numpy

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
	 with open(fileName, 'r') as infile:
	 	for line in infile:
	 		line = line.strip()
			line = (line.rsplit('/', 1)[1]).split('.so')[0]+ '.so'
			if (line == ""):
				continue
			libs.append(line)
	 return (libs)
 
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

			libraryNames.extend(getAllLibraryNames(os.path.join(root, filename)))
	libraryNames = sorted(list(set(libraryNames)))
	return libraryList, libraryNames

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
	libList, libraryNames = getAllFiles(dName, keyword)
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
#	raw_input()
	return jobGroup	


if __name__ == "__main__":
        if len(sys.argv) < 4:
                print "Usage: ./liblistAnalysis <Path to top level folder of liblist> <conte | hansen> <Where to write>"
                exit()
        groupJobs(sys.argv[1], sys.argv[2], 1, sys.argv[3])
