import os, sys
import shutil
import multiprocessing
import time
import datetime
from colorama import *

def cprint(color, text, end = "\n"):
    print(color + text + Style.RESET_ALL, end = end)

def split_tokens(string, charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"):
    res = []
    cur = ""
    for i in string:
        if i in charset:
            cur += i
        else:
            if len(cur) > 0:
                res.append(cur)
                cur = ""
            res.append(i)
    res.append(cur)
    return res

def line_difference(lineA, lineB):
    # calculates the mininum changes (additions, deletions, modifications) to transform from lineA to lineB.
    lineA = split_tokens(lineA)
    lineB = split_tokens(lineB)
    dp = []
    for i in range(len(lineA) + 1):
        line = []
        for j in range(len(lineB)+ 1):
            line.append(float("inf"))
        dp.append(line)
    dp[0][0] = 0
    for i in range(1, len(lineA) + 1):
        dp[i][0] = i
    for i in range(1, len(lineB) + 1):
        dp[0][i] = i
    for i in range(1, len(lineA) + 1):
        for j in range(1, len(lineB) + 1):
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + (0 if lineA[i - 1] == lineB[j - 1] else 1))
    return dp[len(lineA)][len(lineB)]

def calc_line_difference(lineA, lineB):
    dp = []
    src = []
    for i in range(len(lineA) + 1):
        line = []
        sline = []
        for j in range(len(lineB) + 1):
            line.append(float("inf"))
            sline.append("")
        dp.append(line)
        src.append(sline)
    dp[0][0] = 0
    src[0][0] = None
    for i in range(1, len(lineA) + 1):
        dp[i][0] = dp[i - 1][0] + 1
        src[i][0] = "a"
    for i in range(1, len(lineB) + 1):
        dp[0][i] = dp[0][i - 1] + 1
        src[0][i] = "b"
    for i in range(1, len(lineA) + 1):
        for j in range(1, len(lineB) + 1):
            a = dp[i - 1][j] + 1
            b = dp[i][j - 1] + 1
            c = dp[i - 1][j - 1] + (0 if lineA[i - 1] == lineB[j - 1] else 2)
            dp[i][j] = min(a, b, c)
            if dp[i][j] == c and lineA[i - 1] == lineB[j - 1]:
                src[i][j] = "same"
            elif dp[i][j] == a:
                src[i][j] = "a"
            elif dp[i][j] == b:
                src[i][j] = "b"
            elif dp[i][j] == c:
                src[i][j] = "both"
    res = []
    x = len(lineA)
    y = len(lineB)
    while src[x][y] is not None:
        res = [src[x][y]] + res
        if src[x][y] == "a":
            x -= 1
        elif src[x][y] == "b":
            y -= 1
        else:
            x -= 1
            y -= 1
    return res

def calc_difference(progA, progB):
    dp = []
    src = []
    for i in range(len(progA) + 1):
        line = []
        sline = []
        for j in range(len(progB) + 1):
            line.append(float("inf"))
            sline.append("")
        dp.append(line)
        src.append(sline)
    dp[0][0] = 0
    src[0][0] = None
    for i in range(1, len(progA) + 1):
        dp[i][0] = dp[i - 1][0] + len(split_tokens(progA[i - 1]))
        src[i][0] = "a"
    for i in range(1, len(progB) + 1):
        dp[0][i] = dp[0][i - 1] + len(split_tokens(progB[i - 1]))
        src[0][i] = "b"
    for i in range(1, len(progA) + 1):
        for j in range(1, len(progB) + 1):
            a = dp[i - 1][j] + len(split_tokens(progA[i - 1]))
            b = dp[i][j - 1] + len(split_tokens(progB[j - 1]))
            c = dp[i - 1][j - 1] + line_difference(progA[i - 1], progB[j - 1])
            dp[i][j] = min(a, b, c)
            if dp[i][j] == c and progA[i - 1] == progB[j - 1]:
                src[i][j] = "same"
            elif dp[i][j] == c:
                src[i][j] = "both"
            elif dp[i][j] == b:
                src[i][j] = "b"
            else:
                src[i][j] = "a"
    res = []
    x = len(progA)
    y = len(progB)
    while src[x][y] is not None:
        res = [src[x][y]] + res
        if src[x][y] == "a":
            x -= 1
        elif src[x][y] == "b":
            y -= 1
        else:
            x -= 1
            y -= 1
    return res

