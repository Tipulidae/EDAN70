
import sys

t = 0
# Track, Time, Type, Channel, Note, Velocity
# 2, 960, Note_on_c, 1, 81, 81

class Note:
	track = "2"
	channel = "1"
	velocity = "68"
	def __init__(self, time, trackType, note):
		self.t = time
		self.trackType = trackType
		self.note = note

	def toString(self):
		return ", ".join((Note.track,str(self.t),self.trackType,Note.channel,self.note,Note.velocity))



def processChunk(notes, chunk):
	global t
	track = "2"
	startTimeDiff = (ord(chunk[0])<<7) + (ord(chunk[1]))
	t += startTimeDiff

	duration = (ord(chunk[2])<<7) + (ord(chunk[3]))
	note = str(ord(chunk[4]))
	notes.append(Note(t,"Note_on_c",note))
	notes.append(Note(t+duration,"Note_off_c",note))




if __name__ == '__main__':
	csvfile = 'output.csv'
	datafile = 'output.data'
	if len(sys.argv) > 2:
		datafile = sys.argv[1]
		csvfile = sys.argv[2]

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

	with open(datafile) as f:
		data = f.read()
		n = len(data)
		pos = 0
		step = 5
		while pos <= n-step:

			chunk = data[pos:pos+step]
			pos += step

			processChunk(notes,chunk)
	
	notes.sort(key=lambda x: x.t, reverse=False)
	t = notes[-1].t
	footer = "2, "+str(t)+", End_track\n" \
				+ "0, 0, End_of_file\n"

	with open(csvfile,'w') as f:
		f.write(header)
		for note in notes:
			f.write(note.toString()+'\n')
		#f.write(csv)
		f.write(footer)
		print "data written to "+csvfile







