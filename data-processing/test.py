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


def parseTime(time):
    msb = (time >> 7) & 127
    lsb = time & 127
    return chr(msb) + chr(lsb)

class Event:
    def __init__(self, t, dt, n, v):
        self.t = t
        self.dt = dt
        self.n = n
        self.v = v

    def createEntry(self, event):
        dur = event.t - self.t
        dur1, dur2 = parseTime(dur)
        dt1, dt2 = parseTime(self.dt)
        #return dt1 + dt2 + dur1 + dur2 + self.n
        ##return dt1 + dt2 + chr(1) + parseNote(self.n) + parseVelocity(self.v)
        return Entry(self.t,dur,self.n,self.v), Entry(event.t,dur,event.n, event.v)


class Entry:
    def __init__(self, t, dur, n, v):
        self.t = t
        self.n = n
        self.v = v
        self.dur = dur


      #readfile
        #readline
          #-create event (absolute time):
            #add to array
            #or
            #create entry
          #-tempo event:
            #update time

class Tempo:
    def __init__(self):
        self.realTempo = 500000
        self.tempo = 500000
        self.previousClock = 0
        self.previousTime = 0
        self.absoluteTime = 0

    def updateTime(self, time):
        self.absoluteTime += (time - self.previousClock) * self.tempo / self.realTempo


    def timeSinceLastEvent(self, time):
        self.updateTime(time)
        return time - self.previousTime

    def previousTime(self, time):
        self.previousTime = time

    def changeTempoEvent(self, time, newTempo):
        self.updateTime(time)
        self.tempo = newTempo

    def reset(self):
        self.previousClock = 0
        self.deltaT = 2880

'''
def parseNoteOnOff(t, note, isOn):
    return parseTime(t, int(note[1])) + parseType(isOn) + parseNote(note[4]) + parseVelocity(note[5])


def parseTime(t, time):
    dt = t.timeSinceLastEvent(time)

    if dt < 0 or dt > 32767:
        print "WARNING! Something went wrong with dt! dt = " + str(dt) + ". Proceeding anyway..."
    msb = (dt >> 7) & 127
    lsb = dt & 127
    # print "msb = "+str(msb)+", lsb = "+str(lsb)
    return chr(msb) + chr(lsb)'''


def parseType(isOn):
    if isOn:
        return chr(1)
    else:
        return chr(0)


def parseNote(note):
    return chr(int(note) & 127)


def parseVelocity(vel):
    return chr(int(vel) & 127)


def parseTempoChange(t, time, newTempo):
    t.changeTempoEvent(time, newTempo)


def parseAllContentInFile(t, content):
    t.reset()
    playing = dict()
    entries = []

    for line in content:
        items = [x.strip('\n\t ').lower() for x in line.split(',')]
        if len(items) < 3:
            continue
        lineType = items[2]

        if lineType.startswith('note_'):
            note = items[4]
            dt = t.timeSinceLastEvent(int(items[1]))
            e = Event(t.absoluteTime, dt,note,items[5])

            if note in playing:
                e1, e2 = playing[note].createEntry(e)
                entries.append(e1)
                entries.append(e2)
                del playing[note]
            else:
                playing[note] = e

            '''output = parseNoteOnOff(t, items, True)
            # print str(items)+" -> "+output + ", length = "+str(len(output))
            data += output
        elif lineType == 'note_off_c':
            output = parseNoteOnOff(t, items, False)
            # print str(items)+" -> "+output + ", length = "+str(len(output))
            data += output '''
        elif lineType == 'tempo':
            # tempo = int(items[3])
            parseTempoChange(t, int(items[1]), int(items[3]))
        # print "tempo was changed to "+str(tempo)+"!"
        elif lineType[-2:] != '_c':
            continue

    entries.sort(key=lambda e: e.t, reverse=True)
    return parseDataFromEntries(entries)

def parseDataFromEntries(entries):
    data = ""
    t = 0
    for e in entries:
        dt = e.t - t
        dur1, dur2 = parseTime(e.dur)
        dt1, dt2 = parseTime(dt)
        t = e.t
        data += dt1 + dt2 + chr(1) + parseNote(e.n) + parseVelocity(e.v)

    return data

if __name__ == '__main__':
    PATH = '/home/stag/EDAN70/csv/small'
    datafile = 'output.data'
    if len(sys.argv) > 2:
        PATH = sys.argv[1]
        datafile = sys.argv[2]

    data = ""
    t = Tempo()
    files = [f for f in listdir(PATH) if isfile(join(PATH, f))]
    for file in files:
        with open(join(PATH, file), 'r') as f:
            data += parseAllContentInFile(t, f.readlines())

    with open(datafile, 'w') as f:
        f.write(data)
        print "Parsed " + str(len(files)) + " files, output written to " + datafile + "."





