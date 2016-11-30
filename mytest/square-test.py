#!/usr/bin/env python
#!/usr/bin/env python
#!/usr/bin/python
from sys import argv
from getopt import getopt
from subprocess import call
from os import getcwd, system, environ, chdir
from os.path import join
from subprocess import call, Popen, PIPE

if __name__ == "__main__":
    # print argv

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
    executable = "./square-bug"
    test_dir = args[1]
    work_dir = args[2]

    diff = []
    positive = []

    if (len(args) < 4):
        ids = range(1000)
    else:
        ids = args[3:]
    
    my_env = environ

    for _id in ids:
        with open(join(test_dir, "test" + str(_id)), "r") as f:
            array = []
            for line in f:
                array.append(line.rstrip().split()[0])
            _input = array[0]
            _output = array[1]
            p = Popen([executable, _input], stdout=PIPE, stderr=PIPE)
            ret, err = p.communicate()
            #print str(ret), _output, _input
            if (int(ret) == int(_output)):
                positive.append(_id)
            else:
                diff.append(_id)

    if (len(args) < 4):
        f = open("square.revlog", "w");
        f.write("-\n-\n")
        f.write("Diff Cases: Tot " + str(len(diff)) + "\n")
        for _id in diff:
            f.write(str(_id) + " ")
        f.write("\n")
        f.write("Positive Cases: Tot " + str(len(positive)) + "\n")
        for _id in positive:
            f.write(str(_id) + " ")
        f.write("\n")
        f.write("Regression Cases: Tot 0\n")
    else:
        for _id in positive:
            print _id,
                
    chdir(this_dir)
    exit(0)
