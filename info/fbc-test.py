#!/usr/bin/env python
#!/usr/bin/env python
#!/usr/bin/env python
from sys import argv
import getopt
from os import chdir, getcwd, system, path, environ
import subprocess

if __name__ == "__main__":
    print argv

    opts, args = getopt.getopt(argv[1 :], "p:");
    profile_dir = "";
    for o, a in opts:
        if o == "-p":
            profile_dir = a;

    src_dir = args[0];
    test_dir = args[1];
    work_dir = args[2];

    if (len(args) > 3):
        ids = args[3 :];
        cur_dir = src_dir;
        if (profile_dir != ""):
            cur_dir = profile_dir;

        if (not path.exists(cur_dir + "/fbc-src/oldtests")):
            system("mv " + cur_dir + "/fbc-src/tests " + cur_dir + "/fbc-src/oldtests");
            system("cp -rf " + test_dir + " " + cur_dir + "/fbc-src/tests");

        #super hacky, because fbc itself calls *ld*, damn it fbc
        fullpath = path.abspath(path.dirname(argv[0]));
        wrappath = fullpath + "/../build/wrap";
        system("rm -rf " + wrappath + "/gcc");
        system("rm -rf " + wrappath + "/cc");

        ori_dir = getcwd();
        chdir(cur_dir + "/fbc-src/tests");
        my_env = environ;
        my_env["PATH"] = wrappath + ":" + my_env["PATH"];
        for i in ids:
            ret = subprocess.call(["timeout 12s ./fbc-run-tests.pl " + i + " 1>/dev/null 2>/dev/null"], shell = True, env = my_env);
            if (ret == 0):
                print i,
        chdir(ori_dir);