def render_line(lineA, lineB):
    lineA, lineB = split_tokens(lineA), split_tokens(lineB)
    disp = calc_line_difference(lineA, lineB)
    ptrA = 0
    ptrB = 0
    for i in disp:
        if i == "a":
            cprint(Fore.RED, lineA[ptrA], end = "")
            ptrA += 1
        elif i == "b":
            cprint(Fore.GREEN, lineB[ptrB], end = "")
            ptrB += 1
        elif i == "same":
            cprint(Style.RESET_ALL, lineA[ptrA], end = "")
            ptrA += 1
            ptrB += 1
        else:
            cprint(Fore.RED, lineA[ptrA], end = "")
            cprint(Fore.GREEN, lineB[ptrB], end = "")
            ptrA += 1
            ptrB += 1

def num_different_blocks(data):
    last = None
    cnt = 0
    for i in data:
        if i == "same":
            continue
        if i != last or i == "both":
            cnt += 1
            last = i
    return cnt

def render(progA, progB):
    disp = calc_difference(progA, progB)
    ptrA = 0
    ptrB = 0
    for i in disp:
        if i == "a":
            cprint(Fore.RED, progA[ptrA])
            ptrA += 1
        elif i == "b":
            cprint(Fore.GREEN, progB[ptrB])
            ptrB += 1
        elif i == "same":
            cprint(Style.RESET_ALL, progA[ptrA])
            ptrA += 1
            ptrB += 1
        else:
            if num_different_blocks(calc_line_difference(split_tokens(progA[ptrA]), split_tokens(progB[ptrB]))) <= 5:
                render_line(progA[ptrA], progB[ptrB])
                cprint(Style.RESET_ALL, "")
            else:
                cprint(Fore.RED, progA[ptrA])
                cprint(Fore.GREEN, progB[ptrB])
            ptrA += 1
            ptrB += 1

def find_proc(proc_id):
    if os.name != "posix":
        print(Fore.RED + "Fatal: cannot run program out of Linux environment." + Style.RESET_ALL)
        exit(-1)
    os.system("ps a | grep " + str(proc_id) + " > data.txt")
    with open("data.txt","r") as file:
        for line in file.readlines():
            data = line.strip()
            if int(data.split()[0]) == proc_id:
                file.close()
                return True
    return False

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
    os.system("ps a > data.txt")
    pid = None
    with open("data.txt","r") as file:
        for line in file.readlines():
            data = line.strip()
            if data.endswith(name) or data.endswith("sh -c " + proc + " &"):
                if int(data.split()[0]) != os.getpid():
                    pid = int(data.split()[0])
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

current_proc_id = None

def cprint(color, text, end = "\n"):
    print(color + text + Style.RESET_ALL, end = end)

def parse_validator_report(filename):
    with open(filename, "r") as file:
        content = "\n".join(file.readlines())
        judgement = content.split()[0]
        desc = " ".join(content.split()[1:])
        file.close()
    return (judgement,desc)

num_cases, num_errors = 0, 0

def _cleanup(file):
    if os.path.exists(file):
        os.remove(file)

def cleanup(proga, progb):
    _cleanup("data.in")
    _cleanup("data.txt")
    _cleanup("validator_report.txt")
    _cleanup("null.txt")
    _cleanup(proga + ".out")
    _cleanup(progb + ".out")

def signal_handler(signal, frame):
    cprint(Fore.WHITE, "\rDone. Total %d error(s) in %d case(s). See report at report/ ." % (num_errors, num_cases))
    exit(0)

def _workonce(datagen, proga, progb, validator, timelimita = 1, timelimitb = 1):
    global num_cases
    cprint(Fore.WHITE, str(num_cases + 1) + " Initialize...          ", end = "")
    proga_out_file = proga + ".out"
    progb_out_file = progb + ".out"
    tle=False
    cprint(Fore.WHITE, "\r" + str(num_cases + 1) + " Gen data...     ", end = "")
    do_proc(datagen + " > data.in", datagen, tl = 1)
    cprint(Fore.WHITE, "\r" + str(num_cases + 1) + " Run program 1...", end = "")
    if do_proc(proga + " < data.in > " + proga_out_file, proga, timelimita) == "TLE":
        tle=True
    cprint(Fore.WHITE, "\r" + str(num_cases + 1) + " Run program 2...", end = "")
    if do_proc(progb + " < data.in > " + progb_out_file, progb, timelimitb) == "TLE":
        tle=True
    if not tle:
        cprint(Fore.WHITE, "\r" + str(num_cases + 1) + " Validate...       ", end = "")
        _cleanup("validator_report.txt")
        do_proc(validator + " data.in " + proga_out_file + " " + progb_out_file + " 1>validator_report.txt 2>validator_report.txt", validator.split()[0], tl = 1)
        """
        Note that some of the arguments (arg 0) aren't used by the Python validators.
        That's for testlib validators because it requires the input file and a report file.
        """
        return parse_validator_report("validator_report.txt")
    else:
        with open("validator_report.txt","w") as file:
            file.write("TLE Time Limit Exceeded.")
            file.close()
        return ("TLE", "Time Limit Exceeded.")

