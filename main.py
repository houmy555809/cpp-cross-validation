import os
import sys
import multiprocessing

from colorama import *
import lib.main

if len(sys.argv) == 1:
    print("""Usage: cval datagen naive solution [--preset-validator=noip] [--validator-py=path/to/noip.py] [--timelimit=1] [--cases=-1] [--stop|-s] [--nonstop|-n] [--no-time-limit|-t]""")
    exit(-1)
elif len(sys.argv) >= 4:
    datagen = sys.argv[1]
    proga = sys.argv[2]
    progb = sys.argv[3]
    validator = "~/.cval/validators/noip.py"
    tl = 1
    cases = -1
    stop = True
    for i in range(4, len(sys.argv)):
        if '=' in sys.argv[i]:
            dat = sys.argv[i].split("=")
            if dat[0] == "--preset-validator":
                validator = "~/.cval/validators/" + dat[1] + ".py"
            elif dat[0] == "--validator-py":
                validator = dat[1]
            elif dat[0] == "--cases":
                cases = int(dat[1])
            elif dat[0] == "--timelimit":
                tl = float(dat[1])
        else:
            if sys.argv[i] == "--stop" or sys.argv[i] == "-s":
                stop = True
            elif sys.argv[i] == "--nonstop" or sys.argv[i] == "-n":
                stop = False
            elif sys.argv[i] == "--no-time-limit" or sys.argv[i] == "-t":
                tl = 114514
    lib.main.work(datagen, proga, progb, validator, tl, cases, stop)
    exit(0)