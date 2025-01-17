#!/bin/sh

# This file must be executed with main.py, /validators/ and /lib/ in
# the same directory. Otherwise the program cannot build the environment
# successfully.
# Mind that you will need a python environment to build.

# build environment
rm -rf ~/.cvaldata
mkdir ~/.cvaldata
sudo python3 -m pip install -U colorama nuitka -i https://mirrors.aliyun.com/pypi/simple/
# build validators
cp -r ./validators ~/.cvaldata/validators
# compile program
sudo sh -c 'python3 -m nuitka --follow-imports main.py'
cat main.bin > cval
cat cval > ~/.cvaldata/cval
chmod 777 ~/.cvaldata/cval

# register as command
sudo sh -c 'echo alias cval=\"~/.cvaldata/cval\" >> /etc/bash.bashrc'
source /etc/bash.bashrc