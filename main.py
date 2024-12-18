import os
import sys
import multiprocessing

from colorama import *
import lib.main

if len(sys.argv) < 4:
    print(
"""Usage:
cval judge datagen naive solution [--preset-validator=noip] [--validator-py=path/to/noip.py] [--timelimit=1] [--cases=-1] [--stop|-s] [--nonstop|-n] [--no-time-limit|-t]
cval bench datagen prog [--timelimit=1]
"""
    )
    exit(-1)
elif len(sys.argv) >= 4 and sys.argv[1] == "bench":
    datagen = sys.argv[2]
    prog = sys.argv[3]
    tl = 1
    for i in range(4, len(sys.argv)):
        if '=' in sys.argv[i]:
            dat = sys.argv[i].split("=")
            if dat[0] == "--timelimit":
                tl = float(dat[1])
            else:
                print(Fore.RED + "Fatal: Unsupported argument '" + sys.argv[i] + "'." + Style.RESET_ALL)
                exit(-1)
        else:
            print(Fore.RED + "Fatal: Unsupported argument '" + sys.argv[i] + "'." + Style.RESET_ALL)
            exit(-1)
    lib.main.bench(datagen, prog, tl)
    exit(0)
elif len(sys.argv) >= 5 and sys.argv[1] == "judge":
    datagen = sys.argv[2]
    proga = sys.argv[3]
    progb = sys.argv[4]
    validator = "~/.cval/validators/noip.py"
    tl = 1
    cases = -1
    stop = True
    for i in range(5, len(sys.argv)):
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
                print(Fore.RED + "Fatal: Unsupported argument '" + sys.argv[i] + "'." + Style.RESET_ALL)
                exit(-1)
        else:
            if sys.argv[i] == "--stop" or sys.argv[i] == "-s":
                stop = True
            elif sys.argv[i] == "--nonstop" or sys.argv[i] == "-n":
                stop = False
            elif sys.argv[i] == "--no-time-limit" or sys.argv[i] == "-t":
                tl = 114514
            else:
                print(Fore.RED + "Fatal: Unsupported argument '" + sys.argv[i] + "'." + Style.RESET_ALL)
                exit(-1)
    lib.main.judge(datagen, proga, progb, validator, tl, cases, stop)
    exit(0)
else:
    print(Fore.RED + "Fatal: Unsupported command '" + sys.argv[1] + "'." + Style.RESET_ALL)