import sys
#import matplotlib.pyplot as plt
#import numpy as np
from os import listdir
from os.path import isfile, join




class Tempo:
	
	def __init__(self):
		self.realTempo = 500000
		self.tempo = 500000
		self.previousClock = 0
		self.absoluteTime = 0
		self.fileStartTime = 0

	def getAbsoluteTime(self, time):
		self.handleEvent(time)
		return self.absoluteTime

	def changeTempoEvent(self, time, newTempo):
		self.handleEvent(time)
		self.tempo = newTempo

	def handleEvent(self, time):
		self.absoluteTime += (time-self.previousClock)*self.tempo/self.realTempo
		self.previousClock = time

	def reset(self):
		self.previousClock = 0
		self.absoluteTime += 2880
		self.fileStartTime  = self.absoluteTime

class Note:
	def __init__(self, t, n, v):
		self.startTime = t
		self.duration = 0
		self.note = n
		self.velocity = v


	def turnOff(self, t):
		self.duration = t-self.startTime





def parseNote(tempo, notes, items):
	t = tempo.getAbsoluteTime(int(items[1]))
	lineType = items[2]
	note = items[4]
	velocity = int(items[5])
	
	if lineType == 'note_on_c' and velocity > 0:
		notes[note] = Note(t,note,velocity)
	elif note in notes:
		notes[note].turnOff(t)
		return notes[note]

	return None
	

def parseTime(t):
	if t < 0 or t > 32767:
		print "WARNING! Something went wrong with dt! dt = "+str(t)+". Proceeding anyway..."
	msb = (t>>7)&127
	lsb = t&127
	return validate(chr(msb))+validate(chr(lsb))

def parseNote2(note):
	return validate(chr(int(note)&127))

def parseVelocity(vel):
	return validate(chr(int(vel)&127))

def parseTempoChange(tempo, time, newTempo):
	tempo.changeTempoEvent(time,newTempo)

def validate(b):
	if b == chr(1):
		return chr(0)
	else:
		return b


def parseAllContentInFile(tempo, content):
	
	notes = {}
	entries = []
	
	for line in content:
		items = [x.strip('\n\t ').lower() for x in line.split(',')]
		if len(items) < 3:
			continue
		lineType = items[2]


		if lineType in ['note_on_c', 'note_off_c']:
			n = parseNote(tempo, notes, items)
			if n is not None:
				entries.append(n)
		elif lineType == 'tempo':
			parseTempoChange(tempo,int(items[1]),int(items[3]))
		elif lineType[-2:] != '_c':
			continue
	
	entries.sort(key=lambda x: x.startTime, reverse=False)
	t = tempo.fileStartTime
	data = ""
	for note in entries:
		#data += ';'.join(map(str,[note.startTime-t,note.duration,note.note]))+";-"
		data += parseTime(note.startTime-t)+parseTime(note.duration)+parseNote2(note.note)+chr(1)
		#print str(note.startTime-t) + " - " + str(note.duration) + " - " + note.note
		t = note.startTime

	tempo.reset()
	#print data
	
	"""
	ds = np.array(map(lambda x: x.duration, entries))
	plt.hist(ds, bins='auto')
	plt.show()"""

	return data

"dt;duration;note;-dt;duration;note;-"

if __name__ == '__main__':
	PATH = 'csv/'
	datafile = 'output.data'
	if len(sys.argv) > 2:
		PATH = sys.argv[1]
		datafile = sys.argv[2]
	
	
	data = ""
	tempo = Tempo()
	files = [f for f in listdir(PATH) if isfile(join(PATH,f))]
	for file in files:
		with open(join(PATH,file),'r') as f:
			data += parseAllContentInFile(tempo, f.readlines())
	
	
	with open(datafile,'w') as f:
		f.write(data)
		print "Parsed "+str(len(files))+" files, output written to "+datafile+"."
	
	
	



