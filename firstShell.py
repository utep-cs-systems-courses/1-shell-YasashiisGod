import os
import re

def runCommand(param):
    rc = os.fork()
    if rc < 0:
        os._exit(1)
    elif rc == 0:
        for dir in re.split(":", os.environ['PATH']):  # try each directory in the path
            program = "%s/%s" % (dir, param[0])
            try:
                os.execve(program, param, os.environ)  # try to exec program
            except FileNotFoundError:  # ...expected
                pass  # ...fail quietly

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
        if "PS1" in os.environ:
            os.write(1, (os.environ["PS1"]).encode())
        #os.write(1, ('~').encode())
        str = getInput()
        if str[0] == 'red':
            os._exit(4)
        runCommand(str)
main()