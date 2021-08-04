#!/usr/bin/python3
import sys

from commands import compose, common, container
from tools import system_tools, docker_common_tools

# ------------------------------------ common commands
help_commands = ["h", "-h", "help", "--help"]
update_commands = ["u", "update"]
version_commands = ["v", "-v", "version", "--version"]

# ------------------------------------ compose commands
compose_down_commands = ["cd", "cdown", "compose-down"]
compose_kill_commands = ["ck", "ckill", "compose-kill"]
compose_logs_commands = ["cl", "clogs", "compose-logs"]
compose_ps_commands = ["cps", "compose-ps"]
compose_start_commands = ["cstart", "compose-start"]
compose_stop_commands = ["cstop", "compose-stop"]
compose_top_commands = ["ct", "ctop", "compose-top"]

# ------------------------------------ container commands
attach_commands = ["--"]
kill_commands = ["k", "kill"]
logs_commands = ["l", "logs"]
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

    elif command in attach_commands:
        container.attach(args[1:])
    elif command in kill_commands:
        container.kill(args[1:])
    elif command in logs_commands:
        container.logs(args[1:])
    elif command in recreate_commands:
        container.recreate(args[1:])
    elif command in upgrade_commands:
        container.upgrade(args[1:])
    else:
        container.attach(args)

except (ValueError, OSError) as e:
    system_tools.die("Error: " + str(e))
except KeyboardInterrupt:
    pass
