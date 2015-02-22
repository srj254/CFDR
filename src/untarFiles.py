#!/usr/bin/python

import os
import sys



for root, dirnames, filenames in os.walk(sys.argv[1]):
	for filename in filenames:
		if filename.endswith(".tgz") or filename.endswith('.tar.gz'):
			f = (os.path.join(root, filename))
			print f
			os.system ("tar -xzf "+ f+ " -C "+ root)
		elif filename.endswith(".gz"):
			f = (os.path.join(root, filename))
			print f
			os.system ("gunzip "+ f)
		
