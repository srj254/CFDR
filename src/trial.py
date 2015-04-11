#!/usr/bin/python

import os
import sys
import re
import pandas as pd


df  = pd.io.parsers.read_csv(sys.argv[1], sep='\t')
orig = df
ulist =  list(set(df['OriginalUser'].values.tolist()))

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

print len (list(set(df['user'].values.tolist())))
df  = df[df['user'] == "User150"]
jobIDs = df['JobID'].values.tolist()
jobGrps= df[df['JobGrp']!= "-NA-"]['JobGrp'].values.tolist()

print list(set(jobGrps))

print len(jobIDs)

count = 0
for filename in os.listdir(sys.argv[2]):
	if str("nrana") in filename:
		print filename
		count +=1
		if count == 10:
			break

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

