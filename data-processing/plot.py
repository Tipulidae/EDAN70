import torchfile
from matplotlib import pyplot as plt
import numpy as np
from collections import OrderedDict as od
import sys

if len(sys.argv) > 2:
	path = sys.argv[1]
	name = sys.argv[2]


m = torchfile.load(path)

#print len(m['train_losses'])
#print m['train_losses'][10]
#print m['val_losses']


XT = np.linspace(0, len(m['train_losses']), len(m['train_losses']))
T = m['train_losses']

V = od(sorted(m['val_losses'].items()))
XV = np.fromiter(V, np.float32)
V = np.fromiter(iter(V.values()), np.float32)
#print XV
#print "values: %s" % V

fig = plt.figure()
fig.suptitle(name)
train_line, = plt.plot(XT, T, label="Training Error")
val_line, = plt.plot(XV, V, '*-', label="Val Error", linewidth=4)
plt.legend(handles=[train_line, val_line])
plt.xlabel('iterations')
plt.ylabel('error')

fig.savefig(name+'.png')
plt.show()