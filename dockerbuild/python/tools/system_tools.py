import os
import subprocess
import sys


def die(*args):
    print('\n'.join(args))
    sys.exit(1)


def os_run(*command, stdout=True):
    """
    Run given command.
    :param command: command to run
    :param stdout: prints output to stdout if true, otherwise - returns output
    :return: Output or None
    """
    to_run = command[0]

    test = subprocess.Popen(to_run, stdout=subprocess.PIPE)
    output = test.communicate()[0].decode("utf-8")

    if stdout:
        print("%s" % output)
    else:
        return output


def divide_target_and_options(args):
    if len(args) == 0:
        raise ValueError("Logs target required!")
    elif len(args) == 1:
        if args[0][0] == '-':
            raise ValueError("Logs target required!")
        return args[0], ""
    else:
        if args[0][0] == '-':
            return args[-1], ' '.join(args[0:-1])
        return args[0], ' '.join(args[1:])


def prepare_command(command):

    debug(command)

    file_name = "command.sh"
    with open(file_name, "w") as file:
        file.write(command)


def debug(text):
    if os.environ.get("DEBUG") == "True":
        print("[DEBUG] - %s" % text)
