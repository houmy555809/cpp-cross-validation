import os, sys, shutil
from colorama import *

def report(status, desc):
    print(status, desc)
    exit(0)

def escape(char):
    if char in "abcdefghijklmnopqrtstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890`~!@#$%^&*()-_+=[]{}|;:<>,./?":
        return char
    elif char in "\\\"\'":
        return "\\" + char
    else:
        return "<ASCII " + ord(char) + ">"
def escapeStr(string):
    res = ""
    for i in string:
        res += escape(i)
    return res

class Validator:
    def __init__(self):
        pass
    def filea_read(self):
        with open(sys.argv[1], "r") as file:
            content = file.readlines()
            file.close()
        return content
    def fileb_read(self):
        with open(sys.argv[2], "r") as file:
            content = file.readlines()
            file.close()
        return content
    def __call__(self):
        try:
            self.judge(sys.argv[1], sys.argv[2])
        except Exception as err:
            report("UKE", "Validator returned error " + str(err))