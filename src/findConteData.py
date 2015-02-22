#!/usr/bin/python


import os
import sys
import re

for root, dirNames, fileNames in os.walk(sys.argv[1]):
	for fileName in fileNames:
		filePath = os.path.join(root,fileName)
		with open(filePath, 'r') as f:
			fileContent = f.read()
			searchResult= re.search(r'\bconte\b', fileContent, re.IGNORECASE)
			if searchResult is not None:
				print fileName

