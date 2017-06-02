import sys
from random import shuffle
from os import walk
from os.path import join
from shutil import copy

''' Randomly selects a small subsample of csv-files, using all composers available. '''

if __name__ == '__main__':
	SRC = './csv/Composers'
	DST = './csv/Small'
	filesToCopy = 50
	if len(sys.argv) > 3:
		SRC = sys.argv[1]
		DST = sys.argv[2]
		filesToCopy = int(sys.argv[3])
	
	allFiles = []
	for root,subdirs,files in walk(SRC):
		for csvfile in files:
			allFiles.append((root,csvfile))
	
	#for root,f in allFiles:
	#	print root,f

	shuffle(allFiles)
	count = 0
	for root,f in allFiles:
		if count >= filesToCopy:
			break

		copy(join(root,f),join(DST,f))
		print 'copied '+f
		count += 1

	print 'Total of '+str(count)+' files copied.'
	
	