def workonce(datagen, proga, progb, validator, timelimita = 1, timelimitb = 1, stop = True):
    global num_cases, num_errors
    res = _workonce(datagen, proga, progb, validator, timelimita, timelimitb)
    cprint(Fore.GREEN + Style.BRIGHT if res[0] == "AC" or res[0] == "ok" else Fore.RED, "\r" + str(num_cases + 1) + " " + res[0] + " " + res[1])
    if res[0] != "AC" and res[0] != "ok": # if not pass
        num_errors += 1
        os.mkdir("report/" + str(num_cases + 1))
        shutil.copyfile("data.in", "report/" + str(num_cases + 1) + "/data.in")
        shutil.copyfile(proga + ".out", "report/" + str(num_cases + 1) + "/" + proga + ".out")
        shutil.copyfile(progb + ".out", "report/" + str(num_cases + 1) + "/" + progb + ".out")
        shutil.copyfile("validator_report.txt", "report/" + str(num_cases + 1) + "/validator_report.txt")
        if stop:
            cprint(Fore.WHITE, "Done. Total %d error(s) in %d case(s). See report at report/ ." % (num_errors, num_cases + 1))
            cleanup(proga, progb)
            exit(1)
    num_cases += 1

def _bench(caseid, datagen, prog, timelimit = 1, stop = True):
    cprint(Fore.WHITE, "\r" + str(caseid) + " Gen data...          ", end = "")
    do_proc(datagen + "> data.in", datagen, tl = 1)
    cprint(Fore.WHITE, "\r" + str(caseid) + " Exec program...          ", end = "")
    if do_proc(prog + " < data.in > " + prog + ".out", prog, tl = timelimit) == "TLE":
        cprint(Fore.RED, "\r" + str(caseid) + " TLE Time Limit Exceeded.")
        global num_errors
        num_errors += 1
        os.mkdir("report/" + str(caseid))
        shutil.copyfile("data.in", "report/" + str(caseid) + "/data.in")
        if stop:
            cleanup(prog, prog)
            exit(1)
    else:
        cprint(Style.BRIGHT + Fore.GREEN, "\r" + str(caseid) + " PASS Process terminated within time limit.")

def bench(datagen, prog, timelimit = 1, cases = -1, stop = True):
    global num_cases, num_errors
    os.system("rm -rf report")
    os.mkdir("report")
    num_cases = 0
    if cases == -1:
        cid = 0
        while True:
            cid += 1
            num_cases += 1
            _bench(cid, datagen, prog, timelimit, stop)
    else:
        num_cases = cases
        for i in range(1, cases + 1):
            _bench(i, datagen, prog, timelimit, stop)
    cleanup(prog, prog)
    cprint(Fore.WHITE, "Done. Total %d error(s) in %d case(s). See report at report/ ." % (num_errors, num_cases))

def judge(datagen, proga, progb, validator, timelimita = 1, timelimitb = 1, cases = -1, stop = True):
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
            workonce(datagen, proga, progb, validator, timelimita, timelimitb, stop)
    else:
        for i in range(1, cases + 1):
            workonce(datagen, proga, progb, validator, timelimita, timelimitb, stop)
    cleanup(proga, progb)
    cprint(Fore.WHITE, "Done. Total %d error(s) in %d case(s). See report at report/ ." % (num_errors, num_cases))

def test(prog, inpfile, ansfile, timelimit, validator):
    cprint(Style.RESET_ALL, "Running...", end = "")
    if do_proc(prog + " < " + inpfile + " > " + prog + ".out", prog, tl = timelimit) != "TLE":
        _cleanup("validator_report.txt")
        do_proc(validator + " " + inpfile + " " + prog + ".out " + ansfile + " 2>validator_report.txt", validator.split()[0], tl = 1)
        res = parse_validator_report("validator_report.txt")
        cprint(Fore.GREEN if res[0] == "AC" or res[0] == "ok" else Fore.RED, "\r" + res[0] + " " + res[1])
        cleanup(prog, prog)
    else:
        cprint(Fore.RED, "\rTLE Time Limit Exceeded.")
        cleanup(prog, prog)

def diff(fileA, fileB):
    with open(fileA, "r") as file:
        contentA = "".join(file.readlines()).split("\n")
        file.close()
    with open(fileB, "r") as file:
        contentB = "".join(file.readlines()).split("\n")
        file.close()
    render(contentA, contentB)