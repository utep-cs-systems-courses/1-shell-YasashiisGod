import os
import re
import sys
import time

def execute(param):
    for dir in re.split(":", os.environ['PATH']):  # try each directory in the path
        program = "%s/%s" % (dir, param[0])
        try:
            os.execve(program, param, os.environ)  # try to exec program
        except FileNotFoundError:  # ...expected
            pass  # ...fail quietly
        # os.write (1, "Program terminated; Problem unknown")
    os.write(2, ("Command not found : %s\n" % param[0]).encode())
    os.write(2, "Process finished with exit code 1".encode())
    sys.exit(1)


def pipe(param):
    p1 = param[0:param.index('|')]
    p2 = param[param.index('|') + 1:]
    print(p1)
    print(p2)
    r, w = os.pipe()
    os.set_inheritable(w, True)
    os.set_inheritable(r, True)
    rc = os.fork()

    if rc < 0:
        sys.exit(1)
    elif rc == 0:
        os.close(1)
        os.dup(w)
        os.set_inheritable(1, True)

        for fd in (r, w):
            os.close(fd)

        execute(p1)
        os.write(2, f"{p1}: FIALURE\n".encode())
        sys.exit(1)

    else:
        remote_control = os.fork()
        if remote_control < 0:
            os.write(2, ("fork failed, returning %d\n" % rc).encode())
            sys.exit(1)
        elif remote_control == 0:  # Second Child
            os.close(0)  # Disconnect stdin
            os.dup(r)
            os.set_inheritable(0, True)

            for fd in (w, r):
                os.close(fd)
            print("executing parent")
            execute(p2)
            os.write(2, f"{p2}: FAILED\n".encode())
            sys.exit(1)
        else:
            for fd in (w, r):
                os.close(fd)
            os.wait()


def redirect(param):
    if '>' in param:  # write
        # print("redirecting the write")
        sign = param.index('>')
        os.close(1)
        os.open(param[sign + 1], os.O_CREAT | os.O_WRONLY)
        os.set_inheritable(1, True)
        del param[sign:sign + 2]
    else:
        # print ("redirecting the read")
        sign = param.index('<')
        os.close(0)
        os.open(param[sign + 1], os.O_RDONLY)
        os.set_inheritable(0, True)
        del param[sign:sign + 2]
    return param


def ch_dir(path):
    try:
        os.chdir(path)
    except FileNotFoundError:
        os.write(2, f'file {path} not found \n'.encode())


def runCommand(param):
    rc = os.fork()
    b = False
    if '&' in param:
        param.remove('&')
        b = True
    if rc < 0:
        sys.exit(1)
    elif rc == 0:
        if (">" or "<") in param:
            param = redirect(param)
        execute(param)
    else:
        if not b:
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
        # print(len(typing))
        if len(typing) == 0:
            continue  # reset without stopping while loop
        if typing[0] == "red":
            sys.exit(0)
        if typing[0] == "cd" and len(typing) == 2:
            os.write(1, (os.getcwd()).encode())
            ch_dir(typing[1])
        if '|' in typing:
            pipe(typing)
            continue
        runCommand(typing)
main()
