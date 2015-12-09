#!/usr/bin/python
import liblistAnalysis as lA
import sys


if len(sys.argv) != 4:
	print "Usage: ./script.py PreinstalledList SortedHist Top_HowMany"
	exit()

fUsrLib64 = sys.argv[1]
fHistogramLibs = sys.argv[2]
rawUsrLib64s, fullPath = lA.getAllLibraryNames(fUsrLib64) 

fHist = open(fHistogramLibs, 'r')
lines = fHist.readlines()
for l in lines[:int(sys.argv[3])]:
  fields = l.split('\t')
  libName = fields[0].strip()
  if(libName in rawUsrLib64s):
    continue
  
  print l.strip()
  
#for lib in rawLibs:
# print l
 
