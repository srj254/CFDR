#!/usr/bin/python

import sys
import re
import os
import pandas as pd
import numpy  as np
import scipy  as sp


def createNodeDictionary(nodePath):
	global countSuccess
	global count
	global state
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
			nodeDict[filename] = df
	return nodeDict

def createTaccDB(nodesPath):
	nodesDict={}
	for dirpath, dirnames, filenames in os.walk(nodesPath):
		for dirname in dirnames:
			nodeNumber = int((dirname.split('.')[0].split('-')[1])[1:])
			createNodeDictionary(os.path.join(dirpath, dirname))
	return nodesDict
		
#	createNodeDictionary("../TaccStatsData/conte_processed/conte-a000.rcac.purdue.edu")
createNodeDictionary(sys.argv[1])
print count, countSuccess

