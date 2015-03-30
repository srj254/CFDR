#!/usr/bin/python

import sys
import re
import os
import pandas as pd
import numpy  as np
import scipy  as sp


def createNodeDictionary(nodePath):
	nodeDict = {}
	for dirpath, dirnames, filenames in os.walk(nodePath):
		for filename in filenames:
			filepath = os.path.join(dirpath, filename)
			if "SystemInformationTable" in filepath:
				continue
			
			try:
				df = pd.io.parsers.read_csv(filepath, sep='\t')
				df = pd.DataFrame.sort(df, columns='Timestamp')
			except pd._parser.CParserError:
				df = None
			key = filename.split('.')[0]
			nodeDict[key] = df
	return nodeDict

def createTaccDB(nodesPath):
	nodesDict={}
	for dirpath, dirnames, filenames in os.walk(nodesPath):
		for dirname in dirnames:
			nodeNumber = int((dirname.split('.')[0].split('-')[1])[1:])
			nodesDict[nodeNumber] = createNodeDictionary(os.path.join(dirpath, dirname))
	return nodesDict

def extractTaccStats(taccDB, node, key, start, end):
	nodeDict = taccDB.get(node)
	df 	 = nodeDict.get(key)
	roi_df   = df[(df['Timestamp'] >= start) & (df['Timestamp'] <= end)]
	return roi_df
	
if __name__ == "__main__":
	if len(sys.argv) != 6:
		print "Usage: ./<ScriptName> TaccStatsFilePath NodeNumber keyAttr start_time end_time"
		exit()
	taccDB 	  = createTaccDB(sys.argv[1])
	dfExtract = extractTaccStats(taccDB, int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5]))
	mylist =  (dfExtract['rd_merges,E'])
	print mylist.tolist()
