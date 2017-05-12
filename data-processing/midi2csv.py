from os import listdir
from os.path import isfile, join
import subprocess
import shlex

PATH = "midi"
EXPORT_PATH = "csv"

files = [f for f in listdir(PATH) if isfile(join(PATH, f))]

temp = 0
for f in files:
    #subprocess.call(['midicsv', join(PATH, f), join(EXPORT_PATH, f[:-3] + "csv")])
    cmd = 'midicsv {} {}'.format(join(PATH, f), join(EXPORT_PATH, f[:-3] + "csv"))
    subprocess.call(shlex.split(cmd))
    temp += 1

print 'converted {} files.'.format(temp)