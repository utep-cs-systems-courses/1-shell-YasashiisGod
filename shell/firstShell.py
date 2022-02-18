import os
import re
import sys
import time

def runCommand(param):
    rc = os.fork()
    if rc < 0:
        sys.exit(1)
    elif rc == 0:
        for dir in re.split(":", os.environ['PATH']):  # try each directory in the path
            program = "%s/%s" % (dir, param[0])
            try:
                os.execve(program, param, os.environ)  # try to exec program
                time.sleep(1)
            except FileNotFoundError:  # ...expected
               pass  # ...fail quietly
            #os.write (1, "Program terminated; Problem unknown")
        os.write(2, ("Command not found : %s\n" % param[0]).encode())
        os.write(2, ("Process finished with exit code 1").encode())
        sys.exit(1)
        # terminate with error

    else:
        os.wait()

def getInput():
    args = os.read(0, 100)
    args = args.decode()
    args = args.split()
    return args

def main():
    # Don't stop until red light
    while 1:
        os.write(1, (os.environ["PS1"]).encode())
        str = getInput()
        if str[0] == "red":
            sys.exit(0)
        runCommand(str)
main()