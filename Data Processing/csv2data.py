# data = open('test.txt', 'r').read()

# for line in data:
# 	print line




t = 0
# Track, Time, Type, Channel, Note, Velocity
# 2, 960, Note_on_c, 1, 81, 81



def parseNoteOnOff(note,isOn):
	return parseTime(note[1]) + parseType(isOn) + parseNote(note[4]) + parseVelocity(note[5])

def parseTime(time):
	global t
	dt = int(time)-t
	t += dt
	if dt < 0 || dt > 131071:
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



data = ""
with open('test.txt') as f:
	content = f.readlines()
	for line in content:
		items = [x.strip('\n\t ').lower() for x in line.split(',')]
		if len(items) < 3:
			continue
		lineType = items[2]

		if lineType[-2:] != '_c':
			continue
		

		if lineType == 'note_on_c':
			output = parseNoteOnOff(items,True)
			#print str(items)+" -> "+output + ", length = "+str(len(output))
			data += output
		elif lineType == 'note_off_c':
			output = parseNoteOnOff(items,False)
			#print str(items)+" -> "+output + ", length = "+str(len(output))
			data += output

with open('data.txt','w') as f:
	f.write(data)
	print "data written to file:"
