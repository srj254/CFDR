#!/usr/bin/python

import os
import sys
import re
import pandas as pd
import fileinput
from ast import literal_eval as make_tuple
import shutil
from collections import defaultdict
import operator 
'''
with open(sys.argv[1]) as f:
	for line in f:
		try:
			shutil.copy2(line.strip(), sys.argv[2]+'/')	
		except:
			continue
	
'''
with open(sys.argv[1]) as f:
	d = defaultdict(int)
	for line in f:
		fields = [i.strip() for i in line.split()]
		d[fields[0]] = int(fields[1])
	d1 = sorted(d.items(), key=operator.itemgetter(1), reverse=True)

	for l, n in d1:
		print l, '\t', n
	

'''
def getAllLibraryNames(fileName):
         libs = []
         with open(fileName, 'r') as infile:
                for line in infile:
			try:
	                        line = line.strip()
                        	line = (line.rsplit('/', 1)[1]).split('.so')[0]+ '.so'
                	        if (line == ""):
        	                        continue
				if line[0] == '.':
					start = 1
				else:
					start = 0
				libs.append(line[start:])
			except:
				continue
         return (libs)

libs = getAllLibraryNames(sys.argv[1])

for i in libs:
	print i
'''

'''
df  = pd.io.parsers.read_csv(sys.argv[1], sep='\t')
orig = df

users = df['user'].values.tolist()
ousers= df['OriginalUser'].values.tolist()

uziplist = sorted(zip(users, ousers), key=lambda x: x[1], reverse=True)
uziplist = (list(set(uziplist)))

print users[60:90], "\n", ousers[60:90]

f 	= open(sys.argv[2], 'r')
out 	= open(sys.argv[3], 'w')
count = 0
for line in f:
	count += 1
	for u, ou in uziplist:
		line = line.replace(ou, u)
	out.write(line)

print count

out.close()
f.close()
'''

'''
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import operator

df  = pd.io.parsers.read_csv(sys.argv[1], sep='\t')
exitStatus = df[sys.argv[2]].values.tolist()
bins = Counter(exitStatus)
bintuples = sorted(bins.items(), key=operator.itemgetter(1), reverse=True)
#print bins

mysum = 0;
for i,j in bintuples:
	print 'ExitStatus',i,':',bins[i], 'jobs'
	if i == 0:
		continue
	mysum = mysum + bins[i]

#labels, values = zip(*bins.items())
#indexes = np.arange(len(labels))
#width = 0.2

#plt.bar(indexes, values, width)
#plt.xticks(indexes + width * 0.1, labels, rotation='vertical')
#plt.savefig("Hist.png", format='png')
'''

'''
print len(list(set(df[df['Thrashing'] == True]['user'].values.tolist())))
#/float(df['Thrashing'].values.tolist().count(False) + df['Thrashing'].values.tolist().count(True))
print len(df['Thrashing'].values.tolist())
exit()
d = df[['totalCores', 'uniqHosts', 'Resource_List.naccesspolicy']]
d1 = d[d['totalCores'] == 8]
for item in (list(set(d1['uniqHosts'].values.tolist()))):
	print item, (list((d1['uniqHosts'].values.tolist()))).count(item), \
		    (list(set(d1['Resource_List.naccesspolicy'].values.tolist()))), \
		    (list((d1['Resource_List.naccesspolicy'].values.tolist()))).count('shared'),\
		    (list((d1['Resource_List.naccesspolicy'].values.tolist()))).count('share'),\
		    (list((d1['Resource_List.naccesspolicy'].values.tolist()))).count('-NA-')
			

print "Here"
d2 = d[d['totalCores'] == 16]
for item in (list(set(d2['uniqHosts'].values.tolist()))):
	print item, (list((d2['uniqHosts'].values.tolist()))).count(item),\
		    (list(set(d2['Resource_List.naccesspolicy'].values.tolist()))), \
		    (list((d2['Resource_List.naccesspolicy'].values.tolist()))).count('shared'),\
		    (list((d2['Resource_List.naccesspolicy'].values.tolist()))).count('share'),\
		    (list((d2['Resource_List.naccesspolicy'].values.tolist()))).count('-NA-')

exit()
ulist =  list(set(df['OriginalUser'].values.tolist()))

flist = ['User293', "User270", "User168", "User53", "User163", "User169", "User263", "User275", "User32"]
mydf = orig[['OriginalUser', 'user', 'JobGrp']]
for item in flist:
	print mydf[mydf['user']== item].values.tolist()[0]
	print set(mydf[mydf['user']== item]['JobGrp'].values.tolist())
	

raw_input()

count = 0
for item in ulist:
	if ("cms" in item) or ("nano" in item) or ("nemotest" in item):
		print item
		df  = orig
		df  = df[(df['OriginalUser'] == item)]
		dt  = df[(df['Resource_List.naccesspolicy'] == "shared")]
		count += len(list(set(dt['JobID'].values.tolist())))

print count 


#print list(set(dt['user'].values.tolist()))
raw_input()

policyList =  (list(set(df['Resource_List.naccesspolicy'].values.tolist())))

for item in policyList:
	print item, df['Resource_List.naccesspolicy'].values.tolist().count(item)

raw_input()
i
print len (list(set(df['user'].values.tolist())))
df  = df[df['user'] == "User150"]
jobIDs = df['JobID'].values.tolist()
jobGrps= df[df['JobGrp']!= "-NA-"]['JobGrp'].values.tolist()

print list(set(jobGrps))

print len(jobIDs)

count = 0
for filename in os.listdir(sys.argv[2]):
	if str("   ") in filename:
		print filename
		count +=1
		if count == 10:
			break
'''
'''
fakename = ["User235", "User150", "User178", "User8", "User51", "User121", "User26", "User61", "User9", "User98", "User51", "User174", "User208", "User87", "User129", "User52", "User116", "User96", "User274", "User151", "User262", "User107", "User183"]

for username in fakename:
	user = val[val['user'] == username]
	print user.shape
	print user.head(1)
	raw_input()


raw_input()

val = filter(lambda x: x != "-NA-", val)

l = range(0, 3596)
x = (list(set(val)))

for item in x:
	try:
		l.remove(int(item))
	except:
		print item
		print l.count(item)
		raw_input()
print l

raw_input()
'''
#val = df['PeakPgFlt'].values.tolist()
#val = df['Thrashing'].values.tolist()

#print list(set(val))
#print val.count(False), val.count(True)
#print len(filter(lambda x: x>int(sys.argv[2]), val))
#print len(filter(lambda x: x<=int(sys.argv[2]), val))

