import os, sys, re


def param(str):
    """
    Separates string of commands and arguments into a
    list of strings
    """

    commands = []
    for item in str.split():
        commands.append(item)

    return commands


def ch_dir(folder):
    """
    Change directory based on arguments
    """
    try:
        os.chdir(folder)
    except FileNotFoundError:
        os.write(1, (f'file {commands[1]} not found\n').encode())



def fail():
    """
    reports fork could not be completed
    """

    os.write(1,(f'fork failed {os.getpid()}\n').encode())
    sys.exit(1)


def perform_task(commands):
    """
    use a  procces to perform commands
    """
    for dir in re.split(':', os.environ['PATH']):
        program = f'{dir}/{commands[0]}'
        try:
            os.execve(program, commands, os.environ)
        except OSError as error:
            os.write(1,(f'Error code: {error}\n').encode())


def execute_command(commands):
    """
    Create a child process with fork and execute the command
    """
    rc = os.fork()

    if rc < 0:
        fail()
    elif rc == 0:
        perform_task(commands)
    else:
        os.wait()

def main():
    """
    run my shell forever or at leas until
    user type in exit
    """

    while True:
        cursor = f'{os.getcwd()} $'
        str = input(cursor)
        if(str == ''):
            main()
        elif (str == 'exit'):
            sys.exit(0)
        elif (str == 'help'):
            os.write(1, (f'sorry no help at this time').encode())
        elif((str[0:2] == 'cd') and (len(str) > 2)):
            ch_dir(str[3:])
        elif((len(str) == 2) and (str[0:2] == 'cd')):
            os.chdir(os.environ['HOME'])
        else:
            commands = param(str)
            execute_command(commands)


main()