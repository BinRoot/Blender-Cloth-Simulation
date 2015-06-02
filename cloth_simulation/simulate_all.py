__author__ = 'robot'

import sys
import csv
import os
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

print("argv: " + str(sys.argv))
if not (len(sys.argv) == 3):
    print(bcolors.FAIL + "[ ✘ ] Usage: python3 simulate_all.py <file>.3ds points.csv" + bcolors.ENDC)
    sys.exit(0)

POINTS_CSV = sys.argv[-1]
CLOTH_FILE = sys.argv[-2]

with open(POINTS_CSV, 'r', newline='', encoding='utf8') as csvfile:
    csvreader = csv.reader(csvfile)
    rows = list(csvreader)
    total_rows = len(rows)
    for i, row in enumerate(rows):
        progress_str = bcolors.OKBLUE + '[' + str(i+1) + ' / ' + str(total_rows) + ']: ' + bcolors.ENDC
        print(progress_str + 'index ' + row[0])
        call(['blender', '--background', '--python', 'simulate.py', CLOTH_FILE, row[0]])
