import sys

t = 0
# Track, Time, Type, Channel, Note, Velocity
# 2, 960, Note_on_c, 1, 81, 81



def parseNoteOnOff(note,isOn):
	return parseTime(note[1]) + parseType(isOn) + parseNote(note[4]) + parseVelocity(note[5])

def parseTime(time):
	global t
	dt = int(time)-t
	t += dt
	if dt < 0 or dt > 131071:
		print "WARNING! Something went wrong with dt! dt = "+str(dt)+". Proceeding anyway..."
	msb = (dt>>8)&255
	lsb = dt&255
	#print "msb = "+str(msb)+", lsb = "+str(lsb)
	return chr(msb)+chr(lsb)

def parseType(isOn):
	if isOn:
		return chr(1)
	else:
		return chr(0)

def parseNote(note):
	return chr(int(note)&255)

def parseVelocity(vel):
	return chr(int(vel)&255)


<<<<<<< HEAD

data = ""
with open('../csv/appass.csv') as f:
	content = f.readlines()
	for line in content:
		items = [x.strip('\n\t ').lower() for x in line.split(',')]
		if len(items) < 3:
			continue
		lineType = items[2]

		if lineType[-2:] != '_c':
			continue
=======
if __name__ == '__main__':

	#print 'Number of arguments:', len(sys.argv), 'arguments.'
	#print 'Argument List:', str(sys.argv)
	csvfile = 'test.txt'
	datafile = 'data.txt'
	if len(sys.argv) > 2:
		csvfile = sys.argv[1]
		datafile = sys.argv[2]
	
	
	data = ""
	with open(csvfile) as f:
		content = f.readlines()
		for line in content:
			items = [x.strip('\n\t ').lower() for x in line.split(',')]
			if len(items) < 3:
				continue
			lineType = items[2]

			if lineType[-2:] != '_c':
				continue
>>>>>>> 9b0606d15896f0135e2bf5727715f72d9ad62923
		

			if lineType == 'note_on_c':
				output = parseNoteOnOff(items,True)
				#print str(items)+" -> "+output + ", length = "+str(len(output))
				data += output
			elif lineType == 'note_off_c':
				output = parseNoteOnOff(items,False)
				#print str(items)+" -> "+output + ", length = "+str(len(output))
				data += output

	with open(datafile,'w') as f:
		f.write(data)
		print csvfile+" parsed and data written to "+datafile+"."




