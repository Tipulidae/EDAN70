
import sys

t = 0

class Note:
	track = "2"
	channel = "1"
	
	def __init__(self, time, trackType, note):
		self.t = time
		self.trackType = trackType
		self.note = note
		self.velocity = "68"

	def toString(self):
		return ", ".join((Note.track,str(self.t),self.trackType,Note.channel,self.note,self.velocity))


class Composer:
	info = ""
	previousComposer = "no one"
	
	def __init__(self):
		self.composerNames = {0:'albeniz',
			 1:'bach',
			 2:'balakirew',
			 3:'beethoven',
			 4:'borodin',
			 5:'brahms',
			 6:'burgmueller',
			 8:'chopin',
			 9:'clementi',
			10:'debussy',
			11:'godowsky',
			12:'granados',
			13:'grieg',
			14:'haydn',
			15:'liszt',
			16:'mendelssohn',
			17:'moszkowski',
			18:'mozart',
			19:'mussorgsky',
			21:'rachmaninov',
			24:'ravel',
			25:'schubert',
			26:'schumann',
			27:'sinding',
			28:'tchaikovsky',
			29:'tschaikowsky'}
	
	def addComposerInfo(self,compId,timeInSeconds):
		if compId in self.composerNames:
			newComposer = self.composerNames[compId]
		else:
			newComposer = "invalid composer "+str(compId)

		if newComposer != self.previousComposer:
			m,s = divmod(timeInSeconds,60)
			h,m = divmod(m,60)
			theTime = "%d:%02d:%02d"%(h,m,s)
			self.info += "Composer changed at "+theTime+" from "+self.previousComposer+" to "+newComposer+"\n"
			self.previousComposer = newComposer
	
	def printInfo(self):
		return self.info

def processChunk(notes, chunk, datatype, composer):
	global t	

	n = len(chunk)
	if (datatype in ['d1'] and n != 5 or 
			datatype in ['d2', 'd3'] and n != 6 or
			datatype in ['d4'] and n != 7):
		print "invalid chunk length for datatype "+datatype+": "+str(n)
		return


	track = "2"
	startTimeDiff = (ord(chunk[0])<<7) + (ord(chunk[1]))
	t += startTimeDiff

	duration = (ord(chunk[2])<<7) + (ord(chunk[3]))

	note = str(ord(chunk[4]))
	noteOn = Note(t,"Note_on_c",note)
	noteOff = Note(t+duration,"Note_off_c",note)

	if datatype in ['d2','d4']:
		noteOn.velocity = str(ord(chunk[5]))

	


	compId = None
	timeInSeconds = (t-startTimeDiff)*0.5/480
	
	if datatype == 'd3':
		composer.addComposerInfo(ord(chunk[5]),timeInSeconds)
	elif datatype == 'd4':
		composer.addComposerInfo(ord(chunk[6]),timeInSeconds)

	notes.append(noteOn)
	notes.append(noteOff)




if __name__ == '__main__':
	csvfile = 'output.csv'
	datafile = 'output.d1'
	datatype = 'd1'
	if len(sys.argv) > 2:
		datafile = sys.argv[1]
		csvfile = sys.argv[2]
		datatype = datafile[-2:]

	header = "0, 0, Header, 1, 2, 480\n" \
			   + "1, 0, Start_track\n" \
				+ "1, 0, Title_t, \"Training data for RNN\"\n" \
				+ "1, 0, Text_t, \"All the music!\"\n" \
				+ "1, 0, Copyright_t, \"This file is in the public domain (ish)\"\n" \
				+ "1, 0, Time_signature, 4, 2, 24, 8\n" \
				+ "1, 0, Tempo, 500000\n" \
				+ "1, 0, End_track\n" \
				+ "2, 0, Start_track\n" \
				+ "2, 0, Instrument_name_t, \"Piano\"\n" \
				+ "2, 0, Program_c, 1, 0\n"
	
	notes = []
	words = dict()
	wordCount = 0

	composer = Composer()
	
	with open(datafile) as f:
		data = f.read()
		for chunk in data.split(chr(128)):
			processChunk(notes,chunk,datatype,composer)

	
	notes.sort(key=lambda x: x.t, reverse=False)
	t = notes[-1].t
	footer = "2, "+str(t)+", End_track\n" \
				+ "0, 0, End_of_file\n"

	with open(csvfile,'w') as f:
		f.write(header)
		for note in notes:
			f.write(note.toString()+'\n')

		f.write(footer)
		print "data written to "+csvfile
	

	print composer.info
	if composer.info:
		with open(csvfile+'.ci','w') as f:
			f.write(composer.info)
			print "composer info written to "+csvfile+".ci."
	




