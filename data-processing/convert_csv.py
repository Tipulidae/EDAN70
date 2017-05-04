from os import listdir
from os.path import isfile, join
import subprocess

PATH = "midi"
EXPORT_PATH = "csv"

files = [f for f in listdir(PATH) if isfile(join(PATH, f))]

temp = 0
for f in files:
    subprocess.call(['midicsv', join(PATH, f), join(EXPORT_PATH, f[:-3] + "csv")])
    temp += 1

print 'converted {} files.'.format(temp)


