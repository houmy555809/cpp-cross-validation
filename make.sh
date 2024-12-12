#!/bin/sh

# This file must be executed with main.py, /validators/ and /lib/ in
# the same directory. Otherwise the program cannot build the environment
# successfully.
# Mind that you will need a python environment to build.

# build environment
python3 -m pip install -U colorama nuitka
# build validators
mkdir ~/.cval
cp -r validators ~/.cval/
# compile program
python3 -m nuitka --follow-imports main.py
cp ./main.bin ./cval
cp ./cval ~
# backup files
mkdir ~/cval/src
cp make.sh          ~/.cval/src/
cp main.py          ~/.cval/src/
cp cval             ~/.cval/src/
cp -r lib           ~/.cval/src/
cp -r validators    ~/.cval/src/