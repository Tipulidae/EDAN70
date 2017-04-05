import sys
from os import listdir
from os.path import isfile, join

t = 0
realTempo = 500000
tempo = 500000
# Track, Time, Type, Channel, Note, Velocity
# 2, 960, Note_on_c, 1, 81, 81
# In header, assuming division = 480..

previousClock = 0
deltaT = 0



def parseNoteOnOff(note,isOn):
	return parseTime(int(note[1])) + parseType(isOn) + parseNote(note[4]) + parseVelocity(note[5])

def parseTime(time):
	global previousClock
	global tempo
	global realTempo
	global deltaT
	
	dt = deltaT + (time-previousClock)*tempo/realTempo
	previousClock = time
	deltaT = 0

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

def parseTempoChange(time, newtempo):
	global deltaT
	global tempo
	global previousClock
	global realTempo
	deltaT += (time-previousClock)*tempo/realTempo
	tempo = newtempo
	previousClock = time


def parseAllContentInFile(content):
	global previousClock
	global deltaT

	previousClock = 0
	deltaT = 2880
	data = ""
	
	for line in content:
		items = [x.strip('\n\t ').lower() for x in line.split(',')]
		if len(items) < 3:
			continue
		lineType = items[2]

		
	

		if lineType == 'note_on_c':
			output = parseNoteOnOff(items,True)
			#print str(items)+" -> "+output + ", length = "+str(len(output))
			data += output
		elif lineType == 'note_off_c':
			output = parseNoteOnOff(items,False)
			#print str(items)+" -> "+output + ", length = "+str(len(output))
			data += output
		elif lineType == 'tempo':
			#tempo = int(items[3])
			parseTempoChange(int(items[1]),int(items[3]))
			#print "tempo was changed to "+str(tempo)+"!"
		elif lineType[-2:] != '_c':
			continue
	
	return data

if __name__ == '__main__':
	PATH = 'csv/'
	datafile = 'output.data'
	if len(sys.argv) > 2:
		PATH = sys.argv[1]
		datafile = sys.argv[2]
	
	
	data = ""
	files = [f for f in listdir(PATH) if isfile(join(PATH,f))]
	for file in files:
		with open(join(PATH,file),'r') as f:
			data += parseAllContentInFile(f.readlines())
	
	
	with open(datafile,'w') as f:
		f.write(data)
		print "Parsed "+str(len(files))+" files, output written to "+datafile+"."




