#!/usr/bin/python3
import sys

from commands import compose, common, container
from errors import OpenerBaseException
from tools import system_tools, docker_common_tools

commands = [
    # ------------------------------------ common commands
    {'commands': ["h", "-h", "help", "--help"], 'function': common.help},
    {'commands': ["u", "update"], 'function': common.update},
    {'commands': ["v", "-v", "version", "--version"], 'function': common.version},

    # ------------------------------------ compose commands
    {'commands': ["cd", "cdown", "compose-down"], 'function': compose.down},
    {'commands': ["ck", "ckill", "compose-kill"], 'function': compose.kill},
    {'commands': ["cl", "clog", "clogs", "compose-logs"], 'function': compose.logs},
    {'commands': ["clist", "compose-list"], 'function': compose.clist},
    {'commands': ["cps", "compose-ps"], 'function': compose.ps},
    {'commands': ["cstart", "compose-start"], 'function': compose.start},
    {'commands': ["cstop", "compose-stop"], 'function': compose.stop},
    {'commands': ["ct", "ctop", "compose-top"], 'function': compose.top},

    # ------------------------------------ container commands
    {'commands': ["--"], 'function': container.shell},
    {'commands': ["a", "attach"], 'function': container.attach},
    {'commands': ["e", "exec"], 'function': container.docker_exec},
    {'commands': ["i", "inspect"], 'function': container.inspect},
    {'commands': ["k", "kill"], 'function': container.kill},
    {'commands': ["l", "logs", "log"], 'function': container.logs},
    {'commands': ["rm"], 'function': container.rm},

    {'commands': ["p", "pause"], 'function': container.pause},
    {'commands': ["un", "unpause"], 'function': container.unpause},

    {'commands': ["sto", "stop"], 'function': container.stop},
    {'commands': ["sta", "start"], 'function': container.start},
    {'commands': ["res", "restart"], 'function': container.restart},

    {'commands': ["port"], 'function': container.open_port},
    {'commands': ["recreate"], 'function': container.recreate},
    {'commands': ["upgrade"], 'function': container.upgrade},
]

try:
    if not docker_common_tools.is_docker_available():
        raise OSError("Docker is not available")

    args = sys.argv[1:]
    if len(args) == 0:
        common.help()
        raise ValueError("Command or target required.")

    command = args[0]

    function = next((e['function'] for e in commands if command in e['commands']), None)
    if function is not None:
        function(args[1:])
    else:
        container.shell(args)

except OpenerBaseException as e:
    system_tools.die("Opener error: " + str(e))
except (ValueError, OSError) as e:
    system_tools.die("Opener error: " + str(e))
except KeyboardInterrupt:
    pass
