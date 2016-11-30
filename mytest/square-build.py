#!/usr/bin/env python
#!/usr/bin/env python
#!/usr/bin/python
from sys import argv
from getopt import getopt
from subprocess import call
from os import getcwd, system, chdir, environ
from tester_common import extract_arguments

if __name__ == "__main__":
    # print argv

    opts, args = getopt(argv[1:], "cd:")

    compile_only = False
    dryrun_src = ""

    for o, a in opts:
        if o == "-c":
            compile_only = True
        elif o == "-d":
            dryrun_src = a
    
    if (len(args) < 1):
        print("Please, provide a src dir.")
        exit(1)

    this_dir = getcwd()
    src_dir = args[0]
    chdir(src_dir)
    
    my_env = environ
    ret = call(["make"], shell = True, env = my_env)
    if ret != 0:
        chdir(this_dir)
        exit(1)

    chdir(this_dir)

    #system("cd " + str(src_dir) + " && make && cd " + str(this_dir))

    (builddir, buildargs) = extract_arguments(src_dir, dryrun_src)

    if dryrun_src != "":
        if len(args) > 1:
            out_file = open(args[1], "w");
            print >> out_file, builddir;
            print >> out_file, buildargs;
            out_file.close();
        else:
            print builddir;
            print buildargs;

    exit(0)
