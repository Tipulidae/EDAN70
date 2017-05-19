import os
from os.path import isfile, join
import sys
import subprocess
import shlex


#PATH = "midi"
#EXPORT_PATH = "csv"
#
#files = [f for f in os.listdir(PATH) if isfile(join(PATH, f))]
#
#temp = 0
#for f in files:
#    #subprocess.call(['midicsv', join(PATH, f), join(EXPORT_PATH, f[:-3] + "csv")])
#    cmd = 'midicsv {} {}'.format(join(PATH, f), join(EXPORT_PATH, f[:-3] + "csv"))
#    subprocess.call(shlex.split(cmd))
#    temp += 1
#
#print 'converted {} files.'.format(temp)


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