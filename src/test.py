#!/usr/bin/env python
from sys import argv
from getopt import getopt
from subprocess import call
from os import getcwd, system, environ, chdir
from os.path import join
from subprocess import call, Popen, PIPE
import re

if __name__ == "__main__":
    opts, args = getopt(argv[1:], "p:")
    profile_dir = ""
    for o, a in opts:
        if o == "-p":
            profile_dir = a
    
    if (len(args) < 2):
        print("Please, provide a src dir, test dir and at least one test id")
        exit(1)
        
    this_dir = getcwd()
    src_dir = args[0]
    if (profile_dir != ""):
        src_dir = profile_dir
    chdir(src_dir)
    executable = "./run_test"
    test_dir = args[1]
    work_dir = args[2]

    positive = []
    ids = args[3:]

    for id in ids:
        p = Popen([executable, str(id)], stdout=PIPE, stderr=PIPE)
        ret, err = p.communicate()
        if (re.match(".*positive.*", ret)):
            positive.append(id)

    for id in positive:
        print id,
                
    chdir(this_dir)
    exit(0)
