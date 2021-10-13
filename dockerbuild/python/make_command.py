#!/usr/bin/python3
import sys

from commands import compose, common, container
from errors import OpenerBaseException
from tools import system_tools, docker_common_tools

# ------------------------------------ common commands
help_commands = ["h", "-h", "help", "--help"]
update_commands = ["u", "update"]
version_commands = ["v", "-v", "version", "--version"]

# ------------------------------------ compose commands
compose_down_commands = ["cd", "cdown", "compose-down"]
compose_kill_commands = ["ck", "ckill", "compose-kill"]
compose_logs_commands = ["cl", "clog", "clogs", "compose-logs"]
compose_ps_commands = ["cps", "compose-ps"]
compose_start_commands = ["cstart", "compose-start"]
compose_stop_commands = ["cstop", "compose-stop"]
compose_top_commands = ["ct", "ctop", "compose-top"]

# ------------------------------------ container commands
shell_commands = ["--"]
attach_commands = ["a", "attach"]
exec_commands = ["e", "exec"]
inspect_commands = ["i", "inspect"]
kill_commands = ["k", "kill"]
logs_commands = ["l", "logs"]
rm_commands = ["rm"]

pause_commands = ["p", "pause"]
unpause_commands = ["un", "unpause"]

stop_commands = ["sto", "stop"]
start_commands = ["sta", "start"]
restart_commands = ["res", "restart"]

recreate_commands = ["recreate"]
upgrade_commands = ["upgrade"]

try:
    if not docker_common_tools.is_docker_available():
        raise OSError("Docker is not available")

    args = sys.argv[1:]
    if len(args) == 0:
        common.help()
        raise ValueError("Command or target required.")

    command = args[0]

    if command in help_commands:
        common.help()
    elif command in update_commands:
        common.update()
    elif command in version_commands:
        common.version()

    elif command in compose_down_commands:
        compose.down(args[1:])
    elif command in compose_kill_commands:
        compose.kill(args[1:])
    elif command in compose_logs_commands:
        compose.logs(args[1:])
    elif command in compose_ps_commands:
        compose.ps(args[1:])
    elif command in compose_start_commands:
        compose.start(args[1:])
    elif command in compose_stop_commands:
        compose.stop(args[1:])
    elif command in compose_top_commands:
        compose.top(args[1:])

    elif command in shell_commands:
        container.shell(args[1:])
    elif command in attach_commands:
        container.attach(args[1:])
    elif command in exec_commands:
        container.docker_exec(args[1:])
    elif command in inspect_commands:
        container.inspect(args[1:])
    elif command in kill_commands:
        container.kill(args[1:])
    elif command in logs_commands:
        container.logs(args[1:])
    elif command in rm_commands:
        container.rm(args[1:])

    elif command in pause_commands:
        container.pause(args[1:])
    elif command in unpause_commands:
        container.unpause(args[1:])

    elif command in stop_commands:
        container.stop(args[1:])
    elif command in start_commands:
        container.start(args[1:])
    elif command in restart_commands:
        container.restart(args[1:])

    elif command in recreate_commands:
        container.recreate(args[1:])
    elif command in upgrade_commands:
        container.upgrade(args[1:])
    else:
        container.shell(args)

except OpenerBaseException as e:
    system_tools.die("Error: " + str(e))
except (ValueError, OSError) as e:
    system_tools.die("Error: " + str(e))
except KeyboardInterrupt:
    pass
