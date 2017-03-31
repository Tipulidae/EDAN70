
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

	return ",".join((track,time,trackType,channel,note,velocity))



csv = ""
with open('data.txt') as f:
	data = f.read()
	n = len(data)
	pos = 0
	step = 5
	while pos <= n-step:

		chunk = data[pos:pos+step]
		pos += step

		csv += processChunk(chunk) + '\n'
		

with open('output.csv','w') as f:
	f.write(csv)
	print "data written to output.csv"