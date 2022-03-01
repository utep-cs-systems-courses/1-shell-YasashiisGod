import os
import re
import sys
import time

def redirect(param):
    if '>' in param: #write
        os.close(1)
        os.open(param[2], os.O_CREAT | os.O_WRONLY)
        os.set_inheritable(1, True)
    if "<" in param: #read
        os.close(0)
        os.open()
    return
def ch_dir(path):
    try:
        os.chdir(path)
    except FileNotFoundError:
        os.write(2, f'file {path} not found \n'.encode())

def runCommand(param):
    rc = os.fork()
    if rc < 0:
        sys.exit(1)
    elif rc == 0:
        if (">" or "<") in param:
            print("starting redirect")
            print(param)
            redirect(param)
        for dir in re.split(":", os.environ['PATH']):  # try each directory in the path
            program = "%s/%s" % (dir, param[0])
            try:
                os.execve(program, [param[0]], os.environ)  # try to exec program
                time.sleep(1)
            except FileNotFoundError:  # ...expected
                pass  # ...fail quietly
            # os.write (1, "Program terminated; Problem unknown")
        os.write(2, ("Command not found : %s\n" % param[0]).encode())
        os.write(2, "Process finished with exit code 1".encode())
        sys.exit(1)
        # terminate with error
    else:
        os.wait()

def getInput():
    args = os.read(0, 1000)
    args = args.decode()
    args = args.split()
    return args

def main():
    # Don't stop until red light
    while True:
        os.write(1, (os.environ["PS1"]).encode())
        typing = getInput()
        #print(len(typing))
        if len(typing) == 0:
             continue #reset without stopping while loop
        if typing[0] == "red":
            sys.exit(0)
        if typing[0] == "cd" and len(typing) == 2:
            os.write(1, (os.getcwd()).encode())
            ch_dir(typing[1])
        runCommand(typing)
main()
