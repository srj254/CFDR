#!/usr/bin/python

import os
import sys
import re
import pandas as pd


df  = pd.io.parsers.read_csv(sys.argv[1], sep='\t')
orig = df
ulist =  list(set(df['OriginalUser'].values.tolist()))
print "Number of Total users: ", len(ulist)
print "Number of Total Jobs: ", len(df['OriginalUser'].values.tolist())
print "Total groups of jobs: ", len(list(set(df[df['JobGrp']!="-NA-"]['JobGrp'].values.tolist())))

