__author__ = 'robot'

from os import listdir
from os.path import isfile, join
from subprocess import call

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

DATA_DIR = 'res/'

files = [ DATA_DIR + f for f in listdir(DATA_DIR) if isfile(join('res',f)) ]

CLOTH_FILE = None
POINTS_CSV = None

for f in files:
    if f.endswith('.3ds'):
        CLOTH_FILE = f
    if f.endswith('.csv'):
        POINTS_CSV = f
    if CLOTH_FILE and POINTS_CSV:
        break

if not CLOTH_FILE:
    print(bcolors.FAIL + 'Could not find <file>.3ds' + bcolors.ENDC)

if not POINTS_CSV:
    print(bcolors.FAIL + 'Could not find points.csv' + bcolors.ENDC)

if CLOTH_FILE and POINTS_CSV:
    print(bcolors.OKGREEN + 'python3 simulate_all.py ' + CLOTH_FILE + ' ' + POINTS_CSV + bcolors.ENDC)
    call(['python3', 'simulate_all.py', CLOTH_FILE, POINTS_CSV])