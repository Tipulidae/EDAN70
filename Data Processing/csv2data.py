import sys
from os import listdir
from os.path import isfile, join


"""
t = 0
realTempo = 500000
tempo = 500000
previousClock = 0
deltaT = 0
"""

class Tempo:
	
	def __init__(self):
		self.realTempo = 500000
		self.tempo = 500000
		self.previousClock = 0
		self.deltaT = 0
		
	
	def timeSinceLastEvent(self,time):
		dt = self.deltaT + (time-self.previousClock)*self.tempo/self.realTempo
		self.previousClock = time
		self.deltaT = 0
		return dt

	def changeTempoEvent(self, time, newTempo):
		self.deltaT += (time-self.previousClock)*self.tempo/self.realTempo
		self.tempo = newTempo
		self.previousClock = time
	
	def reset(self):
		self.previousClock = 0
		self.deltaT = 2880



def parseNoteOnOff(t,note,isOn):
	return parseTime(t,int(note[1])) + parseType(isOn) + parseNote(note[4]) + parseVelocity(note[5])

def parseTime(t,time):
	dt = t.timeSinceLastEvent(time)

	if dt < 0 or dt > 32767:
		print "WARNING! Something went wrong with dt! dt = "+str(dt)+". Proceeding anyway..."
	msb = (dt>>7)&127
	lsb = dt&127
	#print "msb = "+str(msb)+", lsb = "+str(lsb)
	return chr(msb)+chr(lsb)

def parseType(isOn):
	if isOn:
		return chr(1)
	else:
		return chr(0)

def parseNote(note):
	return chr(int(note)&127)

def parseVelocity(vel):
	return chr(int(vel)&127)

def parseTempoChange(t, time, newTempo):
	t.changeTempoEvent(time,newTempo)


def parseAllContentInFile(t, content):
	t.reset()
	data = ""
	
	for line in content:
		items = [x.strip('\n\t ').lower() for x in line.split(',')]
		if len(items) < 3:
			continue
		lineType = items[2]


		if lineType == 'note_on_c':
			output = parseNoteOnOff(t,items,True)
			#print str(items)+" -> "+output + ", length = "+str(len(output))
			data += output
		elif lineType == 'note_off_c':
			output = parseNoteOnOff(t,items,False)
			#print str(items)+" -> "+output + ", length = "+str(len(output))
			data += output
		elif lineType == 'tempo':
			#tempo = int(items[3])
			parseTempoChange(t,int(items[1]),int(items[3]))
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
	t = Tempo()
	files = [f for f in listdir(PATH) if isfile(join(PATH,f))]
	for file in files:
		with open(join(PATH,file),'r') as f:
			data += parseAllContentInFile(t, f.readlines())
	
	
	with open(datafile,'w') as f:
		f.write(data)
		print "Parsed "+str(len(files))+" files, output written to "+datafile+"."




