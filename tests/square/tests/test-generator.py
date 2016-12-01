#!/usr/bin/env python
from sys import argv
import getopt
from itertools import repeat
import random

if __name__ == "__main__":
    opts, args = getopt.getopt(argv[1:], "p:")
    
    if (len(args) != 1):
        print("Please, provide a number of tests.")
        exit(1)
        
    num = int(args[0])
    for i in range(num):
        x = i + 1
        f = open("test" + str(i + 1), "w")
        f.write(str(x) + "\n" + str(x ** 2) + "\n")
