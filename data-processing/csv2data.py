import sys
from os import listdir
from os import walk
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
		self.composer = 0


	def turnOff(self, t):
		self.duration = t-self.startTime

	def toData(self,t,datatype):
		if datatype == 'd1':
			return timeToData(self.startTime-t)+timeToData(self.duration)+noteToData(self.note)+chr(128)
		elif datatype == 'd2':
			return timeToData(self.startTime-t)+timeToData(self.duration)+noteToData(self.note)+velocityToData(self.velocity)+chr(128)
		elif datatype == 'd3':
			return timeToData(self.startTime-t)+timeToData(self.duration)+noteToData(self.note)+composerToData(self.composer)+chr(128)
		elif datatype == 'd4':
			return (timeToData(self.startTime-t)+timeToData(self.duration)+noteToData(self.note)+
				velocityToData(self.velocity)+composerToData(self.composer)+chr(128))
		else:
			return ''




def parseNoteEvent(tempo, notes, items):
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
	

def timeToData(t):
	if t < 0 or t > 32767:
		print 'WARNING! Something went wrong with dt! dt = '+str(t)+'. Proceeding anyway...'
	msb = (t>>7)&127
	lsb = t&127
	return validate(chr(msb))+validate(chr(lsb))

def noteToData(note):
	return validate(chr(int(note)&127))

def velocityToData(vel):
	return validate(chr(int(vel)&127))

def composerToData(comp):
	return validate(chr(int(comp)&127))

def parseTempoChange(tempo, time, newTempo):
	tempo.changeTempoEvent(time,newTempo)

def validate(b):
	if b == chr(128):
		return chr(127)
	else:
		return b




def parseAllContentInFile(tempo, content, datatype, filename):
	
	notes = {}
	composerNames = ['albeniz','bach','balakirew','beethoven',
			'borodin','brahms','burgmueller','buergmueller','chopin','clementi','debussy','godowsky',
			'granados','grieg','haydn','liszt','mendelssohn','moszkowski','mozart',
			'mussorgsky','mussorgski','rachmaninov','rachmaninow','rachmaninoff','ravel','schubert','schumann','sinding',
			'tchaikovsky','tschaikowsky']
	composers = {name: False for name in composerNames}
	composerId = {composerNames[i]: i for i in range(len(composerNames))}
	composerId['buergmueller'] = composerId['burgmueller']
	composerId['mussorgski'] = composerId['mussorgsky']
	composerId['rachmaninow'] = composerId['rachmaninoff'] = composerId['rachmaninov']
	composerId['tschaikowsky'] = composerId['tchaikovsky']
	entries = []

	composer = 0
	
	for line in content:
		items = [x.strip('\n\t ').lower() for x in line.split(',')]
		if len(items) < 3:
			continue
		lineType = items[2]


		if lineType in ['note_on_c', 'note_off_c']:
			n = parseNoteEvent(tempo, notes, items)
			if n is not None:
				entries.append(n)
		elif lineType == 'tempo':
			parseTempoChange(tempo,int(items[1]),int(items[3]))
		elif lineType in ['text_t','title_t']:
			for w in items[3].split(' '):
				w = w.strip('":.,')
				if w in composers:
					composers[w] = True
					composer = composerId[w]
		elif lineType[-2:] != '_c':
			continue
	
	for note in entries:
		note.composer = composer

	entries.sort(key=lambda x: x.startTime, reverse=False)
	t = tempo.fileStartTime
	data = ''
	for note in entries:
		data += note.toData(t,datatype)
		t = note.startTime

	tempo.reset()

	#print str(sum(composers.values()))
	if sum(composers.values()) != 1:
		print 'WARNING: Composer not recognized for file '+filename

	return data


if __name__ == '__main__':
	INPUT = 'csv/'
	OUTPUT = 'output'
	datatype = 'd1'
	if len(sys.argv) > 3:
		INPUT = sys.argv[1]
		OUTPUT = sys.argv[2]
		datatype = sys.argv[3]
	
	data = ''
	tempo = Tempo()
	fileCount = 0
	for root,subdirs,files in walk(INPUT):
		for csvfile in files:
			with open(join(root,csvfile),'r') as f:
				data += parseAllContentInFile(tempo, f.readlines(),datatype,join(root,csvfile))
				fileCount += 1
	
	with open(OUTPUT+'.'+datatype,'w') as f:
		f.write(data)
		print 'Parsed '+str(fileCount)+' files, output written to '+OUTPUT+'.'+datatype+'.'
	
	
	



