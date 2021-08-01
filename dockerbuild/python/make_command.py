#!/usr/bin/python3
import sys

from commands import attach, compose, help, logs, update
from tools import system_tools, docker_tools

update_commands = ["u", "update"]
help_commands = ["h", "-h", "help", "--help"]
logs_commands = ["l", "logs"]
compose_down_commands = ["cd", "cdown", "compose-down"]
compose_logs_commands = ["cl", "clogs", "compose-logs"]
compose_kill_commands = ["ck", "ckill", "compose-kill"]
compose_start_commands = ["cstart", "compose-start"]
compose_stop_commands = ["cstop", "compose-stop"]
compose_top_commands = ["ct", "ctop", "compose-top"]
attach_commands = ["--"]

try:
    if not docker_tools.is_docker_available():
        raise OSError("Docker is not available")

    args = sys.argv[1:]
    if len(args) == 0:
        system_tools.die("Target required")

    command = args[0]

    if command in help_commands:
        help.run()
    elif command in update_commands:
        update.run()
    elif command in logs_commands:
        logs.run(args[1:])
    elif command in compose_down_commands:
        compose.down(args[1:])
    elif command in compose_kill_commands:
        compose.kill(args[1:])
    elif command in compose_logs_commands:
        compose.logs(args[1:])
    elif command in compose_start_commands:
        compose.start(args[1:])
    elif command in compose_stop_commands:
        compose.stop(args[1:])
    elif command in compose_top_commands:
        compose.top(args[1:])
    elif command in attach_commands:
        attach.run(args[1:])
    else:
        attach.run(args)

except (ValueError, OSError) as e:
    system_tools.die("Error: " + str(e))
except KeyboardInterrupt:
    pass
