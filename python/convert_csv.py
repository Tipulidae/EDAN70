from os import listdir
from os.path import isfile, join
import subprocess

PATH = "/home/stag/EDAN70/midi"
EXPORT_PATH = "/home/stag/EDAN70/csv"


files = [f for f in listdir(PATH) if isfile(join(PATH, f))]

for f in files:
    subprocess.call(['midicsv', join(PATH, f), join(EXPORT_PATH, f)])

