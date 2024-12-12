# CPP Cross Validation

This is a project for OI contestants to check a solution against a brute-force approach. This project is designed for Linux environment and cannot run in Windows environment. Once built, there will be a program in the root directory named `cval`, which is the main program. To use the program, simply type

```bash
./cval ./datagen ./solution ./brute-force
```

and the program starts running. In its default setup, it will keep running until it finds a difference in the output(s) of either programs (Wrong Answer, WA in short) or detects Time Limit Exceeded (TLE in short). However, you can set the maximum number of tests by adding `--cases=XXX`. Additionally, if you don't want the main program to stop when detecting an error, you can specify `--nonstop` or `-n` in short. You may specify the time limit by `--timelimit=XXX` (note that the time limit is in seconds).

## To Build

Run `make.sh` with all the other files in the same directory. It relies on Python package `nuitka` to compile the source file. The shell script automatically installs `nuitka` via pip (and also `python3`, of course), and copies the source to ~/.cval.

## Todo

[-] Add support for long time limits so the program does not wait until the time limit exceedes and checks if the task still exists.

[-] Add more validators and support for `testlib` special judgers.

[-] Add multithreading support for better efficiency.
