
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



def processChunk(notes, chunk, datatype):
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

	if datatype == 'd3':
		print "Composer: "+str(ord(chunk[5]))
	elif datatype == 'd4':
		print "Composer: "+str(ord(chunk[6]))


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
	with open(datafile) as f:
		data = f.read()
		for chunk in data.split(chr(128)):
			processChunk(notes,chunk,datatype)

		
	
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
	
	





