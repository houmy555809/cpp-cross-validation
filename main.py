import os
import sys
import multiprocessing
import signal

from colorama import *
import lib.main

signal.signal(signal.SIGINT, lib.main.signal_handler)

if len(sys.argv) < 4:
    print(
"""Usage:
cval judge datagen naive solution [--preset-validator=noip] [--validator-py=path/to/validator.py] [--testlib-checker=path/to/compiled_checker] [--timelimit=1] [--timelimita=1] [--timelimitb=1] [--cases=-1] [--stop|-s] [--nonstop|-n] [--no-time-limit|-t] [--no-time-limit-a|-A] [--no-time-limit-b|-B]
cval bench datagen prog [--timelimit=1] [--cases=-1] [--stop|-s] [--nonstop|-n]
cval test prog inpfile ansfile [--timelimit=1] [--preset-validator=noip] [--validator-py=path/to/validator.py] [--testlib-checker=path/to/compiled_checker] [--no-time-limit|-t] [--timelimit=1]
cval diff prog1 prog2
"""
    )
    exit(-1)
elif len(sys.argv) >= 4 and sys.argv[1] == "bench":
    datagen = sys.argv[2]
    prog = sys.argv[3]
    tl = 1
    cases = -1
    stop = True
    for i in range(4, len(sys.argv)):
        if '=' in sys.argv[i]:
            dat = sys.argv[i].split("=")
            if dat[0] == "--timelimit":
                tla = float(dat[1])
            elif dat[0] == "--cases":
                cases = int(dat[1])
            else:
                print(Fore.RED + "Fatal: Unsupported argument '" + sys.argv[i] + "'." + Style.RESET_ALL)
                exit(-1)
        else:
            if sys.argv[i] == "--stop" or sys.argv[i] == "-s":
                stop = True
            elif sys.argv[i] == "--nonstop" or sys.argv[i] == "-n":
                stop = False
            else:
                print(Fore.RED + "Fatal: Unsupported argument '" + sys.argv[i] + "'." + Style.RESET_ALL)
                exit(-1)
    lib.main.bench(datagen, prog, tl, cases, stop)
    exit(0)
elif len(sys.argv) >= 5 and sys.argv[1] == "judge":
    datagen = sys.argv[2]
    proga = sys.argv[3]
    progb = sys.argv[4]
    validator = "python3 ~/.cvaldata/validators/noip.py"
    tla = tlb = 1
    cases = -1
    stop = True
    for i in range(5, len(sys.argv)):
        if '=' in sys.argv[i]:
            dat = sys.argv[i].split("=")
            if dat[0] == "--preset-validator":
                validator = "python3 ~/.cvaldata/validators/" + dat[1] + ".py"
            elif dat[0] == "--validator-py":
                validator = "python3 " + dat[1]
            elif dat[0] == "--testlib-checker":
                validator = dat[1]
            elif dat[0] == "--cases":
                cases = int(dat[1])
            elif dat[0] == "--timelimit":
                tla = tlb = float(dat[1])
            elif dat[0] == "--timelimita":
                tla = float(dat[1])
            elif dat[0] == "--timelimitb":
                tlb = float(dat[1])
            else:
                print(Fore.RED + "Fatal: Unsupported argument '" + sys.argv[i] + "'." + Style.RESET_ALL)
                exit(-1)
        else:
            if sys.argv[i] == "--stop" or sys.argv[i] == "-s":
                stop = True
            elif sys.argv[i] == "--nonstop" or sys.argv[i] == "-n":
                stop = False
            elif sys.argv[i] == "--no-time-limit" or sys.argv[i] == "-t":
                print(Fore.YELLOW + "Warning: You enabled the --no-time-limit option. Running programs with infinite loop(s) in this mode can be extremely slow." + Style.RESET_ALL)
                tla = tlb = 114514
            elif sys.argv[i] == "--no-time-limit-a" or sys.argv[i] == "-A":
                print(Fore.YELLOW + "Warning: You enabled the --no-time-limit-a option. Running programs with infinite loop(s) in this mode can be extremely slow." + Style.RESET_ALL)
                tla = 114514
            elif sys.argv[i] == "--no-time-limit-b" or sys.argv[i] == "-B":
                print(Fore.YELLOW + "Warning: You enabled the --no-time-limit-b option. Running programs with infinite loop(s) in this mode can be extremely slow." + Style.RESET_ALL)
                tlb = 114514
            else:
                print(Fore.RED + "Fatal: Unsupported argument '" + sys.argv[i] + "'." + Style.RESET_ALL)
                exit(-1)
    lib.main.judge(datagen, proga, progb, validator, tla, tlb, cases, stop)
    exit(0)
elif len(sys.argv) >= 5 and sys.argv[1] == "test":
    prog = sys.argv[2]
    inpfile = sys.argv[3]
    ansfile = sys.argv[4]
    tl = 1
    validator = "python3 ~/.cvaldata/validators/noip.py"
    for i in range(5, len(sys.argv)):
        if '=' in sys.argv[i]:
            dat = sys.argv[i].split("=")
            if dat[0] == "--timelimit":
                tl = float(dat[1])
            elif dat[0] == "--preset-validator":
                validator = "python3 ~/.cvaldata/validators/" + dat[1] + ".py"
            elif dat[0] == "--validator-py":
                validator = "python3 " + dat[1]
            elif dat[0] == "--testlib-checker":
                validator = dat[1]
            else:
                print(Fore.RED + "Fatal: Unsupported argument '" + sys.argv[i] + "'." + Style.RESET_ALL)
                exit(-1)
        else:
            if sys.argv[i] == "--no-time-limit" or sys.argv[i] == "-t":
                print(Fore.YELLOW + "Warning: You enabled the --no-time-limit option. Running programs with infinite loop(s) in this mode can be extremely slow." + Style.RESET_ALL)
                tl = 114514
            else:
                print(Fore.RED + "Fatal: Unsupported argument '" + sys.argv[i] + "'." + Style.RESET_ALL)
                exit(-1)
    lib.main.test(prog, inpfile, ansfile, tl, validator)
    exit(0)
elif len(sys.argv) >= 4 and sys.argv[1] == "diff":
    lib.main.diff(sys.argv[2], sys.argv[3])
else:
    print(Fore.RED + "Fatal: Unsupported command '" + sys.argv[1] + "' or too less arguments." + Style.RESET_ALL)