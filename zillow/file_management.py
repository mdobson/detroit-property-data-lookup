#!/usr/local/bin/python3
import glob
import os

files = glob.glob('*.csv')

file_suffixes = [f[-21:-4] for f in files]
unique_file_suffixes = list(set(file_suffixes))

for suf in unique_file_suffixes:
	fhs = glob.glob('*%s*' % suf)	
	os.mkdir(suf)
	for fh in fhs:
		os.rename(fh, '%s/%s' % (suf, fh))
