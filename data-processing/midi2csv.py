import os
from os.path import isfile, join
import sys
import subprocess
import shlex

''' Converts midi-files in the specified directory (and subdirectories)
	from midi to csv. '''


if len(sys.argv) > 1:
	rootdir = sys.argv[1]
else:
	print 'Input-folder unspecified, using current folder.'
	rootdir = "./"

count = 0
for subdir, dirs, files in os.walk(rootdir):
	for midifile in files:
		file = midifile.split(".")
		if file[-1].lower().lstrip() == "mid":
			print 'path is %s . %s' % (file[0], file[-1])
			midipath = join(subdir, midifile)
			csvpath = join(subdir, file[0] + ".csv")
			cmd = 'midicsv "{}" "{}"'.format(midipath, csvpath)
			subprocess.call(shlex.split(cmd))
			count += 1

print 'converted {} files.'.format(count)