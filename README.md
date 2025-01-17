# CPP Cross Validation

This is a project for OI contestants to check a solution against a brute-force approach. This project is designed for Linux environment and cannot run in Windows environment. Once built, there will be a program in the root directory named `cval`, which is the main program. The usages are:

```bash
cval judge datagen naive solution [--preset-validator=noip] [--validator-py=path/to/validator.py] [--testlib-checker=path/to/compiled_checker] [--timelimit=1] [--timelimita=1] [--timelimitb=1] [--cases=-1] [--stop|-s] [--nonstop|-n] [--no-time-limit|-t] [--no-time-limit-a|-A] [--no-time-limit-b|-B]
cval bench datagen prog [--timelimit=1] [--cases=-1] [--stop|-s] [--nonstop|-n]
```

In its default setup, it will keep running until it finds a difference in the output(s) of either programs (Wrong Answer, WA in short) or detects Time Limit Exceeded (TLE in short). However, you can set the maximum number of tests by adding `--cases=XXX`. Additionally, if you don't want the main program to stop when detecting an error, you can specify `--nonstop` or `-n` in short. You may specify the time limit by `--timelimit=XXX` (note that the time limit is in seconds). You can set the time limit of the two programs seperately, too.

## To Build

Run `make.sh` with all the other files in the same directory. Please make sure you have installed `python3`. Run `source /etc/bash.bashrc` after build.

## Todo

[-] Add multithreading support for better efficiency.

[-] Fix bugs in `testlib` support
