
import sys

t = 0
# Track, Time, Type, Channel, Note, Velocity
# 2, 960, Note_on_c, 1, 81, 81


def processChunk(chunk):
	global t
	track = "2"
	dt = (ord(chunk[0])<<8) + (ord(chunk[1]))
	t += dt
	#print "chunk[0]="+str(ord(chunk[0]))+", chunk[1]="+str(ord(chunk[1]))
	#print "dt = "+str(dt)
	time = str(t)
	trackType = "-"
	if ord(chunk[2])&1 == 1:
		trackType = "Note_on_c"
	else:
		trackType = "Note_off_c"
	channel = "1"
	note = str(ord(chunk[3]))
	velocity = str(ord(chunk[4]))

	return ", ".join((track,time,trackType,channel,note,velocity))

if __name__ == '__main__':
	
	csvfile = 'output.csv'
	datafile = 'output.data'
	if len(sys.argv) > 2:
		datafile = sys.argv[1]
		csvfile = sys.argv[2]
	
	csv = ""

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
	
	with open(datafile) as f:
		data = f.read()
		n = len(data)
		pos = 0
		step = 5
		while pos <= n-step:

			chunk = data[pos:pos+step]
			pos += step

			csv += processChunk(chunk) + '\n'
	
	footer = "2, "+str(t)+", End_track\n" \
				+ "0, 0, End_of_file\n"

	with open(csvfile,'w') as f:
		f.write(header)
		f.write(csv)
		f.write(footer)
		print "data written to "+csvfile







