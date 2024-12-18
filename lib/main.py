import os, sys
import shutil
import multiprocessing
import time
import datetime
from colorama import *

current_proc_id = None

def cprint(color, text, end = "\n"):
    print(color + text + Style.RESET_ALL, end = end)

def find_proc(proc_id):
    if os.name != "posix":
        print(Fore.RED + "Fatal: cannot run program out of Linux environment." + Style.RESET_ALL)
        exit(-1)
    os.system("ps a | grep " + str(proc_id) + " > data.txt")
    with open("data.txt","r") as file:
        data = file.readlines()[0].strip().split()
        if data[-1] == "data.txt":# ... grep --color=auto [proc_id] > data.txt
            return False
    return True

def kill_proc(proc_id):
    if not find_proc(proc_id):
        return False
    os.system("kill " + str(proc_id))
    return True

def start_proc(proc, name):
    if os.name != "posix":
        print(Fore.RED + "Fatal: cannot run program out of Linux environment." + Style.RESET_ALL)
        exit(-1)
    os.system(proc + " &")
    # get pid
    os.system("ps a | grep '" + name + "' > data.txt")
    pid = None
    with open("data.txt","r") as file:
        for line in file.readlines():
            data = line.strip().split()
            #print(line.strip())
            if " ".join(data[4:]).strip().startswith(name):
                pid = int(data[0])
                break
        file.close()
    return pid
    
def do_proc(proc_name, name, tl = 1):
    pid = start_proc(proc_name, name)
    for i in range(int(tl)):
        time.sleep(1)
        if not find_proc(pid):
            return "OK"
    time.sleep(tl - int(tl))
    if kill_proc(pid):
        return "TLE"
    else:
        return "OK"

def parse_validator_report(filename):
    with open(filename, "r") as file:
        content = "\n".join(file.readlines())
        judgement = content.split()[0]
        desc = " ".join(content.split()[1:])
        file.close()
    return (judgement,desc)

num_cases, num_errors = 0, 0

def _workonce(datagen, proga, progb, validator, timelimit = 1):
    global num_cases
    cprint(Fore.WHITE, str(num_cases + 1) + " Initialize...          ", end = "")
    proga_out_file = proga + ".out"
    progb_out_file = progb + ".out"
    tle=False
    cprint(Fore.WHITE, "\r" + str(num_cases + 1) + " Gen data...          ", end = "")
    do_proc(datagen + " > data.in", datagen, tl = 1)
    cprint(Fore.WHITE, "\r" + str(num_cases + 1) + " Run program 1...          ", end = "")
    if do_proc(proga + " < data.in > " + proga_out_file, proga, timelimit) == "TLE":
        tle=True
    cprint(Fore.WHITE, "\r" + str(num_cases + 1) + " Run program 2...          ", end = "")
    if do_proc(progb + " < data.in > " + progb_out_file, progb, timelimit) == "TLE":
        tle=True
    if not tle:
        cprint(Fore.WHITE, "\r" + str(num_cases + 1) + " Validate...          ", end = "")
        do_proc("python3 " + validator + " " + proga_out_file + " " + progb_out_file + " > validator_report.txt", "python3", tl = 1)
        return parse_validator_report("validator_report.txt")
    else:
        with open("validator_report.txt","w") as file:
            file.write("TLE Time Limit Exceeded.")
            file.close()
        return ("TLE", "Time Limit Exceeded.")

def workonce(caseid, datagen, proga, progb, validator, timelimit = 1, stop = True):
    global num_cases, num_errors
    res = _workonce(datagen, proga, progb, validator, timelimit)
    cprint(Fore.GREEN + Style.BRIGHT if res[0] == "AC" else Fore.RED, "\r" + str(caseid) + " " + res[0] + " " + res[1])
    num_cases += 1
    if res[0] != "AC": # if not pass
        num_errors += 1
        os.mkdir("report/" + str(num_cases))
        shutil.copyfile("data.in", "report/" + str(num_cases) + "/data.in")
        shutil.copyfile(proga + ".out", "report/" + str(num_cases) + "/" + proga + ".out")
        shutil.copyfile(progb + ".out", "report/" + str(num_cases) + "/" + progb + ".out")
        shutil.copyfile("validator_report.txt", "report/" + str(num_cases) + "/validator_report.txt")
        if stop:
            cprint(Fore.WHITE, "Done. Total %d error(s) in %d case(s). See report at report/ ." % (num_errors, num_cases))
            exit(1)

def _bench(datagen, prog, timelimit = 1):
    cprint(Fore.WHITE, "\rGen data...          ", end = "")
    do_proc(datagen + "> data.in", datagen, tl = 1)
    cprint(Fore.WHITE, "\rExec program...          ", end = "")
    if do_proc(prog + " < data.in > " + prog + ".out", prog, tl = timelimit) == "TLE":
        cprint(Fore.RED, "\rTLE Time Limit Exceeded.")
    else:
        cprint(Style.BRIGHT + Fore.GREEN, "\rPASS Process terminated within time limit.")

def bench(datagen, prog, timelimit = 1):
    _bench(datagen, prog, timelimit)

def judge(datagen, proga, progb, validator, timelimit = 1, cases = -1, stop = True):
    global num_cases, num_errors
    # clear last report
    os.system("rm -rf report")
    os.mkdir("report")
    # do main proc
    num_cases = 0
    if cases == -1:
        cid = 0
        while True:
            cid += 1
            workonce(cid, datagen, proga, progb, validator, timelimit, stop)
    else:
        for i in range(1, cases + 1):
            workonce(i, datagen, proga, progb, validator, timelimit, stop)
    cprint(Fore.WHITE, "Done. Total %d error(s) in %d case(s). See report at report/ ." % (num_errors, num_cases))